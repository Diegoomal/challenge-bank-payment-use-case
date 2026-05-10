import json
from datetime import datetime
from decimal import Decimal

import pika

from observability.messaging import begin_message

from adapters.messaging.saga_event_handler import (
    PaymentConfirmedMessage,
    SagaEventHandler,
)
from domain.notification_channel import NotificationChannel


class RabbitMQSagaConsumer:
    def __init__(
        self,
        rabbitmq_url: str,
        handler: SagaEventHandler,
        exchange_name: str = "payments",
        queue_name: str = "notify_customer.saga_events",
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
            routing_key="payment.confirmed",
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
            if method.routing_key == "payment.confirmed":
                self.handler.handle_payment_confirmed(
                    self._payment_confirmed_from_payload(payload)
                )
        except Exception:
            channel.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            raise
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def _payment_confirmed_from_payload(
        payload: dict[str, str],
    ) -> PaymentConfirmedMessage:
        return PaymentConfirmedMessage(
            transaction_id=payload["transaction_id"],
            customer_id=payload["customer_id"],
            merchant_id=payload["merchant_id"],
            amount=Decimal(payload["amount"]),
            confirmed_at=datetime.fromisoformat(payload["confirmed_at"]),
            recipient=payload.get("recipient"),
            channel=NotificationChannel(payload.get("channel", "PUSH")),
        )
