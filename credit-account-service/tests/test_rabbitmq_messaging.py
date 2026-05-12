from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import Mock, patch

from adapters.messaging.debit_completed_handler import DebitCompletedMessage
from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from adapters.messaging.rabbitmq_debit_completed_consumer import (
    RabbitMQDebitCompletedConsumer,
)
from domain.events import CreditCompleted, CreditFailed


def test_rabbitmq_event_publisher_publishes_credit_completed():
    channel = Mock()
    connection = Mock()
    connection.channel.return_value = channel

    with patch(
        "adapters.messaging.rabbitmq_event_publisher.pika.BlockingConnection",
        return_value=connection,
    ):
        publisher = RabbitMQEventPublisher("amqp://guest:guest@localhost:5672/%2F")
        publisher.publish_credit_completed(
            CreditCompleted(
                transaction_id="transaction-1",
                account_id="account-1",
                customer_id="customer-1",
                merchant_id="merchant-1",
                amount=Decimal("10.00"),
                credited_at=datetime.now(timezone.utc),
            )
        )

    assert channel.basic_publish.call_args.kwargs["exchange"] == "payments"
    assert channel.basic_publish.call_args.kwargs["routing_key"] == "credit.completed"
    connection.close.assert_called_once()


def test_rabbitmq_event_publisher_publishes_credit_failed():
    channel = Mock()
    connection = Mock()
    connection.channel.return_value = channel

    with patch(
        "adapters.messaging.rabbitmq_event_publisher.pika.BlockingConnection",
        return_value=connection,
    ):
        publisher = RabbitMQEventPublisher("amqp://guest:guest@localhost:5672/%2F")
        publisher.publish_credit_failed(
            CreditFailed(
                transaction_id="transaction-1",
                customer_id="customer-1",
                merchant_id="merchant-1",
                amount=Decimal("10.00"),
                reason="MERCHANT_ACCOUNT_NOT_FOUND",
                failed_at=datetime.now(timezone.utc),
            )
        )

    assert channel.basic_publish.call_args.kwargs["routing_key"] == "credit.failed"


def test_rabbitmq_debit_completed_consumer_parses_payload():
    payload = {
        "transaction_id": "transaction-1",
        "account_id": "debit-account-1",
        "customer_id": "customer-1",
        "merchant_id": "merchant-1",
        "amount": "10.00",
        "occurred_at": datetime.now(timezone.utc).isoformat(),
    }

    message = RabbitMQDebitCompletedConsumer._message_from_payload(payload)

    assert isinstance(message, DebitCompletedMessage)
    assert message.transaction_id == "transaction-1"
    assert message.customer_id == "customer-1"
    assert message.merchant_id == "merchant-1"
    assert message.amount == Decimal("10.00")
