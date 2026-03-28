import pytest
from unittest.mock import patch, MagicMock
from google.adk.agents.llm_agent import Agent

# Attempt to import our sub-agents
try:
    from otel_agent.sub_agents import math_agent, text_agent, search_agent
except ImportError:
    math_agent = None
    text_agent = None
    search_agent = None

def test_sub_agents_initialization():
    assert math_agent is not None, "math_agent should be defined"
    assert text_agent is not None, "text_agent should be defined"
    assert search_agent is not None, "search_agent should be defined"
    
    assert isinstance(math_agent, Agent), "math_agent must be an ADK Agent"
    assert isinstance(text_agent, Agent), "text_agent must be an ADK Agent"
    assert isinstance(search_agent, Agent), "search_agent must be an ADK Agent"
    
    # Check if search_agent has tools
    assert len(search_agent.tools) > 0, "search_agent should have at least one tool"

@patch('google.adk.agents.llm_agent.Agent.__call__')
def test_math_agent_execution(mock_call):
    if math_agent is None:
        pytest.skip("math_agent not implemented yet")
        
    mock_call.return_value = "4"
    result = math_agent("What is 2+2?")
    assert result == "4"
    mock_call.assert_called_once_with("What is 2+2?")

@patch('google.adk.agents.llm_agent.Agent.__call__')
def test_text_agent_execution(mock_call):
    if text_agent is None:
        pytest.skip("text_agent not implemented yet")
        
    mock_call.return_value = "Once upon a time..."
    result = text_agent("Tell me a story.")
    assert result == "Once upon a time..."
    mock_call.assert_called_once_with("Tell me a story.")

@patch('google.adk.agents.llm_agent.Agent.__call__')
def test_search_agent_execution(mock_call):
    if search_agent is None:
        pytest.skip("search_agent not implemented yet")
        
    mock_call.return_value = "The weather is sunny."
    result = search_agent("What is the weather?")
    assert result == "The weather is sunny."
    mock_call.assert_called_once_with("What is the weather?")
