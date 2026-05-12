from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class CreditCompleted:
    transaction_id: str
    account_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    credited_at: datetime

    @property
    def event_name(self) -> str:
        return "CreditCompleted"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "transaction_id": self.transaction_id,
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "merchant_id": self.merchant_id,
            "amount": str(self.amount),
            "credited_at": self.credited_at.isoformat(),
        }


@dataclass(frozen=True)
class CreditFailed:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    reason: str
    failed_at: datetime

    @property
    def event_name(self) -> str:
        return "CreditFailed"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "transaction_id": self.transaction_id,
            "customer_id": self.customer_id,
            "merchant_id": self.merchant_id,
            "amount": str(self.amount),
            "reason": self.reason,
            "failed_at": self.failed_at.isoformat(),
        }
