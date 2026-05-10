import os

from fastapi import FastAPI

from adapters.api.routes import create_account_router
from adapters.messaging.in_memory_event_publisher import InMemoryEventPublisher
from adapters.messaging.rabbitmq_event_publisher import RabbitMQEventPublisher
from adapters.persistence.sqlite_account_repository import SQLiteAccountRepository
from application.ports.event_publisher import EventPublisher
from application.ports.for_creating_account import ForCreatingAccount
from application.services.create_account_service import CreateAccountService


def configure_event_publisher(rabbitmq_url: str | None = None) -> EventPublisher:
    rabbitmq_url = rabbitmq_url or os.getenv("RABBITMQ_URL")
    if rabbitmq_url:
        return RabbitMQEventPublisher(rabbitmq_url)
    return InMemoryEventPublisher()


def configure_create_account(
    database_path: str = "account.db",
    rabbitmq_url: str | None = None,
) -> ForCreatingAccount:
    repository = SQLiteAccountRepository(database_path)
    event_publisher = configure_event_publisher(rabbitmq_url)
    return CreateAccountService(repository, event_publisher)


def create_app(
    database_path: str = "account.db",
    rabbitmq_url: str | None = None,
) -> FastAPI:
    app = FastAPI(title="Account Service")
    app.include_router(
        create_account_router(configure_create_account(database_path, rabbitmq_url))
    )
    return app
