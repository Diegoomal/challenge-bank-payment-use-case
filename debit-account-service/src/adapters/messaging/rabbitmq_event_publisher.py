import json

import pika

from observability.messaging import build_message_properties, message_published

from application.ports.event_publisher import EventPublisher
from domain.events import DebitCompleted, DebitFailed


class RabbitMQEventPublisher(EventPublisher):
    def __init__(
        self,
        rabbitmq_url: str,
        exchange_name: str = "payments",
    ) -> None:
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name

    def publish_debit_completed(self, event: DebitCompleted) -> None:
        self._publish("debit.completed", event.to_payload())

    def publish_debit_failed(self, event: DebitFailed) -> None:
        self._publish("debit.failed", event.to_payload())

    def _publish(self, routing_key: str, payload: dict[str, str]) -> None:
        parameters = pika.URLParameters(self.rabbitmq_url)
        connection = pika.BlockingConnection(parameters)
        try:
            channel = connection.channel()
            channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type="topic",
                durable=True,
            )
            with message_published(routing_key, payload):
                channel.basic_publish(
                    exchange=self.exchange_name,
                    routing_key=routing_key,
                    body=json.dumps(payload).encode("utf-8"),
                    properties=build_message_properties(
                        payload,
                        content_type="application/json",
                        delivery_mode=pika.DeliveryMode.Persistent,
                    ),
                )
        finally:
            connection.close()
