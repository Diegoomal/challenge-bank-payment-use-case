from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from domain.transaction_status import TransactionStatus


class ConfirmPaymentRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    account_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0)
    occurred_at: datetime


class ConfirmPaymentResponse(BaseModel):
    transaction_id: str
    status: TransactionStatus
    confirmed_at: datetime
