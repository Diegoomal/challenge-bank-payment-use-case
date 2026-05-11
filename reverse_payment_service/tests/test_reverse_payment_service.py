from datetime import datetime, timezone
from decimal import Decimal

import pytest

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from application.schemas import ReversePaymentCommand
from application.services.reverse_payment_service import ReversePaymentService
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


class InMemoryTransactionRepository:
    def __init__(self):
        self.transactions = {}

    def save(self, transaction):
        self.transactions[transaction.id] = transaction

    def get_by_id(self, transaction_id):
        return self.transactions.get(transaction_id)


def test_reverse_payment_reverses_transaction_and_publishes_event():
    repository = InMemoryTransactionRepository()
    repository.save(Transaction.start("transaction-1", "customer-1", "merchant-1"))
    publisher = InMemoryEventPublisher()
    service = ReversePaymentService(repository, publisher)

    result = service.reverse_payment(
        ReversePaymentCommand(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            reason="INSUFFICIENT_BALANCE",
            occurred_at=datetime.now(timezone.utc),
        )
    )

    assert result.status == TransactionStatus.REVERSED
    assert result.reason == "INSUFFICIENT_BALANCE"
    assert len(publisher.reversed_events) == 1
    assert publisher.reversed_events[0].event_name == "PaymentReversed"
    assert publisher.reversed_events[0].merchant_id == "merchant-1"


def test_reverse_payment_is_idempotent_when_already_reversed():
    repository = InMemoryTransactionRepository()
    transaction = Transaction.start("transaction-1", "customer-1", "merchant-1")
    transaction.reverse("INSUFFICIENT_BALANCE")
    repository.save(transaction)
    publisher = InMemoryEventPublisher()
    service = ReversePaymentService(repository, publisher)

    result = service.reverse_payment(
        ReversePaymentCommand(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            reason="INSUFFICIENT_BALANCE",
            occurred_at=datetime.now(timezone.utc),
        )
    )

    assert result.status == TransactionStatus.REVERSED
    assert publisher.reversed_events == []


def test_reverse_payment_fails_when_transaction_not_found():
    service = ReversePaymentService(
        InMemoryTransactionRepository(),
        InMemoryEventPublisher(),
    )

    with pytest.raises(ValueError, match="transaction not found"):
        service.reverse_payment(
            ReversePaymentCommand(
                transaction_id="missing",
                customer_id="customer-1",
                merchant_id="merchant-1",
                amount=Decimal("50.00"),
                reason="ACCOUNT_NOT_FOUND",
                occurred_at=datetime.now(timezone.utc),
            )
        )
