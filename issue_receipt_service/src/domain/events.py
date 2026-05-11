from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class ReceiptIssued:
    receipt_id: str
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    issued_at: datetime

    @property
    def event_name(self) -> str:
        return "ReceiptIssued"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "receipt_id": self.receipt_id,
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "merchant_id": self.merchant_id,
            "amount": str(self.amount),
            "issued_at": self.issued_at.isoformat(),
        }


PaymentStarted = ReceiptIssued
