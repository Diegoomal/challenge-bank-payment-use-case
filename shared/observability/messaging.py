import logging
from contextlib import contextmanager
from typing import Any, Iterator, Mapping

import pika

from shared.observability.context import get_correlation_id, set_correlation_id
from shared.observability.tracing import configure_tracing, get_tracer

logger = logging.getLogger(__name__)


def build_message_properties(payload: dict, **kwargs: Any) -> pika.BasicProperties:
    headers = dict(kwargs.pop("headers", {}) or {})
    _inject_trace_headers(headers)
    headers["correlation_id"] = get_correlation_id()
    payload.setdefault("correlation_id", headers["correlation_id"])
    return pika.BasicProperties(headers=headers, **kwargs)


@contextmanager
def message_published(routing_key: str, payload: dict) -> Iterator[None]:
    configure_tracing()
    tracer = get_tracer(__name__)
    with tracer.start_as_current_span("rabbitmq publish") as span:
        _set_message_attributes(span, routing_key, payload)
        try:
            yield
        except Exception as error:
            _record_span_error(span, error)
            raise
        else:
            log_message_published(routing_key, payload)


@contextmanager
def message_consumed(
    payload: dict,
    routing_key: str,
    headers: Mapping[str, Any] | None = None,
) -> Iterator[str]:
    correlation_id = set_correlation_id(
        _header_value(headers, "correlation_id") or payload.get("correlation_id")
    )
    configure_tracing()
    tracer = get_tracer(__name__)
    context = _extract_trace_context(headers)
    with tracer.start_as_current_span("rabbitmq consume", context=context) as span:
        _set_message_attributes(span, routing_key, payload)
        logger.info(
            "message consumed",
            extra={
                "event": "message.consumed",
                "routing_key": routing_key,
                "transaction_id": payload.get("transaction_id"),
            },
        )
        try:
            yield correlation_id
        except Exception as error:
            _record_span_error(span, error)
            raise


def begin_message(
    payload: dict,
    routing_key: str,
    headers: Mapping[str, Any] | None = None,
) -> str:
    correlation_id = set_correlation_id(
        _header_value(headers, "correlation_id") or payload.get("correlation_id")
    )
    logger.info(
        "message consumed",
        extra={
            "event": "message.consumed",
            "routing_key": routing_key,
            "transaction_id": payload.get("transaction_id"),
        },
    )
    return correlation_id


def log_message_published(routing_key: str, payload: dict) -> None:
    logger.info(
        "message published",
        extra={
            "event": "message.published",
            "routing_key": routing_key,
            "transaction_id": payload.get("transaction_id"),
        },
    )


def _inject_trace_headers(headers: dict[str, Any]) -> None:
    try:
        from opentelemetry.propagate import inject
    except Exception:
        return
    inject(headers)


def _extract_trace_context(headers: Mapping[str, Any] | None):
    try:
        from opentelemetry.propagate import extract
    except Exception:
        return None
    if not headers:
        return None
    return extract(dict(headers))


def _header_value(headers: Mapping[str, Any] | None, key: str) -> Any:
    if not headers:
        return None
    value = headers.get(key)
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def _set_message_attributes(span, routing_key: str, payload: dict) -> None:
    for key, value in {
        "messaging.system": "rabbitmq",
        "messaging.destination.name": routing_key,
        "messaging.rabbitmq.routing_key": routing_key,
        "correlation_id": get_correlation_id(),
        "transaction_id": payload.get("transaction_id"),
    }.items():
        if value:
            span.set_attribute(key, value)


def _record_span_error(span, error: Exception) -> None:
    span.record_exception(error)
    try:
        from opentelemetry.trace import Status, StatusCode
    except Exception:
        return
    span.set_status(Status(StatusCode.ERROR, str(error)))
