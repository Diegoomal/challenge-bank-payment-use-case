from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from domain.issuing_status import IssuingStatus


@dataclass
class TransactionData:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    confirmed_at: datetime


@dataclass
class Receipt:
    id: str
    transaction_data: TransactionData
    status: IssuingStatus
    document_data: str | None
    created_at: datetime
    updated_at: datetime
    issued_at: datetime | None = None
    failure_reason: str | None = None

    @property
    def transaction_id(self) -> str:
        return self.transaction_data.transaction_id

    @property
    def customer_id(self) -> str:
        return self.transaction_data.customer_id

    @property
    def merchant_id(self) -> str:
        return self.transaction_data.merchant_id

    @property
    def amount(self) -> Decimal:
        return self.transaction_data.amount

    @property
    def confirmed_at(self) -> datetime:
        return self.transaction_data.confirmed_at

    @classmethod
    def create_pending(
        cls,
        transaction_id: str,
        customer_id: str,
        merchant_id: str,
        amount: Decimal,
        confirmed_at: datetime,
    ) -> "Receipt":
        cls._validate_required("transaction_id", transaction_id)
        cls._validate_required("customer_id", customer_id)
        cls._validate_required("merchant_id", merchant_id)
        cls._validate_amount(amount)

        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            transaction_data=TransactionData(
                transaction_id=transaction_id,
                customer_id=customer_id,
                merchant_id=merchant_id,
                amount=amount,
                confirmed_at=confirmed_at,
            ),
            status=IssuingStatus.PENDING,
            document_data=None,
            created_at=now,
            updated_at=now,
        )

    def issue(self, document_data: str) -> datetime:
        self._validate_required("document_data", document_data)
        issued_at = datetime.now(timezone.utc)
        self.status = IssuingStatus.ISSUED
        self.document_data = document_data
        self.issued_at = issued_at
        self.failure_reason = None
        self.updated_at = issued_at
        return issued_at

    def fail(self, reason: str) -> None:
        self._validate_required("failure_reason", reason)
        now = datetime.now(timezone.utc)
        self.status = IssuingStatus.FAILED
        self.failure_reason = reason
        self.updated_at = now

    @staticmethod
    def _validate_required(field_name: str, value: str) -> None:
        if not value or not value.strip():
            raise ValueError(f"{field_name} is required")

    @staticmethod
    def _validate_amount(amount: Decimal) -> None:
        if amount <= Decimal("0"):
            raise ValueError("amount must be greater than zero")


@dataclass
class Transaction:
    id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    payment_method: object
    status: object
    created_at: datetime
    updated_at: datetime
