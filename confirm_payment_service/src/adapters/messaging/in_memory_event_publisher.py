from application.ports.event_publisher import EventPublisher
from domain.events import PaymentConfirmed


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.confirmed_events: list[PaymentConfirmed] = []

    def publish_payment_confirmed(self, event: PaymentConfirmed) -> None:
        self.confirmed_events.append(event)
