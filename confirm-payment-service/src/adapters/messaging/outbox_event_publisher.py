import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from observability.context import get_correlation_id


ROUTING_KEYS = {
    "publish_account_created": "account.created",
    "publish_payment_started": "payment.started",
    "publish_debit_completed": "debit.completed",
    "publish_debit_failed": "debit.failed",
    "publish_payment_confirmed": "payment.confirmed",
    "publish_payment_reversed": "payment.reversed",
    "publish_merchant_notified": "merchant.notified",
    "publish_customer_notified": "customer.notified",
    "publish_receipt_issued": "receipt.issued",
}


class OutboxEventPublisher:
    def __init__(self, database_path: str | None = None) -> None:
        self.database_path = database_path or os.getenv("DATABASE_PATH", "outbox.db")
        self._ensure_schema()

    def __getattr__(self, name: str):
        if name not in ROUTING_KEYS:
            raise AttributeError(name)

        def publish(event) -> None:
            payload = event.to_payload()
            payload.setdefault("correlation_id", get_correlation_id())
            self._save_event(
                aggregate_id=getattr(event, "transaction_id", None)
                or getattr(event, "account_id", None)
                or getattr(event, "notification_id", None)
                or getattr(event, "receipt_id", ""),
                event_name=event.event_name,
                routing_key=ROUTING_KEYS[name],
                payload=payload,
            )

        return publish

    def _save_event(
        self,
        aggregate_id: str,
        event_name: str,
        routing_key: str,
        payload: dict[str, str],
    ) -> None:
        now = datetime.now(timezone.utc).isoformat()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO outbox_events (
                    id, aggregate_id, event_name, routing_key, payload, status,
                    attempts, created_at, published_at, last_error
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid4()),
                    aggregate_id,
                    event_name,
                    routing_key,
                    json.dumps(payload),
                    "PENDING",
                    0,
                    now,
                    None,
                    None,
                ),
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
