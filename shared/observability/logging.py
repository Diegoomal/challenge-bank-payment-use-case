import json
import logging
import os
from datetime import datetime, timezone

from shared.observability.context import get_correlation_id
from shared.observability.tracing import current_trace_ids


EXTRA_FIELDS = {
    "duration_ms",
    "event",
    "http_method",
    "http_path",
    "http_status",
    "routing_key",
    "span_id",
    "status",
    "trace_id",
    "transaction_id",
}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        trace_id, span_id = current_trace_ids()
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": os.getenv("OTEL_SERVICE_NAME", "unknown_service"),
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": get_correlation_id(),
            "trace_id": trace_id,
            "span_id": span_id,
        }
        for key in EXTRA_FIELDS:
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging(service_name: str | None = None) -> None:
    if service_name:
        os.environ.setdefault("OTEL_SERVICE_NAME", service_name)

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(os.getenv("LOG_LEVEL", "INFO"))

    for logger_name in ["uvicorn", "uvicorn.error", "uvicorn.access"]:
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = True
    logging.getLogger("pika").setLevel(logging.WARNING)
