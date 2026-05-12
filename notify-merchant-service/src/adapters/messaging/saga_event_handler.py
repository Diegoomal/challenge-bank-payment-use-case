from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from application.ports.for_notifying_merchant import ForNotifyingMerchant
from application.schemas import NotifyMerchantCommand, NotifyMerchantResult
from domain.notification_channel import NotificationChannel


@dataclass(frozen=True)
class PaymentConfirmedMessage:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    confirmed_at: datetime
    recipient: str | None = None
    channel: NotificationChannel = NotificationChannel.WEBHOOK


class SagaEventHandler:
    def __init__(
        self,
        notify_merchant: ForNotifyingMerchant,
    ) -> None:
        self.notify_merchant = notify_merchant

    def handle_payment_confirmed(
        self,
        message: PaymentConfirmedMessage,
    ) -> NotifyMerchantResult:
        return self.notify_merchant.notify_merchant(
            NotifyMerchantCommand(
                transaction_id=message.transaction_id,
                merchant_id=message.merchant_id,
                customer_id=message.customer_id,
                amount=message.amount,
                confirmed_at=message.confirmed_at,
                recipient=message.recipient,
                channel=message.channel,
            )
        )
