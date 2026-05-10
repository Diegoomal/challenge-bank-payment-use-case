from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from application.ports.for_reversing_payment import ForReversingPayment
from application.ports.transaction_repository import TransactionRepository
from application.schemas import ReversePaymentCommand, ReversePaymentResult
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
class DebitFailedMessage:
    transaction_id: str
    customer_id: str
    amount: Decimal
    reason: str
    occurred_at: datetime


class SagaEventHandler:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        reverse_payment: ForReversingPayment,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.reverse_payment = reverse_payment

    def handle_payment_started(self, message: PaymentStartedMessage) -> None:
        if self.transaction_repository.get_by_id(message.transaction_id) is None:
            self.transaction_repository.save(Transaction.start(message.transaction_id))

    def handle_debit_failed(self, message: DebitFailedMessage) -> ReversePaymentResult:
        return self.reverse_payment.reverse_payment(
            ReversePaymentCommand(
                transaction_id=message.transaction_id,
                customer_id=message.customer_id,
                amount=message.amount,
                reason=message.reason,
                occurred_at=message.occurred_at,
            )
        )
