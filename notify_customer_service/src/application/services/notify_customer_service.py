from application.ports.event_publisher import EventPublisher
from application.ports.for_notifying_customer import ForNotifyingCustomer
from application.ports.notification_gateway import NotificationGateway
from application.ports.notification_repository import NotificationRepository
from application.schemas import NotifyCustomerCommand, NotifyCustomerResult
from domain.delivery_status import DeliveryStatus
from domain.events import CustomerNotified
from domain.notification import Notification
from domain.notification_type import NotificationType


class NotifyCustomerService(ForNotifyingCustomer):
    def __init__(
        self,
        notification_repository: NotificationRepository,
        notification_gateway: NotificationGateway,
        event_publisher: EventPublisher,
    ) -> None:
        self.notification_repository = notification_repository
        self.notification_gateway = notification_gateway
        self.event_publisher = event_publisher

    def notify_customer(
        self,
        command: NotifyCustomerCommand,
    ) -> NotifyCustomerResult:
        notification = self.notification_repository.get_by_transaction_and_customer(
            command.transaction_id,
            command.customer_id,
            command.notification_type,
        )
        if notification is not None and notification.status == DeliveryStatus.DELIVERED:
            return self._to_result(notification)

        if notification is None:
            notification = self._create_notification(command)

        try:
            self.notification_gateway.send(notification)
        except Exception as error:
            notification.mark_failed(str(error))
            self.notification_repository.save(notification)
            return self._to_result(notification)

        notified_at = notification.mark_delivered()
        self.notification_repository.save(notification)
        self.event_publisher.publish_customer_notified(
            CustomerNotified(
                notification_id=notification.id,
                transaction_id=notification.transaction_id,
                customer_id=notification.customer_id,
                notification_type=notification.notification_type.value,
                amount=notification.amount,
                channel=notification.channel.value,
                status=notification.status.value,
                notified_at=notified_at,
            )
        )
        return self._to_result(notification)

    def _create_notification(
        self,
        command: NotifyCustomerCommand,
    ) -> Notification:
        recipient = command.recipient or self._default_recipient(command.customer_id)
        if command.notification_type == NotificationType.PAYMENT_REVERSED:
            return Notification.create_for_payment_reversed(
                transaction_id=command.transaction_id,
                merchant_id=command.merchant_id,
                customer_id=command.customer_id,
                amount=command.amount,
                recipient=recipient,
                channel=command.channel,
            )
        return Notification.create_for_payment_confirmed(
            transaction_id=command.transaction_id,
            merchant_id=command.merchant_id,
            customer_id=command.customer_id,
            amount=command.amount,
            recipient=recipient,
            channel=command.channel,
        )

    @staticmethod
    def _default_recipient(customer_id: str) -> str:
        return f"{customer_id}@customer.local"

    @staticmethod
    def _to_result(notification: Notification) -> NotifyCustomerResult:
        return NotifyCustomerResult(
            notification_id=notification.id,
            transaction_id=notification.transaction_id,
            customer_id=notification.customer_id,
            notification_type=notification.notification_type,
            status=notification.status,
            notified_at=notification.notified_at,
        )
