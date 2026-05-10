from typing import Protocol

from application.schemas import DebitAccountCommand, DebitAccountResult


class ForDebitingAccount(Protocol):
    def debit_account(self, command: DebitAccountCommand) -> DebitAccountResult:
        pass
