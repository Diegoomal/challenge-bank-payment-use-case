from datetime import datetime, timezone
from decimal import Decimal

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.saga_event_handler import (
    DebitFailedMessage,
    PaymentStartedMessage,
    SagaEventHandler,
)
from application.services.reverse_payment_service import ReversePaymentService
from domain.transaction_status import TransactionStatus


class InMemoryTransactionRepository:
    def __init__(self):
        self.transactions = {}

    def save(self, transaction):
        self.transactions[transaction.id] = transaction

    def get_by_id(self, transaction_id):
        return self.transactions.get(transaction_id)


def test_saga_handler_projects_payment_started_and_reverses_debit_failed():
    repository = InMemoryTransactionRepository()
    publisher = InMemoryEventPublisher()
    service = ReversePaymentService(repository, publisher)
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
    result = handler.handle_debit_failed(
        DebitFailedMessage(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            reason="INSUFFICIENT_BALANCE",
            occurred_at=datetime.now(timezone.utc),
        )
    )

    assert result.status == TransactionStatus.REVERSED
    assert len(publisher.reversed_events) == 1
    assert publisher.reversed_events[0].merchant_id == "merchant-1"
