from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from adapters.messaging.payment_started_handler import (
    PaymentStartedHandler,
    PaymentStartedMessage,
)
from domain.debit_status import DebitStatus


@dataclass
class FakeDebitAccount:
    command: object = None

    def debit_account(self, command):
        self.command = command
        return object()


def test_payment_started_handler_converts_event_to_debit_command():
    debit_account = FakeDebitAccount()
    handler = PaymentStartedHandler(debit_account)

    handler.handle(
        PaymentStartedMessage(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            payment_method="ACCOUNT_BALANCE",
            occurred_at=datetime.now(timezone.utc),
        )
    )

    assert debit_account.command.transaction_id == "transaction-1"
    assert debit_account.command.customer_id == "customer-1"
    assert debit_account.command.merchant_id == "merchant-1"
    assert debit_account.command.amount == Decimal("50.00")


def test_payment_started_handler_returns_debit_result():
    class CompletedDebitAccount:
        def debit_account(self, command):
            return DebitStatus.COMPLETED

    handler = PaymentStartedHandler(CompletedDebitAccount())

    result = handler.handle(
        PaymentStartedMessage(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            payment_method="ACCOUNT_BALANCE",
            occurred_at=datetime.now(timezone.utc),
        )
    )

    assert result == DebitStatus.COMPLETED
