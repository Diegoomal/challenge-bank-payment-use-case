import sqlite3
from datetime import datetime
from pathlib import Path

from application.ports.transaction_repository import TransactionRepository
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


class SQLiteTransactionRepository(TransactionRepository):
    def __init__(self, database_path: str = "confirm_payment.db") -> None:
        self.database_path = database_path
        self._ensure_schema()

    def save(self, transaction: Transaction) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO transactions (
                    id, merchant_id, status, confirmed_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    merchant_id = COALESCE(excluded.merchant_id, transactions.merchant_id),
                    status = excluded.status,
                    confirmed_at = excluded.confirmed_at,
                    updated_at = excluded.updated_at
                """,
                (
                    transaction.id,
                    transaction.merchant_id,
                    transaction.status.value,
                    transaction.confirmed_at.isoformat()
                    if transaction.confirmed_at else None,
                    transaction.created_at.isoformat(),
                    transaction.updated_at.isoformat(),
                ),
            )

    def get_by_id(self, transaction_id: str) -> Transaction | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, merchant_id, status, confirmed_at, created_at, updated_at
                FROM transactions
                WHERE id = ?
                """,
                (transaction_id,),
            ).fetchone()
        if row is None:
            return None
        return Transaction(
            id=row["id"],
            merchant_id=row["merchant_id"],
            status=TransactionStatus(row["status"]),
            confirmed_at=datetime.fromisoformat(row["confirmed_at"])
            if row["confirmed_at"] else None,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _ensure_schema(self) -> None:
        database_parent = Path(self.database_path).parent
        if str(database_parent) != ".":
            database_parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    merchant_id TEXT,
                    status TEXT NOT NULL,
                    confirmed_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            columns = {
                row["name"]
                for row in connection.execute("PRAGMA table_info(transactions)")
            }
            if "merchant_id" not in columns:
                connection.execute("ALTER TABLE transactions ADD COLUMN merchant_id TEXT")
