from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from domain.issuing_status import IssuingStatus


class IssueReceiptRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    merchant_id: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0)
    confirmed_at: datetime


class IssueReceiptResponse(BaseModel):
    receipt_id: str
    transaction_id: str
    status: IssuingStatus
    issued_at: datetime | None


StartPaymentRequest = IssueReceiptRequest
StartPaymentResponse = IssueReceiptResponse
