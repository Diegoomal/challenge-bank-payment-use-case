import sqlite3
from datetime import datetime
from pathlib import Path

from application.ports.transaction_repository import TransactionRepository
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


class SQLiteTransactionRepository(TransactionRepository):
    def __init__(self, database_path: str = "reverse_payment.db") -> None:
        self.database_path = database_path
        self._ensure_schema()

    def save(self, transaction: Transaction) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO transactions (
                    id, status, reversal_reason, reversed_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    status = excluded.status,
                    reversal_reason = excluded.reversal_reason,
                    reversed_at = excluded.reversed_at,
                    updated_at = excluded.updated_at
                """,
                (
                    transaction.id,
                    transaction.status.value,
                    transaction.reversal_reason,
                    transaction.reversed_at.isoformat()
                    if transaction.reversed_at else None,
                    transaction.created_at.isoformat(),
                    transaction.updated_at.isoformat(),
                ),
            )

    def get_by_id(self, transaction_id: str) -> Transaction | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, status, reversal_reason, reversed_at, created_at, updated_at
                FROM transactions
                WHERE id = ?
                """,
                (transaction_id,),
            ).fetchone()
        if row is None:
            return None
        return Transaction(
            id=row["id"],
            status=TransactionStatus(row["status"]),
            reversal_reason=row["reversal_reason"],
            reversed_at=datetime.fromisoformat(row["reversed_at"])
            if row["reversed_at"] else None,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
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
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    status TEXT NOT NULL,
                    reversal_reason TEXT,
                    reversed_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
