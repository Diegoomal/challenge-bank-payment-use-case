from dataclasses import dataclass
from decimal import Decimal

from domain.credit_status import CreditStatus


@dataclass(frozen=True)
class CreditAccountCommand:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal


@dataclass(frozen=True)
class CreditAccountResult:
    account_id: str | None
    transaction_id: str
    status: CreditStatus
    reason: str | None = None
