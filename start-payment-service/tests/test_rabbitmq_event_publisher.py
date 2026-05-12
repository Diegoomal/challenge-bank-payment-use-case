from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock, patch

from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from domain.events import PaymentStarted
from domain.payment_method import PaymentMethod


def test_rabbitmq_event_publisher_publishes_payment_started():
    channel = Mock()
    connection = Mock()
    connection.channel.return_value = channel

    with patch(
        "adapters.messaging.rabbitmq_event_publisher.pika.BlockingConnection",
        return_value=connection,
    ):
        publisher = RabbitMQEventPublisher("amqp://guest:guest@localhost:5672/%2F")
        publisher.publish_payment_started(
            PaymentStarted(
                transaction_id="transaction-1",
                customer_id="customer-1",
                merchant_id="merchant-1",
                amount=Decimal("10.00"),
                payment_method=PaymentMethod.ACCOUNT_BALANCE,
                occurred_at=datetime.now(timezone.utc),
            )
        )

    channel.exchange_declare.assert_called_once_with(
        exchange="payments",
        exchange_type="topic",
        durable=True,
    )
    assert channel.basic_publish.call_args.kwargs["exchange"] == "payments"
    assert channel.basic_publish.call_args.kwargs["routing_key"] == "payment.started"
    connection.close.assert_called_once()
