import pytest
from unittest.mock import patch, MagicMock
from google.adk.agents.llm_agent import Agent

# Assume the new orchestrator is imported
from otel_agent.agent import root_agent

def test_orchestrator_initialization():
    assert root_agent is not None, "root_agent should be defined"
    assert isinstance(root_agent, Agent), "root_agent must be an ADK Agent"
    assert root_agent.name == 'root_agent'
    assert len(root_agent.sub_agents) == 3

@patch('google.adk.agents.llm_agent.Agent.__call__')
def test_orchestrator_routing_math(mock_call):
    mock_call.return_value = "Delegated to math_agent"
    result = root_agent("What is 2+2?")
    assert result == "Delegated to math_agent"
    mock_call.assert_called_once_with("What is 2+2?")

@patch('google.adk.agents.llm_agent.Agent.__call__')
def test_orchestrator_routing_search(mock_call):
    mock_call.return_value = "Delegated to search_agent"
    result = root_agent("What is the weather in Tokyo?")
    assert result == "Delegated to search_agent"
    mock_call.assert_called_once_with("What is the weather in Tokyo?")
