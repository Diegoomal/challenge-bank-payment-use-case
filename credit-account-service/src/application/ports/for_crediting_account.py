from typing import Protocol

from application.schemas import CreditAccountCommand, CreditAccountResult


class ForCreditingAccount(Protocol):
    def credit_account(self, command: CreditAccountCommand) -> CreditAccountResult:
        pass
