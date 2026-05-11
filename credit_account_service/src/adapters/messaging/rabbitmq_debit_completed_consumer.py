import json
from datetime import datetime
from decimal import Decimal

import pika

from observability.messaging import begin_message

from adapters.messaging.debit_completed_handler import (
    DebitCompletedHandler,
    DebitCompletedMessage,
)


class RabbitMQDebitCompletedConsumer:
    def __init__(
        self,
        rabbitmq_url: str,
        handler: DebitCompletedHandler,
        exchange_name: str = "payments",
        queue_name: str = "credit_account.debit_completed",
    ) -> None:
        self.rabbitmq_url = rabbitmq_url
        self.handler = handler
        self.exchange_name = exchange_name
        self.queue_name = queue_name

    def start(self) -> None:
        parameters = pika.URLParameters(self.rabbitmq_url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type="topic",
            durable=True,
        )
        channel.queue_declare(queue=self.queue_name, durable=True)
        channel.queue_bind(
            exchange=self.exchange_name,
            queue=self.queue_name,
            routing_key="debit.completed",
        )
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._handle_message,
        )
        channel.start_consuming()

    def _handle_message(self, channel, method, properties, body) -> None:
        try:
            payload = json.loads(body.decode("utf-8"))
            begin_message(payload, method.routing_key)
            self.handler.handle(self._message_from_payload(payload))
        except Exception:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            raise
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def _message_from_payload(payload: dict[str, str]) -> DebitCompletedMessage:
        return DebitCompletedMessage(
            transaction_id=payload["transaction_id"],
            account_id=payload["account_id"],
            customer_id=payload["customer_id"],
            merchant_id=payload["merchant_id"],
            amount=Decimal(payload["amount"]),
            occurred_at=datetime.fromisoformat(payload["occurred_at"]),
        )
