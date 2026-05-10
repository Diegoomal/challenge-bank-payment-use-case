from datetime import datetime, timezone
from decimal import Decimal

import pytest

from domain.issuing_status import IssuingStatus
from domain.receipt import Receipt


def test_receipt_starts_pending_with_transaction_snapshot():
    receipt = Receipt.create_pending(
        transaction_id="transaction-1",
        customer_id="customer-1",
        merchant_id="merchant-1",
        amount=Decimal("10.50"),
        confirmed_at=datetime.now(timezone.utc),
    )

    assert receipt.id
    assert receipt.status == IssuingStatus.PENDING
    assert receipt.transaction_id == "transaction-1"
    assert receipt.amount == Decimal("10.50")


def test_receipt_can_be_issued_with_document_data():
    receipt = Receipt.create_pending(
        transaction_id="transaction-1",
        customer_id="customer-1",
        merchant_id="merchant-1",
        amount=Decimal("10.50"),
        confirmed_at=datetime.now(timezone.utc),
    )

    issued_at = receipt.issue("document-data")

    assert receipt.status == IssuingStatus.ISSUED
    assert receipt.document_data == "document-data"
    assert receipt.issued_at == issued_at


def test_receipt_can_fail():
    receipt = Receipt.create_pending(
        transaction_id="transaction-1",
        customer_id="customer-1",
        merchant_id="merchant-1",
        amount=Decimal("10.50"),
        confirmed_at=datetime.now(timezone.utc),
    )

    receipt.fail("generation failed")

    assert receipt.status == IssuingStatus.FAILED
    assert receipt.failure_reason == "generation failed"


def test_receipt_rejects_non_positive_amount():
    with pytest.raises(ValueError, match="amount must be greater than zero"):
        Receipt.create_pending(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("0"),
            confirmed_at=datetime.now(timezone.utc),
        )


def test_receipt_requires_transaction_id():
    with pytest.raises(ValueError, match="transaction_id is required"):
        Receipt.create_pending(
            transaction_id="",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("10.00"),
            confirmed_at=datetime.now(timezone.utc),
        )
