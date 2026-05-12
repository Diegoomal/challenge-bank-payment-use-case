from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock, patch

from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from adapters.messaging.rabbitmq_saga_consumer import RabbitMQSagaConsumer
from domain.events import MerchantNotified
from domain.notification_channel import NotificationChannel


def test_rabbitmq_event_publisher_publishes_merchant_notified():
    channel = Mock()
    connection = Mock()
    connection.channel.return_value = channel

    with patch(
        "adapters.messaging.rabbitmq_event_publisher.pika.BlockingConnection",
        return_value=connection,
    ):
        publisher = RabbitMQEventPublisher("amqp://guest:guest@localhost:5672/%2F")
        publisher.publish_merchant_notified(
            MerchantNotified(
                notification_id="notification-1",
                transaction_id="transaction-1",
                merchant_id="merchant-1",
                amount=Decimal("10.00"),
                channel="WEBHOOK",
                status="DELIVERED",
                notified_at=datetime.now(timezone.utc),
            )
        )

    assert channel.basic_publish.call_args.kwargs["exchange"] == "payments"
    assert channel.basic_publish.call_args.kwargs["routing_key"] == "merchant.notified"
    connection.close.assert_called_once()


def test_rabbitmq_saga_consumer_parses_payment_confirmed_payload():
    payload = {
        "transaction_id": "transaction-1",
        "customer_id": "customer-1",
        "merchant_id": "merchant-1",
        "amount": "10.00",
        "confirmed_at": datetime.now(timezone.utc).isoformat(),
        "recipient": "https://merchant.example/webhook",
        "channel": "WEBHOOK",
    }

    message = RabbitMQSagaConsumer._payment_confirmed_from_payload(payload)

    assert message.transaction_id == "transaction-1"
    assert message.merchant_id == "merchant-1"
    assert message.amount == Decimal("10.00")
    assert message.channel == NotificationChannel.WEBHOOK
