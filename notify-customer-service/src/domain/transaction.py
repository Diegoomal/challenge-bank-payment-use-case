from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

from domain.delivery_status import DeliveryStatus
from domain.notification_channel import NotificationChannel
from domain.notification_type import NotificationType


@dataclass
class Notification:
    id: str
    transaction_id: str
    merchant_id: str
    customer_id: str
    amount: Decimal
    notification_type: NotificationType
    recipient: str
    channel: NotificationChannel
    status: DeliveryStatus
    created_at: datetime
    updated_at: datetime
    notified_at: datetime | None = None
    failure_reason: str | None = None

    @classmethod
    def create_for_payment_confirmed(
        cls,
        transaction_id: str,
        merchant_id: str,
        customer_id: str,
        amount: Decimal,
        recipient: str,
        channel: NotificationChannel,
    ) -> "Notification":
        return cls.create(
            transaction_id=transaction_id,
            merchant_id=merchant_id,
            customer_id=customer_id,
            amount=amount,
            notification_type=NotificationType.PAYMENT_CONFIRMED,
            recipient=recipient,
            channel=channel,
        )

    @classmethod
    def create_for_payment_reversed(
        cls,
        transaction_id: str,
        merchant_id: str,
        customer_id: str,
        amount: Decimal,
        recipient: str,
        channel: NotificationChannel,
    ) -> "Notification":
        return cls.create(
            transaction_id=transaction_id,
            merchant_id=merchant_id,
            customer_id=customer_id,
            amount=amount,
            notification_type=NotificationType.PAYMENT_REVERSED,
            recipient=recipient,
            channel=channel,
        )

    @classmethod
    def create(
        cls,
        transaction_id: str,
        merchant_id: str,
        customer_id: str,
        amount: Decimal,
        notification_type: NotificationType,
        recipient: str,
        channel: NotificationChannel,
    ) -> "Notification":
        cls._validate_required("transaction_id", transaction_id)
        cls._validate_required("merchant_id", merchant_id)
        cls._validate_required("customer_id", customer_id)
        cls._validate_required("recipient", recipient)
        if not isinstance(notification_type, NotificationType):
            raise ValueError("notification_type is invalid")
        if not isinstance(channel, NotificationChannel):
            raise ValueError("channel is invalid")

        now = datetime.now(timezone.utc)
        return cls(
            id=str(uuid4()),
            transaction_id=transaction_id,
            merchant_id=merchant_id,
            customer_id=customer_id,
            amount=amount,
            notification_type=notification_type,
            recipient=recipient,
            channel=channel,
            status=DeliveryStatus.PENDING,
            created_at=now,
            updated_at=now,
        )

    def mark_delivered(self, notified_at: datetime | None = None) -> datetime:
        notified_at = notified_at or datetime.now(timezone.utc)
        self.status = DeliveryStatus.DELIVERED
        self.notified_at = notified_at
        self.failure_reason = None
        self.updated_at = notified_at
        return notified_at

    def mark_failed(self, reason: str) -> None:
        self._validate_required("failure_reason", reason)
        now = datetime.now(timezone.utc)
        self.status = DeliveryStatus.FAILED
        self.failure_reason = reason
        self.updated_at = now

    @staticmethod
    def _validate_required(field_name: str, value: str) -> None:
        if not value or not value.strip():
            raise ValueError(f"{field_name} is required")


Transaction = Notification
