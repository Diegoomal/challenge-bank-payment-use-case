from typing import Protocol

from domain.events import AccountCreated


class EventPublisher(Protocol):
    def publish_account_created(self, event: AccountCreated) -> None:
        pass
