from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class DebitCompleted:
    transaction_id: str
    account_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    occurred_at: datetime

    @property
    def event_name(self) -> str:
        return "DebitCompleted"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "merchant_id": self.merchant_id,
            "amount": str(self.amount),
            "occurred_at": self.occurred_at.isoformat(),
        }


@dataclass(frozen=True)
class DebitFailed:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    reason: str
    occurred_at: datetime

    @property
    def event_name(self) -> str:
        return "DebitFailed"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "merchant_id": self.merchant_id,
            "amount": str(self.amount),
            "reason": self.reason,
            "occurred_at": self.occurred_at.isoformat(),
        }
