import sqlite3
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from application.ports.account_repository import AccountRepository
from domain.account import Account
from domain.accounting_entry import AccountingEntry


class SQLiteAccountRepository(AccountRepository):
    def __init__(self, database_path: str = "credit_account.db") -> None:
        self.database_path = database_path
        self._ensure_schema()

    def save(self, account: Account) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO accounts (
                    id, customer_id, holder_name, balance, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    customer_id = excluded.customer_id,
                    holder_name = excluded.holder_name,
                    balance = excluded.balance,
                    updated_at = excluded.updated_at
                """,
                (
                    account.id,
                    account.customer_id,
                    account.holder_name,
                    str(account.balance),
                    account.created_at.isoformat(),
                    account.updated_at.isoformat(),
                ),
            )
            for entry in account.entries:
                connection.execute(
                    """
                    INSERT OR IGNORE INTO accounting_entries (
                        id, account_id, transaction_id, amount, entry_type, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        entry.id,
                        entry.account_id,
                        entry.transaction_id,
                        str(entry.amount),
                        entry.entry_type,
                        entry.created_at.isoformat(),
                    ),
                )

    def get_by_customer_id(self, customer_id: str) -> Account | None:
        with self._connect() as connection:
            account_row = connection.execute(
                """
                SELECT id, customer_id, holder_name, balance, created_at, updated_at
                FROM accounts
                WHERE customer_id = ?
                """,
                (customer_id,),
            ).fetchone()

            if account_row is None:
                return None

            entry_rows = connection.execute(
                """
                SELECT id, account_id, transaction_id, amount, entry_type, created_at
                FROM accounting_entries
                WHERE account_id = ?
                ORDER BY created_at
                """,
                (account_row["id"],),
            ).fetchall()

        return Account(
            id=account_row["id"],
            customer_id=account_row["customer_id"],
            holder_name=account_row["holder_name"],
            balance=Decimal(account_row["balance"]),
            created_at=datetime.fromisoformat(account_row["created_at"]),
            updated_at=datetime.fromisoformat(account_row["updated_at"]),
            entries=[self._entry_from_row(row) for row in entry_rows],
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
                CREATE TABLE IF NOT EXISTS accounts (
                    id TEXT PRIMARY KEY,
                    customer_id TEXT NOT NULL UNIQUE,
                    holder_name TEXT NOT NULL,
                    balance TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS accounting_entries (
                    id TEXT PRIMARY KEY,
                    account_id TEXT NOT NULL,
                    transaction_id TEXT NOT NULL,
                    amount TEXT NOT NULL,
                    entry_type TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(account_id) REFERENCES accounts(id)
                )
                """
            )

    @staticmethod
    def _entry_from_row(row: sqlite3.Row) -> AccountingEntry:
        return AccountingEntry(
            id=row["id"],
            account_id=row["account_id"],
            transaction_id=row["transaction_id"],
            amount=Decimal(row["amount"]),
            entry_type=row["entry_type"],
            created_at=datetime.fromisoformat(row["created_at"]),
        )
