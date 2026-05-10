from application.ports.event_publisher import EventPublisher
from domain.events import MerchantNotified


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.merchant_notified_events: list[MerchantNotified] = []

    def publish_merchant_notified(self, event: MerchantNotified) -> None:
        self.merchant_notified_events.append(event)
