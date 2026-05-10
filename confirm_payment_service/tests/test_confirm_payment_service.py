from datetime import datetime, timezone
from decimal import Decimal

import pytest

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from application.schemas import ConfirmPaymentCommand
from application.services.confirm_payment_service import ConfirmPaymentService
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


class InMemoryTransactionRepository:
    def __init__(self):
        self.transactions = {}

    def save(self, transaction):
        self.transactions[transaction.id] = transaction

    def get_by_id(self, transaction_id):
        return self.transactions.get(transaction_id)


def test_confirm_payment_confirms_transaction_and_publishes_event():
    repository = InMemoryTransactionRepository()
    transaction = Transaction.start("transaction-1", "merchant-1")
    repository.save(transaction)
    publisher = InMemoryEventPublisher()
    service = ConfirmPaymentService(repository, publisher)

    result = service.confirm_payment(
        ConfirmPaymentCommand(
            transaction_id="transaction-1",
            account_id="account-1",
            customer_id="customer-1",
            amount=Decimal("50.00"),
            occurred_at=datetime.now(timezone.utc),
        )
    )

    assert result.status == TransactionStatus.CONFIRMED
    assert repository.get_by_id("transaction-1").status == TransactionStatus.CONFIRMED
    assert len(publisher.confirmed_events) == 1
    assert publisher.confirmed_events[0].event_name == "PaymentConfirmed"
    assert publisher.confirmed_events[0].transaction_id == "transaction-1"
    assert publisher.confirmed_events[0].merchant_id == "merchant-1"


def test_confirm_payment_fails_when_transaction_not_found():
    service = ConfirmPaymentService(
        InMemoryTransactionRepository(),
        InMemoryEventPublisher(),
    )

    with pytest.raises(ValueError, match="transaction not found"):
        service.confirm_payment(
            ConfirmPaymentCommand(
                transaction_id="missing",
                account_id="account-1",
                customer_id="customer-1",
                amount=Decimal("50.00"),
                occurred_at=datetime.now(timezone.utc),
            )
        )
