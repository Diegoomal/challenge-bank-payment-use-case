from typing import Protocol

from domain.receipt import Receipt


class ReceiptGenerator(Protocol):
    def generate(self, receipt: Receipt) -> str:
        pass
