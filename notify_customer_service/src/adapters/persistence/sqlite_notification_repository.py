import sqlite3
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from application.ports.notification_repository import NotificationRepository
from domain.delivery_status import DeliveryStatus
from domain.notification import Notification
from domain.notification_channel import NotificationChannel
from domain.notification_type import NotificationType


class SQLiteNotificationRepository(NotificationRepository):
    def __init__(self, database_path: str = "notify_customer.db") -> None:
        self.database_path = database_path
        self._ensure_schema()

    def save(self, notification: Notification) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO notifications (
                    id, transaction_id, merchant_id, customer_id,
                    notification_type, amount, recipient, channel, status,
                    failure_reason, notified_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(transaction_id, customer_id, notification_type)
                DO UPDATE SET
                    recipient = excluded.recipient,
                    channel = excluded.channel,
                    status = excluded.status,
                    failure_reason = excluded.failure_reason,
                    notified_at = excluded.notified_at,
                    updated_at = excluded.updated_at
                """,
                (
                    notification.id,
                    notification.transaction_id,
                    notification.merchant_id,
                    notification.customer_id,
                    notification.notification_type.value,
                    str(notification.amount),
                    notification.recipient,
                    notification.channel.value,
                    notification.status.value,
                    notification.failure_reason,
                    notification.notified_at.isoformat()
                    if notification.notified_at else None,
                    notification.created_at.isoformat(),
                    notification.updated_at.isoformat(),
                ),
            )

    def get_by_id(self, notification_id: str) -> Notification | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM notifications
                WHERE id = ?
                """,
                (notification_id,),
            ).fetchone()
        return self._from_row(row)

    def get_by_transaction_and_customer(
        self,
        transaction_id: str,
        customer_id: str,
        notification_type: NotificationType | None = None,
    ) -> Notification | None:
        with self._connect() as connection:
            if notification_type is None:
                row = connection.execute(
                    """
                    SELECT *
                    FROM notifications
                    WHERE transaction_id = ? AND customer_id = ?
                    ORDER BY created_at DESC
                    LIMIT 1
                    """,
                    (transaction_id, customer_id),
                ).fetchone()
            else:
                row = connection.execute(
                    """
                    SELECT *
                    FROM notifications
                    WHERE transaction_id = ?
                      AND customer_id = ?
                      AND notification_type = ?
                    """,
                    (transaction_id, customer_id, notification_type.value),
                ).fetchone()
        return self._from_row(row)

    def get_by_transaction_and_merchant(
        self,
        transaction_id: str,
        merchant_id: str,
    ) -> Notification | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT *
                FROM notifications
                WHERE transaction_id = ? AND merchant_id = ?
                """,
                (transaction_id, merchant_id),
            ).fetchone()
        return self._from_row(row)

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
                CREATE TABLE IF NOT EXISTS notifications (
                    id TEXT PRIMARY KEY,
                    transaction_id TEXT NOT NULL,
                    merchant_id TEXT NOT NULL,
                    customer_id TEXT NOT NULL,
                    notification_type TEXT NOT NULL DEFAULT 'PAYMENT_CONFIRMED',
                    amount TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    channel TEXT NOT NULL,
                    status TEXT NOT NULL,
                    failure_reason TEXT,
                    notified_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    UNIQUE(transaction_id, customer_id, notification_type)
                )
                """
            )
            columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(notifications)")
            }
            if "notification_type" not in columns:
                connection.execute(
                    """
                    ALTER TABLE notifications
                    ADD COLUMN notification_type TEXT NOT NULL
                    DEFAULT 'PAYMENT_CONFIRMED'
                    """
                )
            connection.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS
                idx_notifications_transaction_customer_type
                ON notifications(transaction_id, customer_id, notification_type)
                """
            )

    @staticmethod
    def _from_row(row: sqlite3.Row | None) -> Notification | None:
        if row is None:
            return None
        return Notification(
            id=row["id"],
            transaction_id=row["transaction_id"],
            merchant_id=row["merchant_id"],
            customer_id=row["customer_id"],
            notification_type=NotificationType(row["notification_type"]),
            amount=Decimal(row["amount"]),
            recipient=row["recipient"],
            channel=NotificationChannel(row["channel"]),
            status=DeliveryStatus(row["status"]),
            failure_reason=row["failure_reason"],
            notified_at=datetime.fromisoformat(row["notified_at"])
            if row["notified_at"] else None,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
