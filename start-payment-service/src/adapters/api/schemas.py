from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from domain.payment_method import PaymentMethod
from domain.transaction_status import TransactionStatus


class StartPaymentRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    merchant_id: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0)
    payment_method: PaymentMethod


class StartPaymentResponse(BaseModel):
    transaction_id: str
    status: TransactionStatus
    created_at: datetime
