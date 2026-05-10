import logging
import os
import time

from fastapi import Request
from fastapi.responses import Response

from observability.context import set_correlation_id

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
    _configure_tracing(app, service_name)

    @app.middleware("http")
    async def correlation_and_metrics(request: Request, call_next):
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
            extra={"status": status, "event": "http.request", "routing_key": path},
        )
        return response

    @app.get("/metrics", include_in_schema=False)
    def metrics() -> Response:
        if generate_latest is None:
            return Response("", media_type="text/plain")
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


def _configure_tracing(app, service_name: str) -> None:
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except Exception:
        return

    provider = TracerProvider(
        resource=Resource.create({"service.name": service_name})
    )
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces"))
        )
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)
