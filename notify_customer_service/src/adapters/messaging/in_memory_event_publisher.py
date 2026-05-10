from application.ports.event_publisher import EventPublisher
from domain.events import CustomerNotified


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.customer_notified_events: list[CustomerNotified] = []

    def publish_customer_notified(self, event: CustomerNotified) -> None:
        self.customer_notified_events.append(event)

    @property
    def merchant_notified_events(self) -> list[CustomerNotified]:
        return self.customer_notified_events

    def publish_merchant_notified(self, event: CustomerNotified) -> None:
        self.publish_customer_notified(event)
