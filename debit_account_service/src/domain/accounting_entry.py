from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class AccountingEntry:
    id: str
    account_id: str
    transaction_id: str
    amount: Decimal
    entry_type: str
    created_at: datetime
