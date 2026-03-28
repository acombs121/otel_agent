from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import ToolContext, BaseTool
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler
import logging
from typing import Dict, Any, Optional
import os

_logging_client: Optional[google.cloud.logging.Client] = None

class TraceContextFilter(logging.Filter):
    """Filter to add trace context to log records for Google Cloud Logging correlation."""
    def filter(self, record):
        span = trace.get_current_span()
        if span and span.get_span_context().is_valid:
            ctx = span.get_span_context()
            project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
            if project_id:
                record.trace = f"projects/{project_id}/traces/{format(ctx.trace_id, '032x')}"
            record.span_id = format(ctx.span_id, '016x')
            record.trace_sampled = ctx.trace_flags.sampled
        return True

def setup_telemetry() -> None:
    """Sets up Google Cloud Logging with Trace correlation.
    Note: OpenTelemetry TracerProvider is handled natively by Vertex AI AdkApp.
    """
    global _logging_client
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    try:
        _logging_client = google.cloud.logging.Client(project=project_id)
        _logging_client.setup_logging()
        
        for handler in logging.getLogger().handlers:
            if isinstance(handler, CloudLoggingHandler):
                handler.addFilter(TraceContextFilter())
        
        logging.info("Google Cloud Logging with Trace correlation configured.")
    except Exception as e:
        logging.basicConfig(level=logging.INFO)
        logging.warning(f"Could not configure Google Cloud Logging: {e}")

def flush_telemetry() -> None:
    """Flushes Google Cloud Logging handlers."""
    if _logging_client:
        for handler in logging.getLogger().handlers:
            if isinstance(handler, CloudLoggingHandler):
                handler.flush()

def before_agent_telemetry_cb(callback_context: CallbackContext):
    """Enriches the ADK-generated span with custom agent metadata."""
    span = trace.get_current_span()
    if span and span.is_recording():
        # Added a "custom." prefix so the attributes don't accidentally 
        # overwrite any of the ADK's native internal labels.
        span.set_attribute("custom.agent.name", callback_context.agent_name)
        span.set_attribute("custom.invocation_id", callback_context.invocation_id)
    
    logging.info(f"Agent started: {callback_context.agent_name}")

def after_agent_telemetry_cb(callback_context: CallbackContext):
    """Logs completion. ADK handles ending the actual span."""
    logging.info(f"Agent completed: {callback_context.agent_name}")

def before_tool_telemetry_cb(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext) -> Optional[Dict]:
    """Enriches the ADK-generated span with custom tool metadata and arguments."""
    span = trace.get_current_span()
    if span and span.is_recording():
        span.set_attribute("custom.tool.name", tool.name)
        span.set_attribute("custom.agent.name", tool_context.agent_name)
        # Safely log the arguments passed into the tool
        for k, v in args.items():
            span.set_attribute(f"custom.tool.arg.{k}", str(v))
            
    logging.info(f"Tool started: {tool.name}")

def after_tool_telemetry_cb(tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict) -> Optional[Dict]:
    """Updates the ADK-generated span status if the tool failed."""
    span = trace.get_current_span()
    if span and span.is_recording():
        if isinstance(tool_response, dict) and ("error" in tool_response or tool_response.get("status") == "error"):
            error_msg = tool_response.get("error_message") or tool_response.get("error") or "Tool failed"
            # Explicitly mark the span as failed in the trace UI
            span.set_status(Status(StatusCode.ERROR, str(error_msg)))
            logging.error(f"Tool failed: {tool.name} - {error_msg}")
        else:
            # Span will be OK by default, but we can explicitly set it
            span.set_status(Status(StatusCode.OK))
            logging.info(f"Tool completed: {tool.name}")