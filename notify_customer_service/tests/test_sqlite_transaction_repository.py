from decimal import Decimal

from adapters.persistence.sqlite_notification_repository import (
    SQLiteNotificationRepository,
)
from domain.delivery_status import DeliveryStatus
from domain.notification import Notification
from domain.notification_channel import NotificationChannel


def test_sqlite_notification_repository_saves_and_gets_notification(tmp_path):
    repository = SQLiteNotificationRepository(str(tmp_path / "notify.db"))
    notification = Notification.create_for_payment_confirmed(
        transaction_id="transaction-1",
        merchant_id="merchant-1",
        customer_id="customer-1",
        amount=Decimal("50.00"),
        recipient="merchant@example.com",
        channel=NotificationChannel.EMAIL,
    )
    notification.mark_delivered()

    repository.save(notification)

    saved = repository.get_by_id(notification.id)
    assert saved is not None
    assert saved.transaction_id == "transaction-1"
    assert saved.status == DeliveryStatus.DELIVERED
    assert saved.notified_at is not None


def test_sqlite_notification_repository_gets_by_transaction_and_customer(tmp_path):
    repository = SQLiteNotificationRepository(str(tmp_path / "notify.db"))
    notification = Notification.create_for_payment_confirmed(
        transaction_id="transaction-1",
        merchant_id="merchant-1",
        customer_id="customer-1",
        amount=Decimal("50.00"),
        recipient="customer@example.com",
        channel=NotificationChannel.EMAIL,
    )
    repository.save(notification)

    saved = repository.get_by_transaction_and_customer("transaction-1", "customer-1")

    assert saved is not None
    assert saved.id == notification.id


def test_sqlite_notification_repository_returns_none_when_not_found(tmp_path):
    repository = SQLiteNotificationRepository(str(tmp_path / "notify.db"))

    assert repository.get_by_id("missing") is None
