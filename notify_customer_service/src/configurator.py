import os

from fastapi import FastAPI
from observability.fastapi import configure_observability
from observability.logging import configure_logging

from adapters.api.routes import create_notification_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.outbox_event_publisher import OutboxEventPublisher
from adapters.messaging.rabbitmq_saga_consumer import RabbitMQSagaConsumer
from adapters.messaging.saga_event_handler import SagaEventHandler
from adapters.notification.in_memory_notification_gateway import (
    InMemoryNotificationGateway,
)
from adapters.persistence.sqlite_notification_repository import SQLiteNotificationRepository
from application.ports.event_publisher import EventPublisher
from application.ports.for_notifying_customer import ForNotifyingCustomer
from application.services.notify_customer_service import NotifyCustomerService


def configure_event_publisher(rabbitmq_url: str | None = None) -> EventPublisher:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if rabbitmq_url:
        return OutboxEventPublisher()
    return InMemoryEventPublisher()


def configure_notify_customer(
    database_path: str = "notify_customer.db",
    rabbitmq_url: str | None = None,
) -> ForNotifyingCustomer:
    repository = SQLiteNotificationRepository(database_path)
    notification_gateway = InMemoryNotificationGateway()
    event_publisher = configure_event_publisher(rabbitmq_url)
    return NotifyCustomerService(repository, notification_gateway, event_publisher)


def create_saga_event_handler(
    database_path: str = "notify_customer.db",
    rabbitmq_url: str | None = None,
) -> SagaEventHandler:
    repository = SQLiteNotificationRepository(database_path)
    return SagaEventHandler(
        notify_customer=NotifyCustomerService(
            repository,
            InMemoryNotificationGateway(),
            configure_event_publisher(rabbitmq_url),
        ),
    )


def create_saga_consumer(
    database_path: str = "notify_customer.db",
    rabbitmq_url: str | None = None,
) -> RabbitMQSagaConsumer:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if not rabbitmq_url:
        raise RuntimeError("RABBITMQ_URL is required to create the consumer")
    return RabbitMQSagaConsumer(
        rabbitmq_url=rabbitmq_url,
        handler=create_saga_event_handler(database_path, rabbitmq_url),
    )


def create_app(
    database_path: str = "notify_customer.db",
    rabbitmq_url: str | None = None,
) -> FastAPI:
    app = FastAPI(title="Notify Customer Service")
    configure_logging()
    configure_observability(app, os.getenv("OTEL_SERVICE_NAME", "Notify Customer Service".lower().replace(" ", "_")))
    app.include_router(
        create_notification_router(configure_notify_customer(database_path, rabbitmq_url))
    )
    return app


configure_notify_merchant = configure_notify_customer
