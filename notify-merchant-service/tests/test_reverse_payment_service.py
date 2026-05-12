from datetime import datetime, timezone
from decimal import Decimal

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.notification.in_memory_notification_gateway import (
    InMemoryNotificationGateway,
)
from application.schemas import NotifyMerchantCommand
from application.services.notify_merchant_service import NotifyMerchantService
from domain.delivery_status import DeliveryStatus
from domain.notification_channel import NotificationChannel


class InMemoryNotificationRepository:
    def __init__(self):
        self.notifications = {}

    def save(self, notification):
        self.notifications[notification.id] = notification

    def get_by_id(self, notification_id):
        return self.notifications.get(notification_id)

    def get_by_transaction_and_merchant(self, transaction_id, merchant_id):
        return next(
            (
                notification
                for notification in self.notifications.values()
                if notification.transaction_id == transaction_id
                and notification.merchant_id == merchant_id
            ),
            None,
        )


class FailingNotificationGateway:
    def send(self, notification):
        raise RuntimeError("delivery failed")


def test_notify_merchant_delivers_notification_and_publishes_event():
    repository = InMemoryNotificationRepository()
    gateway = InMemoryNotificationGateway()
    publisher = InMemoryEventPublisher()
    service = NotifyMerchantService(repository, gateway, publisher)

    result = service.notify_merchant(
        NotifyMerchantCommand(
            transaction_id="transaction-1",
            merchant_id="merchant-1",
            customer_id="customer-1",
            amount=Decimal("50.00"),
            confirmed_at=datetime.now(timezone.utc),
            recipient="merchant@example.com",
            channel=NotificationChannel.EMAIL,
        )
    )

    assert result.status == DeliveryStatus.DELIVERED
    assert result.notified_at is not None
    assert len(gateway.sent_notifications) == 1
    assert len(publisher.merchant_notified_events) == 1
    assert publisher.merchant_notified_events[0].event_name == "MerchantNotified"


def test_notify_merchant_is_idempotent_when_already_delivered():
    repository = InMemoryNotificationRepository()
    gateway = InMemoryNotificationGateway()
    publisher = InMemoryEventPublisher()
    service = NotifyMerchantService(repository, gateway, publisher)
    command = NotifyMerchantCommand(
        transaction_id="transaction-1",
        merchant_id="merchant-1",
        customer_id="customer-1",
        amount=Decimal("50.00"),
        confirmed_at=datetime.now(timezone.utc),
        recipient="merchant@example.com",
    )

    first = service.notify_merchant(command)
    second = service.notify_merchant(command)

    assert second.notification_id == first.notification_id
    assert len(gateway.sent_notifications) == 1
    assert len(publisher.merchant_notified_events) == 1


def test_notify_merchant_records_failure_without_publishing_event():
    repository = InMemoryNotificationRepository()
    publisher = InMemoryEventPublisher()
    service = NotifyMerchantService(repository, FailingNotificationGateway(), publisher)

    result = service.notify_merchant(
        NotifyMerchantCommand(
            transaction_id="transaction-1",
            merchant_id="merchant-1",
            customer_id="customer-1",
            amount=Decimal("50.00"),
            confirmed_at=datetime.now(timezone.utc),
            recipient="merchant@example.com",
        )
    )

    assert result.status == DeliveryStatus.FAILED
    assert publisher.merchant_notified_events == []
