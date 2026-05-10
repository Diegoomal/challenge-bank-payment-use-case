from typing import Protocol

from domain.transaction import Transaction


class TransactionRepository(Protocol):
    def save(self, transaction: Transaction) -> None:
        pass

    def get_by_id(self, transaction_id: str) -> Transaction | None:
        pass
