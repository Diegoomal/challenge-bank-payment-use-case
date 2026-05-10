from typing import Protocol

from application.schemas import CreateAccountCommand, CreateAccountResult


class ForCreatingAccount(Protocol):
    def create_account(self, command: CreateAccountCommand) -> CreateAccountResult:
        pass
