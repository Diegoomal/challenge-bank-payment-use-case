from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.delivery_status import DeliveryStatus
from domain.notification_channel import NotificationChannel
from domain.notification_type import NotificationType


@dataclass(frozen=True)
class NotifyCustomerCommand:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    confirmed_at: datetime
    notification_type: NotificationType = NotificationType.PAYMENT_CONFIRMED
    recipient: str | None = None
    channel: NotificationChannel = NotificationChannel.PUSH


@dataclass(frozen=True)
class NotifyCustomerResult:
    notification_id: str
    transaction_id: str
    customer_id: str
    notification_type: NotificationType
    status: DeliveryStatus
    notified_at: datetime | None


NotifyMerchantCommand = NotifyCustomerCommand
NotifyMerchantResult = NotifyCustomerResult
