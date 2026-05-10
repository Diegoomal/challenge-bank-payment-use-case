from datetime import datetime, timezone
from decimal import Decimal

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.notification.in_memory_notification_gateway import (
    InMemoryNotificationGateway,
)
from application.schemas import NotifyCustomerCommand
from application.services.notify_customer_service import NotifyCustomerService
from domain.delivery_status import DeliveryStatus
from domain.notification_channel import NotificationChannel


class InMemoryNotificationRepository:
    def __init__(self):
        self.notifications = {}

    def save(self, notification):
        self.notifications[notification.id] = notification

    def get_by_id(self, notification_id):
        return self.notifications.get(notification_id)

    def get_by_transaction_and_customer(self, transaction_id, customer_id):
        return next(
            (
                notification
                for notification in self.notifications.values()
                if notification.transaction_id == transaction_id
                and notification.customer_id == customer_id
            ),
            None,
        )


class FailingNotificationGateway:
    def send(self, notification):
        raise RuntimeError("delivery failed")


def test_notify_customer_delivers_notification_and_publishes_event():
    repository = InMemoryNotificationRepository()
    gateway = InMemoryNotificationGateway()
    publisher = InMemoryEventPublisher()
    service = NotifyCustomerService(repository, gateway, publisher)

    result = service.notify_customer(
        NotifyCustomerCommand(
            transaction_id="transaction-1",
            merchant_id="merchant-1",
            customer_id="customer-1",
            amount=Decimal("50.00"),
            confirmed_at=datetime.now(timezone.utc),
            recipient="customer@example.com",
            channel=NotificationChannel.EMAIL,
        )
    )

    assert result.status == DeliveryStatus.DELIVERED
    assert result.notified_at is not None
    assert len(gateway.sent_notifications) == 1
    assert len(publisher.customer_notified_events) == 1
    assert publisher.customer_notified_events[0].event_name == "CustomerNotified"


def test_notify_customer_is_idempotent_when_already_delivered():
    repository = InMemoryNotificationRepository()
    gateway = InMemoryNotificationGateway()
    publisher = InMemoryEventPublisher()
    service = NotifyCustomerService(repository, gateway, publisher)
    command = NotifyCustomerCommand(
        transaction_id="transaction-1",
        merchant_id="merchant-1",
        customer_id="customer-1",
        amount=Decimal("50.00"),
        confirmed_at=datetime.now(timezone.utc),
        recipient="customer@example.com",
    )

    first = service.notify_customer(command)
    second = service.notify_customer(command)

    assert second.notification_id == first.notification_id
    assert len(gateway.sent_notifications) == 1
    assert len(publisher.customer_notified_events) == 1


def test_notify_customer_records_failure_without_publishing_event():
    repository = InMemoryNotificationRepository()
    publisher = InMemoryEventPublisher()
    service = NotifyCustomerService(repository, FailingNotificationGateway(), publisher)

    result = service.notify_customer(
        NotifyCustomerCommand(
            transaction_id="transaction-1",
            merchant_id="merchant-1",
            customer_id="customer-1",
            amount=Decimal("50.00"),
            confirmed_at=datetime.now(timezone.utc),
            recipient="customer@example.com",
        )
    )

    assert result.status == DeliveryStatus.FAILED
    assert publisher.customer_notified_events == []
