from contextvars import ContextVar
from uuid import uuid4


_correlation_id: ContextVar[str | None] = ContextVar(
    "correlation_id",
    default=None,
)


def get_correlation_id() -> str:
    correlation_id = _correlation_id.get()
    if correlation_id is None:
        correlation_id = str(uuid4())
        set_correlation_id(correlation_id)
    return correlation_id


def set_correlation_id(correlation_id: str | None) -> str:
    if not correlation_id:
        correlation_id = str(uuid4())
    _correlation_id.set(correlation_id)
    return correlation_id
