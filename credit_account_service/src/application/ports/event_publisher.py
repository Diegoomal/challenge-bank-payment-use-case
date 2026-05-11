from typing import Protocol

from domain.events import CreditCompleted, CreditFailed


class EventPublisher(Protocol):
    def publish_credit_completed(self, event: CreditCompleted) -> None:
        pass

    def publish_credit_failed(self, event: CreditFailed) -> None:
        pass
