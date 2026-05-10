from datetime import datetime, timezone
from decimal import Decimal

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.saga_event_handler import (
    DebitCompletedMessage,
    PaymentStartedMessage,
    SagaEventHandler,
)
from application.services.confirm_payment_service import ConfirmPaymentService
from domain.transaction_status import TransactionStatus


class InMemoryTransactionRepository:
    def __init__(self):
        self.transactions = {}

    def save(self, transaction):
        self.transactions[transaction.id] = transaction

    def get_by_id(self, transaction_id):
        return self.transactions.get(transaction_id)


def test_saga_handler_projects_payment_started_and_confirms_debit_completed():
    repository = InMemoryTransactionRepository()
    publisher = InMemoryEventPublisher()
    service = ConfirmPaymentService(repository, publisher)
    handler = SagaEventHandler(repository, service)

    handler.handle_payment_started(
        PaymentStartedMessage(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            payment_method="ACCOUNT_BALANCE",
            occurred_at=datetime.now(timezone.utc),
        )
    )
    result = handler.handle_debit_completed(
        DebitCompletedMessage(
            transaction_id="transaction-1",
            account_id="account-1",
            customer_id="customer-1",
            amount=Decimal("50.00"),
            occurred_at=datetime.now(timezone.utc),
        )
    )

    assert result.status == TransactionStatus.CONFIRMED
    assert len(publisher.confirmed_events) == 1
