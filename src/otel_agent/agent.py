from google.adk.agents.llm_agent import Agent
from vertexai.preview.reasoning_engines import AdkApp
from .instructions import ORCHESTRATOR_INSTRUCTION
from .sub_agents import math_agent, text_agent, search_agent
from .telemetry import (
    setup_telemetry,
    before_agent_telemetry_cb, 
    after_agent_telemetry_cb,
    before_tool_telemetry_cb,
    after_tool_telemetry_cb
)

# Initialize just our Cloud Logging correlation. 
# We removed the service_name parameter because AdkApp handles OpenTelemetry setup.
setup_telemetry()

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description="Orchestrates requests by delegating to specialized agents.",
    instruction=ORCHESTRATOR_INSTRUCTION,
    sub_agents=[math_agent, text_agent, search_agent],
    before_agent_callback=before_agent_telemetry_cb,
    after_agent_callback=after_agent_telemetry_cb,
    before_tool_callback=before_tool_telemetry_cb,
    after_tool_callback=after_tool_telemetry_cb
)

adk_app = AdkApp(
    agent=root_agent,
    enable_tracing=True 
)