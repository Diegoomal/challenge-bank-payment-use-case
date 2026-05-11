import os
from typing import Any


_configured = False


def configure_tracing(service_name: str | None = None) -> None:
    global _configured
    if _configured:
        return
    _configured = True

    service_name = service_name or os.getenv("OTEL_SERVICE_NAME", "unknown_service")
    os.environ.setdefault("OTEL_SERVICE_NAME", service_name)

    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except Exception:
        return

    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces"))
        )
    try:
        trace.set_tracer_provider(provider)
    except Exception:
        pass


def get_tracer(name: str) -> Any:
    try:
        from opentelemetry import trace
    except Exception:
        return _NoopTracer()
    return trace.get_tracer(name)


def current_trace_ids() -> tuple[str | None, str | None]:
    try:
        from opentelemetry import trace
    except Exception:
        return None, None

    span = trace.get_current_span()
    context = span.get_span_context()
    if not context or not context.is_valid:
        return None, None
    return format(context.trace_id, "032x"), format(context.span_id, "016x")


class _NoopSpan:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def set_attribute(self, *_args, **_kwargs) -> None:
        return None

    def record_exception(self, *_args, **_kwargs) -> None:
        return None

    def set_status(self, *_args, **_kwargs) -> None:
        return None


class _NoopTracer:
    def start_as_current_span(self, *_args, **_kwargs):
        return _NoopSpan()
