from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from domain.delivery_status import DeliveryStatus
from domain.notification_channel import NotificationChannel


@dataclass(frozen=True)
class NotifyCustomerCommand:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    confirmed_at: datetime
    recipient: str | None = None
    channel: NotificationChannel = NotificationChannel.PUSH


@dataclass(frozen=True)
class NotifyCustomerResult:
    notification_id: str
    transaction_id: str
    customer_id: str
    status: DeliveryStatus
    notified_at: datetime | None


NotifyMerchantCommand = NotifyCustomerCommand
NotifyMerchantResult = NotifyCustomerResult
