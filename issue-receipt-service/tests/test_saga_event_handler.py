from datetime import datetime, timezone
from decimal import Decimal

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.saga_event_handler import (
    PaymentConfirmedMessage,
    SagaEventHandler,
)
from adapters.receipt.in_memory_receipt_generator import InMemoryReceiptGenerator
from application.services.issue_receipt_service import IssueReceiptService
from domain.issuing_status import IssuingStatus


class InMemoryReceiptRepository:
    def __init__(self):
        self.receipts = {}

    def save(self, receipt):
        self.receipts[receipt.id] = receipt

    def get_by_id(self, receipt_id):
        return self.receipts.get(receipt_id)

    def get_by_transaction_id(self, transaction_id):
        return next(
            (
                receipt
                for receipt in self.receipts.values()
                if receipt.transaction_id == transaction_id
            ),
            None,
        )


def test_saga_handler_issues_receipt_when_payment_is_confirmed():
    publisher = InMemoryEventPublisher()
    service = IssueReceiptService(
        InMemoryReceiptRepository(),
        InMemoryReceiptGenerator(),
        publisher,
    )
    handler = SagaEventHandler(service)

    result = handler.handle_payment_confirmed(
        PaymentConfirmedMessage(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            confirmed_at=datetime.now(timezone.utc),
        )
    )

    assert result.status == IssuingStatus.ISSUED
    assert len(publisher.issued_events) == 1
