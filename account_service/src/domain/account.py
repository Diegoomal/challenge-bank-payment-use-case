from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from domain.accounting_entry import AccountingEntry
from domain.exceptions import InsufficientBalance


@dataclass
class Account:
    id: str
    customer_id: str
    holder_name: str
    balance: Decimal
    created_at: datetime
    updated_at: datetime
    entries: list[AccountingEntry] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        customer_id: str,
        holder_name: str,
        balance: Decimal,
    ) -> "Account":
        cls._validate_required("customer_id", customer_id)
        cls._validate_required("holder_name", holder_name)
        cls._validate_balance(balance)

        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            customer_id=customer_id,
            holder_name=holder_name,
            balance=balance,
            created_at=now,
            updated_at=now,
        )

    def debit(self, transaction_id: str, amount: Decimal) -> AccountingEntry:
        self._validate_required("transaction_id", transaction_id)
        self._validate_debit_amount(amount)

        if self.balance < amount:
            raise InsufficientBalance("insufficient balance")

        self.balance -= amount
        self.updated_at = datetime.now(timezone.utc)
        entry = AccountingEntry(
            id=str(uuid4()),
            account_id=self.id,
            transaction_id=transaction_id,
            amount=amount,
            entry_type="DEBIT",
            created_at=self.updated_at,
        )
        self.entries.append(entry)
        return entry

    @staticmethod
    def _validate_required(field_name: str, value: str) -> None:
        if not value or not value.strip():
            raise ValueError(f"{field_name} is required")

    @staticmethod
    def _validate_balance(balance: Decimal) -> None:
        if balance < Decimal("0"):
            raise ValueError("balance cannot be negative")

    @staticmethod
    def _validate_debit_amount(amount: Decimal) -> None:
        if amount <= Decimal("0"):
            raise ValueError("amount must be greater than zero")
