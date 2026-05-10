from application.ports.event_publisher import EventPublisher
from application.ports.for_notifying_merchant import ForNotifyingMerchant
from application.ports.notification_gateway import NotificationGateway
from application.ports.notification_repository import NotificationRepository
from application.schemas import NotifyMerchantCommand, NotifyMerchantResult
from domain.delivery_status import DeliveryStatus
from domain.events import MerchantNotified
from domain.notification import Notification


class NotifyMerchantService(ForNotifyingMerchant):
    def __init__(
        self,
        notification_repository: NotificationRepository,
        notification_gateway: NotificationGateway,
        event_publisher: EventPublisher,
    ) -> None:
        self.notification_repository = notification_repository
        self.notification_gateway = notification_gateway
        self.event_publisher = event_publisher

    def notify_merchant(
        self,
        command: NotifyMerchantCommand,
    ) -> NotifyMerchantResult:
        notification = self.notification_repository.get_by_transaction_and_merchant(
            command.transaction_id,
            command.merchant_id,
        )
        if notification is not None and notification.status == DeliveryStatus.DELIVERED:
            return self._to_result(notification)

        if notification is None:
            notification = Notification.create_for_payment_confirmed(
                transaction_id=command.transaction_id,
                merchant_id=command.merchant_id,
                customer_id=command.customer_id,
                amount=command.amount,
                recipient=command.recipient or self._default_recipient(
                    command.merchant_id
                ),
                channel=command.channel,
            )

        try:
            self.notification_gateway.send(notification)
        except Exception as error:
            notification.mark_failed(str(error))
            self.notification_repository.save(notification)
            return self._to_result(notification)

        notified_at = notification.mark_delivered()
        self.notification_repository.save(notification)
        self.event_publisher.publish_merchant_notified(
            MerchantNotified(
                notification_id=notification.id,
                transaction_id=notification.transaction_id,
                merchant_id=notification.merchant_id,
                amount=notification.amount,
                channel=notification.channel.value,
                status=notification.status.value,
                notified_at=notified_at,
            )
        )
        return self._to_result(notification)

    @staticmethod
    def _default_recipient(merchant_id: str) -> str:
        return f"{merchant_id}@merchant.local"

    @staticmethod
    def _to_result(notification: Notification) -> NotifyMerchantResult:
        return NotifyMerchantResult(
            notification_id=notification.id,
            transaction_id=notification.transaction_id,
            merchant_id=notification.merchant_id,
            status=notification.status,
            notified_at=notification.notified_at,
        )
