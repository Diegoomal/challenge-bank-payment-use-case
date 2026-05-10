from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from application.ports.for_debiting_account import ForDebitingAccount
from application.schemas import DebitAccountCommand, DebitAccountResult


@dataclass(frozen=True)
class PaymentStartedMessage:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    payment_method: str
    occurred_at: datetime


class PaymentStartedHandler:
    def __init__(self, debit_account: ForDebitingAccount) -> None:
        self.debit_account = debit_account

    def handle(self, message: PaymentStartedMessage) -> DebitAccountResult:
        return self.debit_account.debit_account(
            DebitAccountCommand(
                transaction_id=message.transaction_id,
                customer_id=message.customer_id,
                amount=message.amount,
            )
        )
