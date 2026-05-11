from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from application.ports.for_crediting_account import ForCreditingAccount
from application.schemas import CreditAccountCommand, CreditAccountResult


@dataclass(frozen=True)
class DebitCompletedMessage:
    transaction_id: str
    account_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    occurred_at: datetime


class DebitCompletedHandler:
    def __init__(self, credit_account: ForCreditingAccount) -> None:
        self.credit_account = credit_account

    def handle(self, message: DebitCompletedMessage) -> CreditAccountResult:
        return self.credit_account.credit_account(
            CreditAccountCommand(
                transaction_id=message.transaction_id,
                customer_id=message.customer_id,
                merchant_id=message.merchant_id,
                amount=message.amount,
            )
        )
