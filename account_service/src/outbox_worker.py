import json
import logging
import os
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path

import pika

from observability.context import set_correlation_id
from observability.logging import configure_logging
from observability.messaging import log_message_published

logger = logging.getLogger(__name__)


class OutboxWorker:
    def __init__(
        self,
        database_path: str,
        rabbitmq_url: str,
        exchange_name: str = "payments",
    ) -> None:
        self.database_path = database_path
        self.rabbitmq_url = rabbitmq_url
        self.exchange_name = exchange_name
        self._ensure_schema()

    def run_forever(self) -> None:
        while True:
            self.publish_pending()
            time.sleep(1)

    def publish_pending(self, limit: int = 20) -> None:
        for event in self._get_pending(limit):
            try:
                payload = json.loads(event["payload"])
                set_correlation_id(payload.get("correlation_id"))
                self._publish(event["routing_key"], event["payload"])
            except Exception as error:
                self._mark_failed(event["id"], str(error))
                logger.exception(
                    "outbox publish failed",
                    extra={
                        "event": "outbox.publish_failed",
                        "routing_key": event["routing_key"],
                    },
                )
            else:
                self._mark_published(event["id"])
                log_message_published(event["routing_key"], payload)

    def _get_pending(self, limit: int) -> list[sqlite3.Row]:
        with self._connect() as connection:
            return connection.execute(
                """
                SELECT *
                FROM outbox_events
                WHERE status IN ('PENDING', 'FAILED') AND attempts < 10
                ORDER BY created_at
                LIMIT ?
                """,
                (limit,),
            ).fetchall()

    def _publish(self, routing_key: str, payload: str) -> None:
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
                routing_key=routing_key,
                body=payload.encode("utf-8"),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=pika.DeliveryMode.Persistent,
                ),
            )
        finally:
            connection.close()

    def _mark_published(self, event_id: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE outbox_events
                SET status = 'PUBLISHED', published_at = ?, last_error = NULL
                WHERE id = ?
                """,
                (datetime.now(timezone.utc).isoformat(), event_id),
            )

    def _mark_failed(self, event_id: str, error: str) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE outbox_events
                SET status = 'FAILED', attempts = attempts + 1, last_error = ?
                WHERE id = ?
                """,
                (error, event_id),
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _ensure_schema(self) -> None:
        parent = Path(self.database_path).parent
        if str(parent) != ".":
            parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS outbox_events (
                    id TEXT PRIMARY KEY,
                    aggregate_id TEXT NOT NULL,
                    event_name TEXT NOT NULL,
                    routing_key TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    status TEXT NOT NULL,
                    attempts INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL,
                    published_at TEXT,
                    last_error TEXT
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_outbox_events_pending
                ON outbox_events(status, created_at)
                """
            )


def main() -> None:
    configure_logging()
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    if not rabbitmq_url:
        raise RuntimeError("RABBITMQ_URL is required to start the outbox worker")
    database_path = os.getenv("DATABASE_PATH", "outbox.db")
    OutboxWorker(database_path, rabbitmq_url).run_forever()


if __name__ == "__main__":
    main()
