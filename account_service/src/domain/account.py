from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from domain.account_status import AccountStatus


@dataclass
class Account:
    id: str
    customer_id: str
    account_holder: str
    balance: Decimal
    status: AccountStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        customer_id: str,
        account_holder: str,
        initial_deposit: Decimal,
    ) -> "Account":
        cls._validate_required("customer_id", customer_id)
        cls._validate_required("account_holder", account_holder)
        cls._validate_initial_deposit(initial_deposit)

        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            customer_id=customer_id,
            account_holder=account_holder,
            balance=initial_deposit,
            status=AccountStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _validate_required(field_name: str, value: str) -> None:
        if not value or not value.strip():
            raise ValueError(f"{field_name} is required")

    @staticmethod
    def _validate_initial_deposit(initial_deposit: Decimal) -> None:
        if initial_deposit < Decimal("0"):
            raise ValueError("initial deposit cannot be negative")
