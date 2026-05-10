from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock, patch

from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from adapters.messaging.rabbitmq_saga_consumer import RabbitMQSagaConsumer
from domain.events import PaymentConfirmed


def test_rabbitmq_event_publisher_publishes_payment_confirmed():
    channel = Mock()
    connection = Mock()
    connection.channel.return_value = channel

    with patch(
        "adapters.messaging.rabbitmq_event_publisher.pika.BlockingConnection",
        return_value=connection,
    ):
        publisher = RabbitMQEventPublisher("amqp://guest:guest@localhost:5672/%2F")
        publisher.publish_payment_confirmed(
            PaymentConfirmed(
                transaction_id="transaction-1",
                customer_id="customer-1",
                account_id="account-1",
                amount=Decimal("10.00"),
                confirmed_at=datetime.now(timezone.utc),
            )
        )

    channel.exchange_declare.assert_called_once_with(
        exchange="payments",
        exchange_type="topic",
        durable=True,
    )
    assert channel.basic_publish.call_args.kwargs["exchange"] == "payments"
    assert channel.basic_publish.call_args.kwargs["routing_key"] == "payment.confirmed"
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


def test_rabbitmq_saga_consumer_parses_debit_completed_payload():
    payload = {
        "transaction_id": "transaction-1",
        "account_id": "account-1",
        "customer_id": "customer-1",
        "amount": "10.00",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
    }

    message = RabbitMQSagaConsumer._debit_completed_from_payload(payload)

    assert message.transaction_id == "transaction-1"
    assert message.account_id == "account-1"
    assert message.amount == Decimal("10.00")
