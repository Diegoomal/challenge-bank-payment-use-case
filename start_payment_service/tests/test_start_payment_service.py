from decimal import Decimal

import pytest

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from application.schemas import StartPaymentCommand
from application.services.start_payment_service import StartPaymentService
from domain.payment_method import PaymentMethod
from domain.transaction_status import TransactionStatus


class InMemoryTransactionRepository:
    def __init__(self):
        self.transactions = {}

    def save(self, transaction):
        self.transactions[transaction.id] = transaction

    def get_by_id(self, transaction_id):
        return self.transactions.get(transaction_id)


def test_start_payment_persists_transaction_and_publishes_event():
    repository = InMemoryTransactionRepository()
    publisher = InMemoryEventPublisher()
    service = StartPaymentService(repository, publisher)

    result = service.start_payment(
        StartPaymentCommand(
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("25.90"),
            payment_method=PaymentMethod.PIX,
        )
    )

    transaction = repository.get_by_id(result.transaction_id)
    assert result.status == TransactionStatus.STARTED
    assert transaction is not None
    assert transaction.status == TransactionStatus.STARTED
    assert len(publisher.published_events) == 1

    event = publisher.published_events[0]
    assert event.event_name == "PaymentStarted"
    assert event.transaction_id == result.transaction_id
    assert event.customer_id == "customer-1"
    assert event.merchant_id == "merchant-1"
    assert event.amount == Decimal("25.90")
    assert event.payment_method == PaymentMethod.PIX


def test_start_payment_rejects_invalid_amount_before_publishing_event():
    repository = InMemoryTransactionRepository()
    publisher = InMemoryEventPublisher()
    service = StartPaymentService(repository, publisher)

    with pytest.raises(ValueError, match="amount must be greater than zero"):
        service.start_payment(
            StartPaymentCommand(
                customer_id="customer-1",
                merchant_id="merchant-1",
                amount=Decimal("-1"),
                payment_method=PaymentMethod.PIX,
            )
        )

    assert repository.transactions == {}
    assert publisher.published_events == []
