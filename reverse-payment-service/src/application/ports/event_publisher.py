from typing import Protocol

from domain.events import PaymentReversed


class EventPublisher(Protocol):
    def publish_payment_reversed(self, event: PaymentReversed) -> None:
        pass
