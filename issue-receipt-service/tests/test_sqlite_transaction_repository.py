from datetime import datetime, timezone
from decimal import Decimal

from adapters.persistence.sqlite_receipt_repository import SQLiteReceiptRepository
from domain.issuing_status import IssuingStatus
from domain.receipt import Receipt


def test_sqlite_receipt_repository_saves_and_gets_receipt(tmp_path):
    repository = SQLiteReceiptRepository(str(tmp_path / "receipts.db"))
    receipt = Receipt.create_pending(
        transaction_id="transaction-1",
        customer_id="customer-1",
        merchant_id="merchant-1",
        amount=Decimal("99.99"),
        confirmed_at=datetime.now(timezone.utc),
    )
    receipt.issue("document-data")

    repository.save(receipt)

    saved = repository.get_by_id(receipt.id)
    assert saved is not None
    assert saved.id == receipt.id
    assert saved.transaction_id == "transaction-1"
    assert saved.amount == Decimal("99.99")
    assert saved.status == IssuingStatus.ISSUED
    assert saved.document_data == "document-data"


def test_sqlite_receipt_repository_gets_by_transaction_id(tmp_path):
    repository = SQLiteReceiptRepository(str(tmp_path / "receipts.db"))
    receipt = Receipt.create_pending(
        transaction_id="transaction-1",
        customer_id="customer-1",
        merchant_id="merchant-1",
        amount=Decimal("99.99"),
        confirmed_at=datetime.now(timezone.utc),
    )
    repository.save(receipt)

    saved = repository.get_by_transaction_id("transaction-1")

    assert saved is not None
    assert saved.id == receipt.id


def test_sqlite_receipt_repository_returns_none_when_not_found(tmp_path):
    repository = SQLiteReceiptRepository(str(tmp_path / "receipts.db"))

    assert repository.get_by_id("missing") is None
