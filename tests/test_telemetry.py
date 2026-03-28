import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

def test_setup_telemetry():
    # Attempt to import and call setup_telemetry
    from otel_agent.telemetry import setup_telemetry
    
    setup_telemetry()
    
    # Verify that the tracer provider is configured
    provider = trace.get_tracer_provider()
    assert isinstance(provider, TracerProvider)
