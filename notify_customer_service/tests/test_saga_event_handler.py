from datetime import datetime, timezone
from decimal import Decimal

from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.saga_event_handler import (
    PaymentConfirmedMessage,
    SagaEventHandler,
)
from adapters.notification.in_memory_notification_gateway import (
    InMemoryNotificationGateway,
)
from application.services.notify_customer_service import NotifyCustomerService
from domain.delivery_status import DeliveryStatus


class InMemoryNotificationRepository:
    def __init__(self):
        self.notifications = {}

    def save(self, notification):
        self.notifications[notification.id] = notification

    def get_by_id(self, notification_id):
        return self.notifications.get(notification_id)

    def get_by_transaction_and_customer(self, transaction_id, customer_id):
        return next(
            (
                notification
                for notification in self.notifications.values()
                if notification.transaction_id == transaction_id
                and notification.customer_id == customer_id
            ),
            None,
        )


def test_saga_handler_notifies_customer_when_payment_is_confirmed():
    repository = InMemoryNotificationRepository()
    publisher = InMemoryEventPublisher()
    service = NotifyCustomerService(
        repository,
        InMemoryNotificationGateway(),
        publisher,
    )
    handler = SagaEventHandler(service)

    result = handler.handle_payment_confirmed(
        PaymentConfirmedMessage(
            transaction_id="transaction-1",
            customer_id="customer-1",
            merchant_id="merchant-1",
            amount=Decimal("50.00"),
            confirmed_at=datetime.now(timezone.utc),
        )
    )

    assert result.status == DeliveryStatus.DELIVERED
    assert len(publisher.customer_notified_events) == 1
