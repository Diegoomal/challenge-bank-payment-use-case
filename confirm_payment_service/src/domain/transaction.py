from dataclasses import dataclass
from datetime import datetime, timezone

from domain.exceptions import InvalidTransactionStatus
from domain.transaction_status import TransactionStatus


@dataclass
class Transaction:
    id: str
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime
    confirmed_at: datetime | None = None

    @classmethod
    def start(cls, transaction_id: str) -> "Transaction":
        cls._validate_transaction_id(transaction_id)
        now = datetime.now(timezone.utc)
        return cls(
            id=transaction_id,
            status=TransactionStatus.STARTED,
            created_at=now,
            updated_at=now,
        )

    def confirm(self) -> datetime:
        if self.status != TransactionStatus.STARTED:
            raise InvalidTransactionStatus(
                f"transaction cannot be confirmed from {self.status.value}"
            )
        now = datetime.now(timezone.utc)
        self.status = TransactionStatus.CONFIRMED
        self.confirmed_at = now
        self.updated_at = now
        return now

    @staticmethod
    def _validate_transaction_id(transaction_id: str) -> None:
        if not transaction_id or not transaction_id.strip():
            raise ValueError("transaction_id is required")
