from application.ports.event_publisher import EventPublisher
from domain.events import AccountCreated


class InMemoryEventPublisher(EventPublisher):
    def __init__(self) -> None:
        self.created_events: list[AccountCreated] = []

    def publish_account_created(self, event: AccountCreated) -> None:
        self.created_events.append(event)
