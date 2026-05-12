from typing import Protocol

from domain.notification import Notification


class NotificationRepository(Protocol):
    def save(self, notification: Notification) -> None:
        pass

    def get_by_id(self, notification_id: str) -> Notification | None:
        pass

    def get_by_transaction_and_merchant(
        self,
        transaction_id: str,
        merchant_id: str,
    ) -> Notification | None:
        pass
