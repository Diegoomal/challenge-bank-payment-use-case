from typing import Protocol

from domain.receipt import Receipt


class ReceiptRepository(Protocol):
    def save(self, receipt: Receipt) -> None:
        pass

    def get_by_id(self, receipt_id: str) -> Receipt | None:
        pass

    def get_by_transaction_id(self, transaction_id: str) -> Receipt | None:
        pass
