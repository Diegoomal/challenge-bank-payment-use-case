from domain.notification import Notification


class InMemoryNotificationGateway:
    def __init__(self) -> None:
        self.sent_notifications: list[Notification] = []

    def send(self, notification: Notification) -> None:
        self.sent_notifications.append(notification)
