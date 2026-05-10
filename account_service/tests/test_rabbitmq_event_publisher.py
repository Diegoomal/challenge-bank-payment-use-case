from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock, patch

from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from domain.events import AccountCreated


def test_rabbitmq_event_publisher_publishes_account_created():
    channel = Mock()
    connection = Mock()
    connection.channel.return_value = channel

    with patch(
        "adapters.messaging.rabbitmq_event_publisher.pika.BlockingConnection",
        return_value=connection,
    ):
        publisher = RabbitMQEventPublisher("amqp://guest:guest@localhost:5672/%2F")
        publisher.publish_account_created(
            AccountCreated(
                account_id="account-1",
                customer_id="customer-1",
                account_holder="Customer One",
                initial_deposit=Decimal("100.00"),
                occurred_at=datetime.now(timezone.utc),
            )
        )

    channel.exchange_declare.assert_called_once_with(
        exchange="accounts",
        exchange_type="topic",
        durable=True,
    )
    assert channel.basic_publish.call_args.kwargs["exchange"] == "accounts"
    assert channel.basic_publish.call_args.kwargs["routing_key"] == "account.created"
    connection.close.assert_called_once()
