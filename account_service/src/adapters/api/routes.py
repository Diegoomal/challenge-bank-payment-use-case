from fastapi import APIRouter, HTTPException, status

from adapters.api.schemas import CreateAccountRequest, CreateAccountResponse
from application.ports.for_creating_account import ForCreatingAccount
from application.schemas import CreateAccountCommand


def create_account_router(create_account: ForCreatingAccount) -> APIRouter:
    router = APIRouter(prefix="/accounts", tags=["accounts"])

    @router.post(
        "",
        response_model=CreateAccountResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_account_endpoint(
        request: CreateAccountRequest,
    ) -> CreateAccountResponse:
        try:
            result = create_account.create_account(
                CreateAccountCommand(
                    customer_id=request.customer_id,
                    account_holder=request.account_holder,
                    initial_deposit=request.initial_deposit,
                )
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

        return CreateAccountResponse(
            account_id=result.account_id,
            customer_id=result.customer_id,
            status=result.status,
            created_at=result.created_at,
        )

    return router
