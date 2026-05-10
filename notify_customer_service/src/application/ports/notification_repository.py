from typing import Protocol

from domain.notification import Notification


class NotificationRepository(Protocol):
    def save(self, notification: Notification) -> None:
        pass

    def get_by_id(self, notification_id: str) -> Notification | None:
        pass

    def get_by_transaction_and_customer(
        self,
        transaction_id: str,
        customer_id: str,
    ) -> Notification | None:
        pass
