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
    reversal_reason: str | None = None
    reversed_at: datetime | None = None

    @classmethod
    def start(cls, transaction_id: str) -> "Transaction":
        cls._validate_required("transaction_id", transaction_id)
        now = datetime.now(timezone.utc)
        return cls(
            id=transaction_id,
            status=TransactionStatus.STARTED,
            created_at=now,
            updated_at=now,
        )

    def reverse(self, reason: str) -> datetime:
        self._validate_required("reason", reason)
        if self.status not in [TransactionStatus.STARTED, TransactionStatus.PROCESSING]:
            raise InvalidTransactionStatus(
                f"transaction cannot be reversed from {self.status.value}"
            )
        now = datetime.now(timezone.utc)
        self.status = TransactionStatus.REVERSED
        self.reversal_reason = reason
        self.reversed_at = now
        self.updated_at = now
        return now

    @staticmethod
    def _validate_required(field_name: str, value: str) -> None:
        if not value or not value.strip():
            raise ValueError(f"{field_name} is required")
