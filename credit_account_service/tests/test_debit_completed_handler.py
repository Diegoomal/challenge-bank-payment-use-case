from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from adapters.messaging.debit_completed_handler import (
    DebitCompletedHandler,
    DebitCompletedMessage,
)
from domain.credit_status import CreditStatus


@dataclass
class FakeCreditAccount:
    command: object = None

    def credit_account(self, command):
        self.command = command
        return object()


def test_debit_completed_handler_converts_event_to_credit_command():
    credit_account = FakeCreditAccount()
    handler = DebitCompletedHandler(credit_account)

    handler.handle(
        DebitCompletedMessage(
            transaction_id="transaction-1",
            account_id="debit-account-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            occurred_at=datetime.now(timezone.utc),
        )
    )

    assert credit_account.command.transaction_id == "transaction-1"
    assert credit_account.command.customer_id == "customer-1"
    assert credit_account.command.merchant_id == "merchant-1"
    assert credit_account.command.amount == Decimal("50.00")


def test_debit_completed_handler_returns_credit_result():
    class CompletedCreditAccount:
        def credit_account(self, command):
            return CreditStatus.COMPLETED

    handler = DebitCompletedHandler(CompletedCreditAccount())

    result = handler.handle(
        DebitCompletedMessage(
            transaction_id="transaction-1",
            account_id="debit-account-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            occurred_at=datetime.now(timezone.utc),
        )
    )

    assert result == CreditStatus.COMPLETED
