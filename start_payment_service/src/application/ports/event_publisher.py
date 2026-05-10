from typing import Protocol

from domain.events import PaymentStarted


class EventPublisher(Protocol):
    def publish_payment_started(self, event: PaymentStarted) -> None:
        pass
