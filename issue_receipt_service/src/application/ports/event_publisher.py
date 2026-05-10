from typing import Protocol

from domain.events import ReceiptIssued


class EventPublisher(Protocol):
    def publish_receipt_issued(self, event: ReceiptIssued) -> None:
        pass
