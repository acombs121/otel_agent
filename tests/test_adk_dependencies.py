def test_google_adk_import():
    import google.adk
    assert google.adk is not None

def test_adk_agent_import():
    from google.adk.agents.llm_agent import Agent
    assert Agent is not None
