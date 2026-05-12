from application.ports.event_publisher import EventPublisher
from domain.events import DebitCompleted, DebitFailed


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.completed_events: list[DebitCompleted] = []
        self.failed_events: list[DebitFailed] = []

    def publish_debit_completed(self, event: DebitCompleted) -> None:
        self.completed_events.append(event)

    def publish_debit_failed(self, event: DebitFailed) -> None:
        self.failed_events.append(event)
