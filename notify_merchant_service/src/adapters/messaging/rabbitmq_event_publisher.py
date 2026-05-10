import json

import pika

from application.ports.event_publisher import EventPublisher
from domain.events import MerchantNotified


class RabbitMQEventPublisher(EventPublisher):
    def __init__(self, rabbitmq_url: str, exchange_name: str = "payments") -> None:
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name

    def publish_merchant_notified(self, event: MerchantNotified) -> None:
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
                routing_key="merchant.notified",
                body=json.dumps(event.to_payload()).encode("utf-8"),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=pika.DeliveryMode.Persistent,
                ),
            )
        finally:
            connection.close()
