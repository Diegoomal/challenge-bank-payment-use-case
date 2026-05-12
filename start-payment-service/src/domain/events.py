from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.payment_method import PaymentMethod


@dataclass(frozen=True)
class PaymentStarted:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    payment_method: PaymentMethod
    occurred_at: datetime

    @property
    def event_name(self) -> str:
        return "PaymentStarted"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "merchant_id": self.merchant_id,
            "amount": str(self.amount),
            "payment_method": self.payment_method.value,
            "occurred_at": self.occurred_at.isoformat(),
        }
