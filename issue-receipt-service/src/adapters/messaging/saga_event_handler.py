from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from application.ports.for_issuing_receipt import ForIssuingReceipt
from application.schemas import IssueReceiptCommand, IssueReceiptResult


@dataclass(frozen=True)
class PaymentConfirmedMessage:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    confirmed_at: datetime


class SagaEventHandler:
    def __init__(self, issue_receipt: ForIssuingReceipt) -> None:
        self.issue_receipt = issue_receipt

    def handle_payment_confirmed(
        self,
        message: PaymentConfirmedMessage,
    ) -> IssueReceiptResult:
        return self.issue_receipt.issue_receipt(
            IssueReceiptCommand(
                transaction_id=message.transaction_id,
                customer_id=message.customer_id,
                merchant_id=message.merchant_id,
                amount=message.amount,
                confirmed_at=message.confirmed_at,
            )
        )
