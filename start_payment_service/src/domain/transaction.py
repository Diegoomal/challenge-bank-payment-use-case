from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from domain.payment_method import PaymentMethod
from domain.transaction_status import TransactionStatus


@dataclass
class Transaction:
    id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    payment_method: PaymentMethod
    status: TransactionStatus
    created_at: datetime
    updated_at: datetime

    @classmethod
    def start(
        cls,
        customer_id: str,
        merchant_id: str,
        amount: Decimal,
        payment_method: PaymentMethod,
    ) -> "Transaction":
        cls._validate_required("customer_id", customer_id)
        cls._validate_required("merchant_id", merchant_id)
        cls._validate_amount(amount)

        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            customer_id=customer_id,
            merchant_id=merchant_id,
            amount=amount,
            payment_method=payment_method,
            status=TransactionStatus.STARTED,
            created_at=now,
            updated_at=now,
        )

    @staticmethod
    def _validate_required(field_name: str, value: str) -> None:
        if not value or not value.strip():
            raise ValueError(f"{field_name} is required")

    @staticmethod
    def _validate_amount(amount: Decimal) -> None:
        if amount <= Decimal("0"):
            raise ValueError("amount must be greater than zero")
