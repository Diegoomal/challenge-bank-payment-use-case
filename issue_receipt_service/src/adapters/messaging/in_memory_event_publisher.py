from application.ports.event_publisher import EventPublisher
from domain.events import ReceiptIssued


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.issued_events: list[ReceiptIssued] = []

    def publish_receipt_issued(self, event: ReceiptIssued) -> None:
        self.issued_events.append(event)

    @property
    def published_events(self) -> list[ReceiptIssued]:
        return self.issued_events

    def publish_payment_started(self, event: ReceiptIssued) -> None:
        self.publish_receipt_issued(event)
