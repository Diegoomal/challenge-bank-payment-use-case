from datetime import datetime, timezone
from decimal import Decimal

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.receipt.in_memory_receipt_generator import InMemoryReceiptGenerator
from application.schemas import IssueReceiptCommand
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


class FailingReceiptGenerator:
    def generate(self, receipt):
        raise RuntimeError("generation failed")


def test_issue_receipt_persists_receipt_and_publishes_event():
    repository = InMemoryReceiptRepository()
    publisher = InMemoryEventPublisher()
    service = IssueReceiptService(repository, InMemoryReceiptGenerator(), publisher)

    result = service.issue_receipt(
        IssueReceiptCommand(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("25.90"),
            confirmed_at=datetime.now(timezone.utc),
        )
    )

    receipt = repository.get_by_id(result.receipt_id)
    assert result.status == IssuingStatus.ISSUED
    assert receipt is not None
    assert receipt.status == IssuingStatus.ISSUED
    assert receipt.document_data
    assert len(publisher.issued_events) == 1

    event = publisher.issued_events[0]
    assert event.event_name == "ReceiptIssued"
    assert event.receipt_id == result.receipt_id
    assert event.transaction_id == result.transaction_id
    assert event.customer_id == "customer-1"
    assert event.merchant_id == "merchant-1"
    assert event.amount == Decimal("25.90")


def test_issue_receipt_is_idempotent_when_already_issued():
    repository = InMemoryReceiptRepository()
    publisher = InMemoryEventPublisher()
    service = IssueReceiptService(repository, InMemoryReceiptGenerator(), publisher)
    command = IssueReceiptCommand(
        transaction_id="transaction-1",
        customer_id="customer-1",
        merchant_id="merchant-1",
        amount=Decimal("25.90"),
        confirmed_at=datetime.now(timezone.utc),
    )

    first = service.issue_receipt(command)
    second = service.issue_receipt(command)

    assert second.receipt_id == first.receipt_id
    assert len(publisher.issued_events) == 1


def test_issue_receipt_records_failure_without_publishing_event():
    repository = InMemoryReceiptRepository()
    publisher = InMemoryEventPublisher()
    service = IssueReceiptService(repository, FailingReceiptGenerator(), publisher)

    result = service.issue_receipt(
        IssueReceiptCommand(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("25.90"),
            confirmed_at=datetime.now(timezone.utc),
        )
    )

    assert result.status == IssuingStatus.FAILED
    assert publisher.issued_events == []
