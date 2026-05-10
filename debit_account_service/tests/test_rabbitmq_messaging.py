from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock, patch

from adapters.messaging.payment_started_handler import PaymentStartedMessage
from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from adapters.messaging.rabbitmq_payment_started_consumer import (
    RabbitMQPaymentStartedConsumer,
)
from domain.events import DebitCompleted, DebitFailed


def test_rabbitmq_event_publisher_publishes_debit_completed():
    channel = Mock()
    connection = Mock()
    connection.channel.return_value = channel

    with patch(
        "adapters.messaging.rabbitmq_event_publisher.pika.BlockingConnection",
        return_value=connection,
    ):
        publisher = RabbitMQEventPublisher("amqp://guest:guest@localhost:5672/%2F")
        publisher.publish_debit_completed(
            DebitCompleted(
                transaction_id="transaction-1",
                account_id="account-1",
                customer_id="customer-1",
                amount=Decimal("10.00"),
                occurred_at=datetime.now(timezone.utc),
            )
        )

    assert channel.basic_publish.call_args.kwargs["exchange"] == "payments"
    assert channel.basic_publish.call_args.kwargs["routing_key"] == "debit.completed"
    connection.close.assert_called_once()


def test_rabbitmq_event_publisher_publishes_debit_failed():
    channel = Mock()
    connection = Mock()
    connection.channel.return_value = channel

    with patch(
        "adapters.messaging.rabbitmq_event_publisher.pika.BlockingConnection",
        return_value=connection,
    ):
        publisher = RabbitMQEventPublisher("amqp://guest:guest@localhost:5672/%2F")
        publisher.publish_debit_failed(
            DebitFailed(
                transaction_id="transaction-1",
                customer_id="customer-1",
                amount=Decimal("10.00"),
                reason="INSUFFICIENT_BALANCE",
                occurred_at=datetime.now(timezone.utc),
            )
        )

    assert channel.basic_publish.call_args.kwargs["routing_key"] == "debit.failed"


def test_rabbitmq_payment_started_consumer_parses_payload():
    payload = {
        "transaction_id": "transaction-1",
        "customer_id": "customer-1",
        "merchant_id": "merchant-1",
        "amount": "10.00",
        "payment_method": "ACCOUNT_BALANCE",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
    }

    message = RabbitMQPaymentStartedConsumer._message_from_payload(payload)

    assert isinstance(message, PaymentStartedMessage)
    assert message.transaction_id == "transaction-1"
    assert message.customer_id == "customer-1"
    assert message.amount == Decimal("10.00")
