from fastapi import APIRouter, HTTPException, status

from adapters.api.schemas import NotifyMerchantRequest, NotifyMerchantResponse
from application.ports.for_notifying_merchant import ForNotifyingMerchant
from application.schemas import NotifyMerchantCommand


def create_notification_router(notify_merchant: ForNotifyingMerchant) -> APIRouter:
    router = APIRouter(prefix="/notifications", tags=["notifications"])

    @router.post("/merchant", response_model=NotifyMerchantResponse)
    def notify_merchant_endpoint(
        request: NotifyMerchantRequest,
    ) -> NotifyMerchantResponse:
        try:
            result = notify_merchant.notify_merchant(
                NotifyMerchantCommand(
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
        return NotifyMerchantResponse(
            notification_id=result.notification_id,
            transaction_id=result.transaction_id,
            merchant_id=result.merchant_id,
            status=result.status,
            notified_at=result.notified_at,
        )

    return router
