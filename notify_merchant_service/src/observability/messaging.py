import logging
import os

from observability.context import set_correlation_id

logger = logging.getLogger(__name__)
_tracing_configured = False


def _configure_tracing() -> None:
    global _tracing_configured
    if _tracing_configured:
        return
    _tracing_configured = True
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except Exception:
        return

    service_name = os.getenv("OTEL_SERVICE_NAME", "rabbitmq_worker")
    provider = TracerProvider(resource=Resource.create({"service.name": service_name}))
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces"))
        )
    trace.set_tracer_provider(provider)


def _trace_message(span_name: str, routing_key: str, payload: dict) -> None:
    try:
        from opentelemetry import trace
    except Exception:
        return

    _configure_tracing()
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span(span_name) as span:
        span.set_attribute("messaging.system", "rabbitmq")
        span.set_attribute("messaging.destination", routing_key)
        transaction_id = payload.get("transaction_id")
        if transaction_id:
            span.set_attribute("transaction_id", transaction_id)
        correlation_id = payload.get("correlation_id")
        if correlation_id:
            span.set_attribute("correlation_id", correlation_id)


def begin_message(payload: dict, routing_key: str) -> str:
    correlation_id = set_correlation_id(payload.get("correlation_id"))
    _trace_message("rabbitmq consume", routing_key, payload)
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
    _trace_message("rabbitmq publish", routing_key, payload)
    logger.info(
        "message published",
        extra={
            "event": "message.published",
            "routing_key": routing_key,
            "transaction_id": payload.get("transaction_id"),
        },
    )
