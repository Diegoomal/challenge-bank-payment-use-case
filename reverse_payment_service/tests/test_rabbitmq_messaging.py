from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock, patch

from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from adapters.messaging.rabbitmq_saga_consumer import RabbitMQSagaConsumer
from domain.events import PaymentReversed


def test_rabbitmq_event_publisher_publishes_payment_reversed():
    channel = Mock()
    connection = Mock()
    connection.channel.return_value = channel

    with patch(
        "adapters.messaging.rabbitmq_event_publisher.pika.BlockingConnection",
        return_value=connection,
    ):
        publisher = RabbitMQEventPublisher("amqp://guest:guest@localhost:5672/%2F")
        publisher.publish_payment_reversed(
            PaymentReversed(
                transaction_id="transaction-1",
                customer_id="customer-1",
                amount=Decimal("10.00"),
                reason="INSUFFICIENT_BALANCE",
                reversed_at=datetime.now(timezone.utc),
            )
        )

    assert channel.basic_publish.call_args.kwargs["exchange"] == "payments"
    assert channel.basic_publish.call_args.kwargs["routing_key"] == "payment.reversed"
    connection.close.assert_called_once()


def test_rabbitmq_saga_consumer_parses_payment_started_payload():
    payload = {
        "transaction_id": "transaction-1",
        "customer_id": "customer-1",
        "merchant_id": "merchant-1",
        "amount": "10.00",
        "payment_method": "ACCOUNT_BALANCE",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
    }

    message = RabbitMQSagaConsumer._payment_started_from_payload(payload)

    assert message.transaction_id == "transaction-1"
    assert message.amount == Decimal("10.00")


def test_rabbitmq_saga_consumer_parses_debit_failed_payload():
    payload = {
        "transaction_id": "transaction-1",
        "customer_id": "customer-1",
        "amount": "10.00",
        "reason": "INSUFFICIENT_BALANCE",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
    }

    message = RabbitMQSagaConsumer._debit_failed_from_payload(payload)

    assert message.transaction_id == "transaction-1"
    assert message.reason == "INSUFFICIENT_BALANCE"
    assert message.amount == Decimal("10.00")
