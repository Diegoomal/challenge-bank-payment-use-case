from typing import Protocol

from application.schemas import ConfirmPaymentCommand, ConfirmPaymentResult


class ForConfirmingPayment(Protocol):
    def confirm_payment(self, command: ConfirmPaymentCommand) -> ConfirmPaymentResult:
        pass
