import os

from fastapi import FastAPI

from adapters.api.routes import create_notification_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from adapters.messaging.rabbitmq_saga_consumer import RabbitMQSagaConsumer
from adapters.messaging.saga_event_handler import SagaEventHandler
from adapters.notification.in_memory_notification_gateway import (
    InMemoryNotificationGateway,
)
from adapters.persistence.sqlite_notification_repository import SQLiteNotificationRepository
from application.ports.event_publisher import EventPublisher
from application.ports.for_notifying_merchant import ForNotifyingMerchant
from application.services.notify_merchant_service import NotifyMerchantService


def configure_event_publisher(rabbitmq_url: str | None = None) -> EventPublisher:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if rabbitmq_url:
        return RabbitMQEventPublisher(rabbitmq_url)
    return InMemoryEventPublisher()


def configure_notify_merchant(
    database_path: str = "notify_merchant.db",
    rabbitmq_url: str | None = None,
) -> ForNotifyingMerchant:
    repository = SQLiteNotificationRepository(database_path)
    notification_gateway = InMemoryNotificationGateway()
    event_publisher = configure_event_publisher(rabbitmq_url)
    return NotifyMerchantService(repository, notification_gateway, event_publisher)


def create_saga_event_handler(
    database_path: str = "notify_merchant.db",
    rabbitmq_url: str | None = None,
) -> SagaEventHandler:
    repository = SQLiteNotificationRepository(database_path)
    return SagaEventHandler(
        notify_merchant=NotifyMerchantService(
            repository,
            InMemoryNotificationGateway(),
            configure_event_publisher(rabbitmq_url),
        ),
    )


def create_saga_consumer(
    database_path: str = "notify_merchant.db",
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
    database_path: str = "notify_merchant.db",
    rabbitmq_url: str | None = None,
) -> FastAPI:
    app = FastAPI(title="Notify Merchant Service")
    app.include_router(
        create_notification_router(configure_notify_merchant(database_path, rabbitmq_url))
    )
    return app
