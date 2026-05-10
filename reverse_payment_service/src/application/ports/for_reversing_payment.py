from typing import Protocol

from application.schemas import ReversePaymentCommand, ReversePaymentResult


class ForReversingPayment(Protocol):
    def reverse_payment(self, command: ReversePaymentCommand) -> ReversePaymentResult:
        pass
