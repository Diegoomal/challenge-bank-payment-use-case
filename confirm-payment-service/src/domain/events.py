from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class PaymentConfirmed:
    transaction_id: str
    customer_id: str
    merchant_id: str
    account_id: str
    amount: Decimal
    confirmed_at: datetime

    @property
    def event_name(self) -> str:
        return "PaymentConfirmed"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "merchant_id": self.merchant_id,
            "account_id": self.account_id,
            "amount": str(self.amount),
            "confirmed_at": self.confirmed_at.isoformat(),
        }
