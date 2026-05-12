from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.transaction_status import TransactionStatus


@dataclass(frozen=True)
class ConfirmPaymentCommand:
    transaction_id: str
    account_id: str
    customer_id: str
    amount: Decimal
    occurred_at: datetime


@dataclass(frozen=True)
class ConfirmPaymentResult:
    transaction_id: str
    status: TransactionStatus
    confirmed_at: datetime
