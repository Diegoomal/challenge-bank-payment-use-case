from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.issuing_status import IssuingStatus


@dataclass(frozen=True)
class IssueReceiptCommand:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    confirmed_at: datetime


@dataclass(frozen=True)
class IssueReceiptResult:
    receipt_id: str
    transaction_id: str
    status: IssuingStatus
    issued_at: datetime | None


StartPaymentCommand = IssueReceiptCommand
StartPaymentResult = IssueReceiptResult
