from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from application.ports.for_notifying_customer import ForNotifyingCustomer
from application.schemas import NotifyCustomerCommand, NotifyCustomerResult
from domain.notification_channel import NotificationChannel
from domain.notification_type import NotificationType


@dataclass(frozen=True)
class PaymentConfirmedMessage:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    confirmed_at: datetime
    recipient: str | None = None
    channel: NotificationChannel = NotificationChannel.PUSH


@dataclass(frozen=True)
class PaymentReversedMessage:
    transaction_id: str
    customer_id: str
    merchant_id: str
    amount: Decimal
    reason: str
    reversed_at: datetime
    recipient: str | None = None
    channel: NotificationChannel = NotificationChannel.PUSH


class SagaEventHandler:
    def __init__(
        self,
        notify_customer: ForNotifyingCustomer,
    ) -> None:
        self.notify_customer = notify_customer

    def handle_payment_confirmed(
        self,
        message: PaymentConfirmedMessage,
    ) -> NotifyCustomerResult:
        return self.notify_customer.notify_customer(
            NotifyCustomerCommand(
                transaction_id=message.transaction_id,
                merchant_id=message.merchant_id,
                customer_id=message.customer_id,
                amount=message.amount,
                confirmed_at=message.confirmed_at,
                recipient=message.recipient,
                channel=message.channel,
            )
        )

    def handle_payment_reversed(
        self,
        message: PaymentReversedMessage,
    ) -> NotifyCustomerResult:
        return self.notify_customer.notify_customer(
            NotifyCustomerCommand(
                transaction_id=message.transaction_id,
                merchant_id=message.merchant_id,
                customer_id=message.customer_id,
                amount=message.amount,
                confirmed_at=message.reversed_at,
                notification_type=NotificationType.PAYMENT_REVERSED,
                recipient=message.recipient,
                channel=message.channel,
            )
        )
