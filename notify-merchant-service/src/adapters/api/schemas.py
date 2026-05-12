from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from domain.delivery_status import DeliveryStatus
from domain.notification_channel import NotificationChannel


class NotifyMerchantRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    merchant_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0)
    confirmed_at: datetime
    recipient: str | None = Field(default=None, min_length=1)
    channel: NotificationChannel = NotificationChannel.WEBHOOK


class NotifyMerchantResponse(BaseModel):
    notification_id: str
    transaction_id: str
    merchant_id: str
    status: DeliveryStatus
    notified_at: datetime | None
