import sqlite3
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from application.ports.transaction_repository import TransactionRepository
from domain.payment_method import PaymentMethod
from domain.transaction import Transaction
from domain.transaction_status import TransactionStatus


class SQLiteTransactionRepository(TransactionRepository):
    def __init__(self, database_path: str = "start_payment.db") -> None:
        self.database_path = database_path
        self._ensure_schema()

    def save(self, transaction: Transaction) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO transactions (
                    id, customer_id, merchant_id, amount, payment_method,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    transaction.id,
                    transaction.customer_id,
                    transaction.merchant_id,
                    str(transaction.amount),
                    transaction.payment_method.value,
                    transaction.status.value,
                    transaction.created_at.isoformat(),
                    transaction.updated_at.isoformat(),
                ),
            )

    def get_by_id(self, transaction_id: str) -> Transaction | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, customer_id, merchant_id, amount, payment_method,
                       status, created_at, updated_at
                FROM transactions
                WHERE id = ?
                """,
                (transaction_id,),
            ).fetchone()

        if row is None:
            return None

        return Transaction(
            id=row["id"],
            customer_id=row["customer_id"],
            merchant_id=row["merchant_id"],
            amount=Decimal(row["amount"]),
            payment_method=PaymentMethod(row["payment_method"]),
            status=TransactionStatus(row["status"]),
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
                    customer_id TEXT NOT NULL,
                    merchant_id TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    payment_method TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
