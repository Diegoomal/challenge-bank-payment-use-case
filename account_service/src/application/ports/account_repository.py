from typing import Protocol

from domain.account import Account


class AccountRepository(Protocol):
    def save(self, account: Account) -> None:
        pass

    def get_by_customer_id(self, customer_id: str) -> Account | None:
        pass

    def has_active_account(self, customer_id: str) -> bool:
        pass
