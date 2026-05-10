from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Protocol


class IEntity(Protocol):
    id: int
    created_at: datetime
    updated_at: datetime

    def to_string(self) -> str:
        return (
            f"User(id={self.id},"
            f"created_at={self.created_at}, "
            f"updated_at={self.updated_at})"
        )


@dataclass
class User(IEntity):
    id: int
    name: str
    email: str
    birthdate: date
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_string(self) -> str:
        return (
            f"User(id={self.id}, name={self.name}, email={self.email}, "
            f"birthdate={self.birthdate}, created_at={self.created_at}, "
            f"updated_at={self.updated_at})"
        )

    def __str__(self) -> str:
        return self.to_string()

    def __repr__(self) -> str:
        return self.to_string()
