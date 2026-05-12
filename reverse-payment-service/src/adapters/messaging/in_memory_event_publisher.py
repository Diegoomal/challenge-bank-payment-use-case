from application.ports.event_publisher import EventPublisher
from domain.events import PaymentReversed


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.reversed_events: list[PaymentReversed] = []

    def publish_payment_reversed(self, event: PaymentReversed) -> None:
        self.reversed_events.append(event)
