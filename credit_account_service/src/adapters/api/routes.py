from fastapi import APIRouter

from adapters.api.schemas import CreditAccountRequest, CreditAccountResponse
from application.ports.for_crediting_account import ForCreditingAccount
from application.schemas import CreditAccountCommand


def create_account_router(credit_account: ForCreditingAccount) -> APIRouter:
    router = APIRouter(prefix="/accounts", tags=["accounts"])

    @router.post("/credit", response_model=CreditAccountResponse)
    def credit_account_endpoint(request: CreditAccountRequest) -> CreditAccountResponse:
        result = credit_account.credit_account(
            CreditAccountCommand(
                transaction_id=request.transaction_id,
                customer_id=request.customer_id,
                merchant_id=request.merchant_id,
                amount=request.amount,
            )
        )
        return CreditAccountResponse(
            account_id=result.account_id,
            transaction_id=result.transaction_id,
            status=result.status,
            reason=result.reason,
        )

    return router
