from typing import Protocol

from domain.events import DebitCompleted, DebitFailed


class EventPublisher(Protocol):
    def publish_debit_completed(self, event: DebitCompleted) -> None:
        pass

    def publish_debit_failed(self, event: DebitFailed) -> None:
        pass
