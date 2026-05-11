from fastapi import APIRouter

from adapters.api.schemas import DebitAccountRequest, DebitAccountResponse
from application.ports.for_debiting_account import ForDebitingAccount
from application.schemas import DebitAccountCommand


def create_account_router(debit_account: ForDebitingAccount) -> APIRouter:
    router = APIRouter(prefix="/accounts", tags=["accounts"])

    @router.post("/debit", response_model=DebitAccountResponse)
    def debit_account_endpoint(request: DebitAccountRequest) -> DebitAccountResponse:
        result = debit_account.debit_account(
            DebitAccountCommand(
                transaction_id=request.transaction_id,
                customer_id=request.customer_id,
                merchant_id=request.merchant_id,
                amount=request.amount,
            )
        )
        return DebitAccountResponse(
            account_id=result.account_id,
            transaction_id=result.transaction_id,
            status=result.status,
            reason=result.reason,
        )

    return router
