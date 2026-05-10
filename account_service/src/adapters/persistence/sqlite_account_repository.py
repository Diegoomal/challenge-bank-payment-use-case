import sqlite3
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from application.ports.account_repository import AccountRepository
from domain.account import Account
from domain.account_status import AccountStatus


class SQLiteAccountRepository(AccountRepository):
    def __init__(self, database_path: str = "account.db") -> None:
        self.database_path = database_path
        self._ensure_schema()

    def save(self, account: Account) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO accounts (
                    id, customer_id, account_holder, balance, status,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    customer_id = excluded.customer_id,
                    account_holder = excluded.account_holder,
                    balance = excluded.balance,
                    status = excluded.status,
                    updated_at = excluded.updated_at
                """,
                (
                    account.id,
                    account.customer_id,
                    account.account_holder,
                    str(account.balance),
                    account.status.value,
                    account.created_at.isoformat(),
                    account.updated_at.isoformat(),
                ),
            )

    def get_by_customer_id(self, customer_id: str) -> Account | None:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT id, customer_id, account_holder, balance, status,
                       created_at, updated_at
                FROM accounts
                WHERE customer_id = ?
                ORDER BY created_at DESC
                LIMIT 1
                """,
                (customer_id,),
            ).fetchone()

        if row is None:
            return None
        return self._account_from_row(row)

    def has_active_account(self, customer_id: str) -> bool:
        with self._connect() as connection:
            row = connection.execute(
                """
                SELECT 1
                FROM accounts
                WHERE customer_id = ? AND status = ?
                LIMIT 1
                """,
                (customer_id, AccountStatus.ACTIVE.value),
            ).fetchone()
        return row is not None

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
                    customer_id TEXT NOT NULL,
                    account_holder TEXT NOT NULL,
                    balance TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_accounts_customer_id
                ON accounts(customer_id)
                """
            )
            connection.execute(
                """
                CREATE UNIQUE INDEX IF NOT EXISTS idx_accounts_active_customer
                ON accounts(customer_id)
                WHERE status = 'ACTIVE'
                """
            )

    @staticmethod
    def _account_from_row(row: sqlite3.Row) -> Account:
        return Account(
            id=row["id"],
            customer_id=row["customer_id"],
            account_holder=row["account_holder"],
            balance=Decimal(row["balance"]),
            status=AccountStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
