from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.transaction_status import TransactionStatus


@dataclass(frozen=True)
class ReversePaymentCommand:
    transaction_id: str
    customer_id: str
    merchant_id: str | None
    amount: Decimal
    reason: str
    occurred_at: datetime


@dataclass(frozen=True)
class ReversePaymentResult:
    transaction_id: str
    status: TransactionStatus
    reversed_at: datetime
    reason: str
