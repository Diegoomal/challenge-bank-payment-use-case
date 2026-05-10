from dataclasses import dataclass
from decimal import Decimal

from domain.debit_status import DebitStatus


@dataclass(frozen=True)
class DebitAccountCommand:
    transaction_id: str
    customer_id: str
    amount: Decimal


@dataclass(frozen=True)
class DebitAccountResult:
    account_id: str | None
    transaction_id: str
    status: DebitStatus
    reason: str | None = None
