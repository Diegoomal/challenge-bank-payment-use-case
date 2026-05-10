import json

import pika

from application.ports.event_publisher import EventPublisher
from domain.events import PaymentReversed


class RabbitMQEventPublisher(EventPublisher):
    def __init__(self, rabbitmq_url: str, exchange_name: str = "payments") -> None:
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name

    def publish_payment_reversed(self, event: PaymentReversed) -> None:
        parameters = pika.URLParameters(self.rabbitmq_url)
        connection = pika.BlockingConnection(parameters)
        try:
            channel = connection.channel()
            channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type="topic",
                durable=True,
            )
            channel.basic_publish(
                exchange=self.exchange_name,
                routing_key="payment.reversed",
                body=json.dumps(event.to_payload()).encode("utf-8"),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=pika.DeliveryMode.Persistent,
                ),
            )
        finally:
            connection.close()
