from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from application.ports.for_confirming_payment import ForConfirmingPayment
from application.ports.transaction_repository import TransactionRepository
from application.schemas import ConfirmPaymentCommand, ConfirmPaymentResult
from domain.transaction import Transaction


@dataclass(frozen=True)
class PaymentStartedMessage:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    payment_method: str
    occurred_at: datetime


@dataclass(frozen=True)
class DebitCompletedMessage:
    transaction_id: str
    account_id: str
    customer_id: str
    amount: Decimal
    occurred_at: datetime


class SagaEventHandler:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        confirm_payment: ForConfirmingPayment,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.confirm_payment = confirm_payment

    def handle_payment_started(self, message: PaymentStartedMessage) -> None:
        if self.transaction_repository.get_by_id(message.transaction_id) is None:
            self.transaction_repository.save(
                Transaction.start(message.transaction_id, message.merchant_id)
            )

    def handle_debit_completed(
        self,
        message: DebitCompletedMessage,
    ) -> ConfirmPaymentResult:
        return self.confirm_payment.confirm_payment(
            ConfirmPaymentCommand(
                transaction_id=message.transaction_id,
                account_id=message.account_id,
                customer_id=message.customer_id,
                amount=message.amount,
                occurred_at=message.occurred_at,
            )
        )
