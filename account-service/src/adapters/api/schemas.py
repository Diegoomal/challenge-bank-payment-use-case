from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from domain.account_status import AccountStatus


class CreateAccountRequest(BaseModel):
    customer_id: str = Field(..., min_length=1)
    account_holder: str = Field(..., min_length=1)
    initial_deposit: Decimal = Field(..., ge=0)


class CreateAccountResponse(BaseModel):
    account_id: str
    customer_id: str
    status: AccountStatus
    created_at: datetime
