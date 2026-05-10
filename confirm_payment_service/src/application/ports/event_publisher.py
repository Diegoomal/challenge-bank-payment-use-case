from typing import Protocol

from domain.events import PaymentConfirmed


class EventPublisher(Protocol):
    def publish_payment_confirmed(self, event: PaymentConfirmed) -> None:
        pass
