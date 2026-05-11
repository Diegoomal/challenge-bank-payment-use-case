import logging
import os
import time

from fastapi import Request
from fastapi.responses import Response

from shared.observability.context import set_correlation_id
from shared.observability.tracing import configure_tracing

logger = logging.getLogger(__name__)

try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
except Exception:  # pragma: no cover - optional dependency
    CONTENT_TYPE_LATEST = "text/plain"
    Counter = None
    Histogram = None
    generate_latest = None


if Counter is not None:
    HTTP_REQUESTS = Counter(
        "http_requests_total",
        "Total HTTP requests",
        ["service", "method", "path", "status"],
    )
    HTTP_DURATION = Histogram(
        "http_request_duration_seconds",
        "HTTP request duration",
        ["service", "method", "path"],
    )
else:
    HTTP_REQUESTS = None
    HTTP_DURATION = None


def configure_observability(app, service_name: str) -> None:
    os.environ.setdefault("OTEL_SERVICE_NAME", service_name)
    configure_tracing(service_name)
    _instrument_fastapi(app)

    @app.middleware("http")
    async def correlation_metrics_and_logging(request: Request, call_next):
        correlation_id = set_correlation_id(request.headers.get("X-Correlation-ID"))
        start = time.monotonic()
        response = await call_next(request)
        duration = time.monotonic() - start
        response.headers["X-Correlation-ID"] = correlation_id

        path = request.url.path
        status = str(response.status_code)
        if HTTP_REQUESTS is not None:
            HTTP_REQUESTS.labels(service_name, request.method, path, status).inc()
            HTTP_DURATION.labels(service_name, request.method, path).observe(duration)

        logger.info(
            "http request handled",
            extra={
                "duration_ms": round(duration * 1000, 3),
                "event": "http.request",
                "http_method": request.method,
                "http_path": path,
                "http_status": status,
                "status": status,
            },
        )
        return response

    @app.get("/metrics", include_in_schema=False)
    def metrics() -> Response:
        if generate_latest is None:
            return Response("", media_type="text/plain")
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def _instrument_fastapi(app) -> None:
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except Exception:
        return
    FastAPIInstrumentor.instrument_app(app)
