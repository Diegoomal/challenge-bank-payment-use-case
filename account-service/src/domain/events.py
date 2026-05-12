from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class AccountCreated:
    account_id: str
    customer_id: str
    account_holder: str
    initial_deposit: Decimal
    occurred_at: datetime

    @property
    def event_name(self) -> str:
        return "AccountCreated"

    def to_payload(self) -> dict[str, str]:
        return {
            "event_name": self.event_name,
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "account_holder": self.account_holder,
            "initial_deposit": str(self.initial_deposit),
            "occurred_at": self.occurred_at.isoformat(),
        }
