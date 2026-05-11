from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from domain.transaction_status import TransactionStatus


class ReversePaymentRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    merchant_id: str | None = Field(default=None, min_length=1)
    amount: Decimal = Field(..., gt=0)
    reason: str = Field(..., min_length=1)
    occurred_at: datetime


class ReversePaymentResponse(BaseModel):
    transaction_id: str
    status: TransactionStatus
    reversed_at: datetime
    reason: str
