from fastapi import APIRouter, HTTPException, status

from adapters.api.schemas import NotifyCustomerRequest, NotifyCustomerResponse
from application.ports.for_notifying_customer import ForNotifyingCustomer
from application.schemas import NotifyCustomerCommand


def create_notification_router(notify_customer: ForNotifyingCustomer) -> APIRouter:
    router = APIRouter(prefix="/notifications", tags=["notifications"])

    @router.post("/customer", response_model=NotifyCustomerResponse)
    def notify_customer_endpoint(
        request: NotifyCustomerRequest,
    ) -> NotifyCustomerResponse:
        try:
            result = notify_customer.notify_customer(
                NotifyCustomerCommand(
                    transaction_id=request.transaction_id,
                    merchant_id=request.merchant_id,
                    customer_id=request.customer_id,
                    amount=request.amount,
                    confirmed_at=request.confirmed_at,
                    recipient=request.recipient,
                    channel=request.channel,
                )
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error
        return NotifyCustomerResponse(
            notification_id=result.notification_id,
            transaction_id=result.transaction_id,
            customer_id=result.customer_id,
            status=result.status,
            notified_at=result.notified_at,
        )

    return router
