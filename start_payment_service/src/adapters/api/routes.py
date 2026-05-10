from fastapi import APIRouter, HTTPException, status

from application.ports.for_starting_payment import ForStartingPayment
from application.schemas import StartPaymentCommand
from adapters.api.schemas import StartPaymentRequest, StartPaymentResponse


def create_payment_router(start_payment: ForStartingPayment) -> APIRouter:
    router = APIRouter(prefix="/payments", tags=["payments"])

    @router.post(
        "/start",
        response_model=StartPaymentResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def start_payment_endpoint(request: StartPaymentRequest) -> StartPaymentResponse:
        try:
            result = start_payment.start_payment(
                StartPaymentCommand(
                    customer_id=request.customer_id,
                    merchant_id=request.merchant_id,
                    amount=request.amount,
                    payment_method=request.payment_method,
                )
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
            ) from error

        return StartPaymentResponse(
            transaction_id=result.transaction_id,
            status=result.status,
            created_at=result.created_at,
        )

    return router
