import json
from datetime import datetime
from decimal import Decimal

import pika

from adapters.messaging.payment_started_handler import (
    PaymentStartedHandler,
    PaymentStartedMessage,
)


class RabbitMQPaymentStartedConsumer:
    def __init__(
        self,
        rabbitmq_url: str,
        handler: PaymentStartedHandler,
        exchange_name: str = "payments",
        queue_name: str = "debit_account.payment_started",
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
            routing_key="payment.started",
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
            self.handler.handle(self._message_from_payload(payload))
        except Exception:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            raise
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def _message_from_payload(payload: dict[str, str]) -> PaymentStartedMessage:
        return PaymentStartedMessage(
            transaction_id=payload["transaction_id"],
            customer_id=payload["customer_id"],
            merchant_id=payload["merchant_id"],
            amount=Decimal(payload["amount"]),
            payment_method=payload["payment_method"],
            occurred_at=datetime.fromisoformat(payload["occurred_at"]),
        )
