from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from domain.delivery_status import DeliveryStatus
from domain.notification_channel import NotificationChannel
from domain.notification_type import NotificationType


class NotifyCustomerRequest(BaseModel):
    transaction_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    merchant_id: str = Field(..., min_length=1)
    amount: Decimal = Field(..., gt=0)
    confirmed_at: datetime
    notification_type: NotificationType = NotificationType.PAYMENT_CONFIRMED
    recipient: str | None = Field(default=None, min_length=1)
    channel: NotificationChannel = NotificationChannel.PUSH


class NotifyCustomerResponse(BaseModel):
    notification_id: str
    transaction_id: str
    customer_id: str
    notification_type: NotificationType
    status: DeliveryStatus
    notified_at: datetime | None


NotifyMerchantRequest = NotifyCustomerRequest
NotifyMerchantResponse = NotifyCustomerResponse
