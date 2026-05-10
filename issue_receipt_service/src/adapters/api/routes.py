from fastapi import APIRouter, HTTPException, status

from adapters.api.schemas import IssueReceiptRequest, IssueReceiptResponse
from application.ports.for_issuing_receipt import ForIssuingReceipt
from application.schemas import IssueReceiptCommand


def create_receipt_router(issue_receipt: ForIssuingReceipt) -> APIRouter:
    router = APIRouter(prefix="/receipts", tags=["receipts"])

    @router.post(
        "",
        response_model=IssueReceiptResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def issue_receipt_endpoint(request: IssueReceiptRequest) -> IssueReceiptResponse:
        try:
            result = issue_receipt.issue_receipt(
                IssueReceiptCommand(
                    transaction_id=request.transaction_id,
                    customer_id=request.customer_id,
                    merchant_id=request.merchant_id,
                    amount=request.amount,
                    confirmed_at=request.confirmed_at,
                )
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
            ) from error

        return IssueReceiptResponse(
            receipt_id=result.receipt_id,
            transaction_id=result.transaction_id,
            status=result.status,
            issued_at=result.issued_at,
        )

    return router


create_payment_router = create_receipt_router
