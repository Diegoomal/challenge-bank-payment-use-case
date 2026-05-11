import json
import logging
import os
from datetime import datetime, timezone

from observability.context import get_correlation_id


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "service": os.getenv("OTEL_SERVICE_NAME", "unknown_service"),
            "message": record.getMessage(),
            "correlation_id": get_correlation_id(),
            "logger": record.name,
        }
        for key in ["event", "routing_key", "transaction_id", "status"]:
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging() -> None:
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
