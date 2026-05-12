from datetime import datetime, timezone
from decimal import Decimal

import pytest

from domain.delivery_status import DeliveryStatus
from domain.notification import Notification
from domain.notification_channel import NotificationChannel
from domain.notification_type import NotificationType


def test_notification_can_be_created_for_confirmed_payment():
    notification = Notification.create_for_payment_confirmed(
        transaction_id="transaction-1",
        merchant_id="merchant-1",
        customer_id="customer-1",
        amount=Decimal("50.00"),
        recipient="merchant@example.com",
        channel=NotificationChannel.EMAIL,
    )

    assert notification.id
    assert notification.status == DeliveryStatus.PENDING
    assert notification.transaction_id == "transaction-1"
    assert notification.notification_type == NotificationType.PAYMENT_CONFIRMED


def test_notification_can_be_created_for_reversed_payment():
    notification = Notification.create_for_payment_reversed(
        transaction_id="transaction-1",
        merchant_id="merchant-1",
        customer_id="customer-1",
        amount=Decimal("50.00"),
        recipient="customer@example.com",
        channel=NotificationChannel.PUSH,
    )

    assert notification.id
    assert notification.status == DeliveryStatus.PENDING
    assert notification.notification_type == NotificationType.PAYMENT_REVERSED


def test_notification_can_be_marked_delivered():
    notification = Notification.create_for_payment_confirmed(
        transaction_id="transaction-1",
        merchant_id="merchant-1",
        customer_id="customer-1",
        amount=Decimal("50.00"),
        recipient="merchant@example.com",
        channel=NotificationChannel.EMAIL,
    )

    notified_at = notification.mark_delivered(datetime.now(timezone.utc))

    assert notification.status == DeliveryStatus.DELIVERED
    assert notification.notified_at == notified_at


def test_notification_can_be_marked_failed():
    notification = Notification.create_for_payment_confirmed(
        transaction_id="transaction-1",
        merchant_id="merchant-1",
        customer_id="customer-1",
        amount=Decimal("50.00"),
        recipient="merchant@example.com",
        channel=NotificationChannel.EMAIL,
    )

    notification.mark_failed("delivery failed")

    assert notification.status == DeliveryStatus.FAILED
    assert notification.failure_reason == "delivery failed"


def test_notification_requires_recipient():
    with pytest.raises(ValueError, match="recipient is required"):
        Notification.create_for_payment_confirmed(
            transaction_id="transaction-1",
            merchant_id="merchant-1",
            customer_id="customer-1",
            amount=Decimal("50.00"),
            recipient="",
            channel=NotificationChannel.EMAIL,
        )
