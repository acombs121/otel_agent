import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from unittest.mock import MagicMock, patch

from otel_agent.telemetry import (
    before_agent_telemetry_cb, 
    after_agent_telemetry_cb,
    before_tool_telemetry_cb,
    after_tool_telemetry_cb
)

@pytest.fixture
def memory_exporter():
    provider = TracerProvider()
    exporter = InMemorySpanExporter()
    processor = SimpleSpanProcessor(exporter)
    provider.add_span_processor(processor)
    
    with patch("otel_agent.telemetry.trace.get_current_span") as mock_get_current_span:
        span_mock = MagicMock()
        mock_get_current_span.return_value = span_mock
        span_mock.is_recording.return_value = True
        yield span_mock
    
    exporter.clear()

def test_agent_telemetry_callbacks(memory_exporter):
    ctx = MagicMock()
    ctx.agent_name = "test_agent"
    ctx.invocation_id = "test_inv_123"
    
    before_agent_telemetry_cb(callback_context=ctx)
    after_agent_telemetry_cb(callback_context=ctx)
    
    memory_exporter.set_attribute.assert_any_call("custom.agent.name", "test_agent")

def test_tool_telemetry_callbacks(memory_exporter):
    tool = MagicMock()
    tool.name = "test_tool"
    
    ctx = MagicMock()
    ctx.agent_name = "test_agent"
    ctx.invocation_id = "test_inv_456"
    
    args = {"query": "hello"}
    
    # Run before
    before_tool_telemetry_cb(tool=tool, args=args, tool_context=ctx)
    
    # Run after
    after_tool_telemetry_cb(tool=tool, args=args, tool_context=ctx, tool_response={"result": "hi"})
    
    memory_exporter.set_attribute.assert_any_call("custom.tool.name", "test_tool")