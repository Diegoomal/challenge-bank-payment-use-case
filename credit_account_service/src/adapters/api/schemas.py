from decimal import Decimal

from pydantic import BaseModel, Field

from domain.credit_status import CreditStatus


class CreditAccountRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    merchant_id: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0)


class CreditAccountResponse(BaseModel):
    account_id: str | None
    transaction_id: str
    status: CreditStatus
    reason: str | None = None
