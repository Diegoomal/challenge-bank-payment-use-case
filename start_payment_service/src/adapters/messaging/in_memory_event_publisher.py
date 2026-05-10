from application.ports.event_publisher import EventPublisher
from domain.events import PaymentStarted


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.published_events: list[PaymentStarted] = []

    def publish_payment_started(self, event: PaymentStarted) -> None:
        self.published_events.append(event)
