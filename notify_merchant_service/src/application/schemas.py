from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.delivery_status import DeliveryStatus
from domain.notification_channel import NotificationChannel


@dataclass(frozen=True)
class NotifyMerchantCommand:
    transaction_id: str
    merchant_id: str
    customer_id: str
    amount: Decimal
    confirmed_at: datetime
    recipient: str | None = None
    channel: NotificationChannel = NotificationChannel.WEBHOOK


@dataclass(frozen=True)
class NotifyMerchantResult:
    notification_id: str
    transaction_id: str
    merchant_id: str
    status: DeliveryStatus
    notified_at: datetime | None
