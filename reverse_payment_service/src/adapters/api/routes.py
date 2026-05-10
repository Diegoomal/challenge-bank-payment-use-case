from fastapi import APIRouter, HTTPException, status

from adapters.api.schemas import ReversePaymentRequest, ReversePaymentResponse
from application.ports.for_reversing_payment import ForReversingPayment
from application.schemas import ReversePaymentCommand


def create_payment_router(reverse_payment: ForReversingPayment) -> APIRouter:
    router = APIRouter(prefix="/payments", tags=["payments"])

    @router.post("/reverse", response_model=ReversePaymentResponse)
    def reverse_payment_endpoint(
        request: ReversePaymentRequest,
    ) -> ReversePaymentResponse:
        try:
            result = reverse_payment.reverse_payment(
                ReversePaymentCommand(
                    transaction_id=request.transaction_id,
                    customer_id=request.customer_id,
                    amount=request.amount,
                    reason=request.reason,
                    occurred_at=request.occurred_at,
                )
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        return ReversePaymentResponse(
            transaction_id=result.transaction_id,
            status=result.status,
            reversed_at=result.reversed_at,
            reason=result.reason,
        )

    return router
