import sqlite3
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from application.ports.receipt_repository import ReceiptRepository
from domain.issuing_status import IssuingStatus
from domain.receipt import Receipt, TransactionData


class SQLiteReceiptRepository(ReceiptRepository):
    def __init__(self, database_path: str = "issue_receipt.db") -> None:
        self.database_path = database_path
        self._ensure_schema()

    def save(self, receipt: Receipt) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO receipts (
                    id, transaction_id, customer_id, merchant_id, amount,
                    confirmed_at, status, document_data, failure_reason,
                    issued_at, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(transaction_id) DO UPDATE SET
                    status = excluded.status,
                    document_data = excluded.document_data,
                    failure_reason = excluded.failure_reason,
                    issued_at = excluded.issued_at,
                    updated_at = excluded.updated_at
                """,
                (
                    receipt.id,
                    receipt.transaction_id,
                    receipt.customer_id,
                    receipt.merchant_id,
                    str(receipt.amount),
                    receipt.confirmed_at.isoformat(),
                    receipt.status.value,
                    receipt.document_data,
                    receipt.failure_reason,
                    receipt.issued_at.isoformat() if receipt.issued_at else None,
                    receipt.created_at.isoformat(),
                    receipt.updated_at.isoformat(),
                ),
            )

    def get_by_id(self, receipt_id: str) -> Receipt | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM receipts WHERE id = ?",
                (receipt_id,),
            ).fetchone()
        return self._from_row(row)

    def get_by_transaction_id(self, transaction_id: str) -> Receipt | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM receipts WHERE transaction_id = ?",
                (transaction_id,),
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
                CREATE TABLE IF NOT EXISTS receipts (
                    id TEXT PRIMARY KEY,
                    transaction_id TEXT NOT NULL UNIQUE,
                    customer_id TEXT NOT NULL,
                    merchant_id TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    confirmed_at TEXT NOT NULL,
                    status TEXT NOT NULL,
                    document_data TEXT,
                    failure_reason TEXT,
                    issued_at TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    @staticmethod
    def _from_row(row: sqlite3.Row | None) -> Receipt | None:
        if row is None:
            return None
        return Receipt(
            id=row["id"],
            transaction_data=TransactionData(
                transaction_id=row["transaction_id"],
                customer_id=row["customer_id"],
                merchant_id=row["merchant_id"],
                amount=Decimal(row["amount"]),
                confirmed_at=datetime.fromisoformat(row["confirmed_at"]),
            ),
            status=IssuingStatus(row["status"]),
            document_data=row["document_data"],
            failure_reason=row["failure_reason"],
            issued_at=datetime.fromisoformat(row["issued_at"])
            if row["issued_at"] else None,
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
