from decimal import Decimal

from pydantic import BaseModel, Field

from domain.debit_status import DebitStatus


class DebitAccountRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    merchant_id: str = Field(default="", min_length=0)
    amount: Decimal = Field(..., gt=0)


class DebitAccountResponse(BaseModel):
    account_id: str | None
    transaction_id: str
    status: DebitStatus
    reason: str | None = None
