from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.account_status import AccountStatus


@dataclass(frozen=True)
class CreateAccountCommand:
    customer_id: str
    account_holder: str
    initial_deposit: Decimal


@dataclass(frozen=True)
class CreateAccountResult:
    account_id: str
    customer_id: str
    status: AccountStatus
    created_at: datetime
