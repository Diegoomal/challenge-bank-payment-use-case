from typing import Protocol

from domain.events import CustomerNotified


class EventPublisher(Protocol):
    def publish_customer_notified(self, event: CustomerNotified) -> None:
        pass
