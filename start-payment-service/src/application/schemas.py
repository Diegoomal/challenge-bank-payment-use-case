from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.payment_method import PaymentMethod
from domain.transaction_status import TransactionStatus


@dataclass(frozen=True)
class StartPaymentCommand:
    customer_id: str
    merchant_id: str
    amount: Decimal
    payment_method: PaymentMethod


@dataclass(frozen=True)
class StartPaymentResult:
    transaction_id: str
    status: TransactionStatus
    created_at: datetime
