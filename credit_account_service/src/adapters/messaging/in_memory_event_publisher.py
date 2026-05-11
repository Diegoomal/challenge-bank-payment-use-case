from application.ports.event_publisher import EventPublisher
from domain.events import CreditCompleted, CreditFailed


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.completed_events: list[CreditCompleted] = []
        self.failed_events: list[CreditFailed] = []

    def publish_credit_completed(self, event: CreditCompleted) -> None:
        self.completed_events.append(event)

    def publish_credit_failed(self, event: CreditFailed) -> None:
        self.failed_events.append(event)
