# Otel-Agent: Multi-Agent Observability

This project is designed to demonstrate how to integrate OpenTelemetry (Otel) within a simple multi-agent AI system, utilizing callbacks to track execution flows.

## Setup

Ensure you have Python >= 3.10 installed.
```bash
uv sync
```

## Running Locally

Ensure you have Python >= 3.10 and `uv` installed.
```bash
uv sync
python3 -m src.otel_agent.main "What is 2+2?"
```

## Deployment to Agent Engine

Deploy the agent to Vertex AI Agent Engine using the ADK CLI:

```bash
adk deploy agent_engine src/otel_agent --display_name "otel_agent" --project <project-id> --region us-central1
```

*(Further step-by-step guidance on OpenTelemetry hooks and tracing will be added here as features are developed.)*