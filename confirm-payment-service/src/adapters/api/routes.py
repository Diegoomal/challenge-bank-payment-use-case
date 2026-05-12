from fastapi import APIRouter, HTTPException, status

from adapters.api.schemas import ConfirmPaymentRequest, ConfirmPaymentResponse
from application.ports.for_confirming_payment import ForConfirmingPayment
from application.schemas import ConfirmPaymentCommand


def create_payment_router(confirm_payment: ForConfirmingPayment) -> APIRouter:
    router = APIRouter(prefix="/payments", tags=["payments"])

    @router.post("/confirm", response_model=ConfirmPaymentResponse)
    def confirm_payment_endpoint(
        request: ConfirmPaymentRequest,
    ) -> ConfirmPaymentResponse:
        try:
            result = confirm_payment.confirm_payment(
                ConfirmPaymentCommand(
                    transaction_id=request.transaction_id,
                    account_id=request.account_id,
                    customer_id=request.customer_id,
                    amount=request.amount,
                    occurred_at=request.occurred_at,
                )
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        return ConfirmPaymentResponse(
            transaction_id=result.transaction_id,
            status=result.status,
            confirmed_at=result.confirmed_at,
        )

    return router
