from typing import Protocol

from application.schemas import StartPaymentCommand, StartPaymentResult


class ForStartingPayment(Protocol):
    def start_payment(self, command: StartPaymentCommand) -> StartPaymentResult:
        pass
