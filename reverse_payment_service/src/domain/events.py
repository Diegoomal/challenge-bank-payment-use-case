from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class PaymentReversed:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    reason: str
    reversed_at: datetime

    @property
    def event_name(self) -> str:
        return "PaymentReversed"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "merchant_id": self.merchant_id,
            "amount": str(self.amount),
            "reason": self.reason,
            "reversed_at": self.reversed_at.isoformat(),
        }
