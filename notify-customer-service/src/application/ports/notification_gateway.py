from typing import Protocol

from domain.notification import Notification


class NotificationGateway(Protocol):
    def send(self, notification: Notification) -> None:
        pass
