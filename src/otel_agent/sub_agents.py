from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from .instructions import (
    MATH_AGENT_INSTRUCTION, 
    TEXT_AGENT_INSTRUCTION, 
    SEARCH_AGENT_INSTRUCTION
)
from .telemetry import (
    before_agent_telemetry_cb, 
    after_agent_telemetry_cb,
    before_tool_telemetry_cb,
    after_tool_telemetry_cb
)

math_agent = Agent(
    model='gemini-2.5-flash',
    name='math_agent',
    description="Calculates mathematical expressions.",
    instruction=MATH_AGENT_INSTRUCTION,
    before_agent_callback=before_agent_telemetry_cb,
    after_agent_callback=after_agent_telemetry_cb,
    before_tool_callback=before_tool_telemetry_cb,
    after_tool_callback=after_tool_telemetry_cb
)

text_agent = Agent(
    model='gemini-2.5-flash',
    name='text_agent',
    description="Generates text and answers general knowledge questions.",
    instruction=TEXT_AGENT_INSTRUCTION,
    before_agent_callback=before_agent_telemetry_cb,
    after_agent_callback=after_agent_telemetry_cb,
    before_tool_callback=before_tool_telemetry_cb,
    after_tool_callback=after_tool_telemetry_cb
)

search_agent = Agent(
    model='gemini-2.5-flash',
    name='search_agent',
    description="Searches the internet for real-world information and current events.",
    instruction=SEARCH_AGENT_INSTRUCTION,
    tools=[google_search],
    before_agent_callback=before_agent_telemetry_cb,
    after_agent_callback=after_agent_telemetry_cb,
    before_tool_callback=before_tool_telemetry_cb,
    after_tool_callback=after_tool_telemetry_cb,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True
)