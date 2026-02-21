---
name: bedrock-agentcore
description: >
  Build, deploy, and operate AI agents on Amazon Bedrock AgentCore — AWS's serverless runtime
  for production agentic AI. Use when working with AgentCore Runtime (container or code deployment),
  AgentCore Memory (short-term events, long-term semantic/preference/summary), AgentCore Gateway
  (MCP tool servers, API exposure), AgentCore Identity (workload identities, OAuth, JWT auth),
  or AgentCore Observability (CloudWatch, OpenTelemetry, X-Ray). Also use for CDK/CloudFormation
  infrastructure for AgentCore, Dockerfile/container patterns for AgentCore Runtime, session
  management, keepalive patterns, troubleshooting AgentCore deployments, or any task involving
  deploying agents to AgentCore. Covers Strands Agents, LangGraph, CrewAI, and custom frameworks
  on AgentCore. Includes security best practices (VPC, IAM, KMS, Cognito integration).
---

# Amazon Bedrock AgentCore

## Overview

AgentCore is a serverless platform for hosting AI agents with 9 modular services: **Runtime**, **Memory**, **Gateway**, **Identity**, **Code Interpreter**, **Browser**, **Observability**, **Evaluations**, and **Policy**. Framework-agnostic (Strands, LangGraph, CrewAI, OpenAI SDK, custom). Model-agnostic (Bedrock, external).

## Decision Tree

| Task | Reference |
|------|-----------|
| Deploy agent container to Runtime | [runtime.md](references/runtime.md) |
| Configure Memory (semantic, prefs, summary) | [memory.md](references/memory.md) |
| Set up Gateway for MCP tools | [gateway.md](references/gateway.md) |
| CDK/CloudFormation infrastructure | [cdk.md](references/cdk.md) |
| IAM, VPC, security, identity | [security.md](references/security.md) |
| Logging, tracing, metrics | [observability.md](references/observability.md) |
| Troubleshoot deployment issues | [troubleshooting.md](references/troubleshooting.md) |

## Quick Start — Container-Based Agent

### 1. Agent code (`agent.py`)

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent
from strands.models import BedrockModel

app = BedrockAgentCoreApp()
model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-6")
agent = Agent(model=model, system_prompt="You are a helpful assistant.")

@app.entrypoint
async def invoke(payload):
    user_input = payload.get("prompt", "Hello")
    async for event in agent.stream_async(user_input):
        delta = event.get("event", {}).get("contentBlockDelta", {}).get("delta", {}).get("text")
        if delta:
            yield delta

if __name__ == "__main__":
    app.run()  # localhost:8080
```

### 2. Dockerfile

```dockerfile
FROM --platform=linux/arm64 ghcr.io/astral-sh/uv:python3.13-bookworm-slim
WORKDIR /app
ENV UV_SYSTEM_PYTHON=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN uv pip install -r requirements.txt && \
    uv pip install aws-opentelemetry-distro>=0.10.1
RUN useradd -m -u 1000 bedrock_agentcore
USER bedrock_agentcore
COPY . .
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/ping', timeout=3)" || exit 1
CMD ["opentelemetry-instrument", "python", "agent.py"]
```

### 3. Deploy

```bash
# Using starter toolkit
pip install bedrock-agentcore-starter-toolkit strands-agents
agentcore create && agentcore configure -e agent.py && agentcore launch

# Or manual: build, push to ECR, deploy CDK
docker build --platform linux/arm64 -t my-agent .
aws ecr get-login-password | docker login --username AWS --password-stdin <ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com
docker tag my-agent:latest <ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com/my-agent:latest
docker push <ACCOUNT>.dkr.ecr.<REGION>.amazonaws.com/my-agent:latest
cdk deploy
```

## Container Contract

AgentCore requires these HTTP endpoints on **port 8080** (ARM64 only):

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/ping` | GET | Health check — return 200 OK |
| `/invocations` | POST | Main agent invocation (JSON or SSE streaming) |
| `/mcp` | POST | MCP protocol (port 8000 if hosting MCP server) |
| `/ws` | WS | WebSocket bidirectional streaming (optional) |

`BedrockAgentCoreApp` from the SDK handles these automatically. For custom implementations, see [runtime.md](references/runtime.md).

## Session Model

- Each `runtimeSessionId` gets a dedicated **Firecracker microVM** (CPU, memory, filesystem isolation)
- Sessions persist state between invocations to the same `runtimeSessionId`
- **Max lifetime**: 8 hours (28800s, configurable)
- **Idle timeout**: 15 minutes (900s, configurable, range 60-28800s)
- **No persistent disk** — use S3 or AgentCore Memory for data that survives session termination
- Max 500 concurrent sessions per runtime
- `StopRuntimeSession` API terminates a session immediately

## Critical Gotchas

- **ARM64 required** — build with `--platform linux/arm64` or use CodeBuild with ARM environment
- **Image must exist in ECR before CDK deploy** — push first, then `cdk deploy`
- **Resource names**: `^[a-zA-Z][a-zA-Z0-9_]{0,47}$` — underscores only, no hyphens
- **EventExpiryDuration** is in **days** (3-365), not seconds
- **Memory execution role** must trust both `bedrock.amazonaws.com` AND `bedrock-agentcore.amazonaws.com`
- **Node.js 22 in VPC** without IPv6 needs `--dns-result-order=ipv4first --no-network-family-autoselection` and a DNS lookup patch forcing `family: 4`
- **Code changes require new session** — bump env var or use new `runtimeSessionId` to get fresh container
- **VPC mode** requires NAT Gateway for internet or VPC endpoints (ECR, S3, CloudWatch Logs minimum)
- **CLI `--payload`** expects base64 — boto3 SDK handles encoding automatically
- **Control plane** API is `bedrock-agentcore-control`, **data plane** is `bedrock-agentcore`
- **Docker Hub rate limits** in CodeBuild — use `public.ecr.aws/docker/library/` mirror instead
- **Container logs** go to `/aws/bedrock-agentcore/runtimes/<agent_id>-<endpoint_name>/` — not always auto-enabled
- **Vended log delivery** for invocation-level logs requires CloudWatch Logs `create_delivery` API setup

## Supported Regions (15)

us-east-1, us-east-2, us-west-2, ap-south-1, ap-southeast-1, ap-southeast-2, ap-northeast-1, ap-northeast-2, ca-central-1, eu-central-1, eu-west-1, eu-west-2, eu-west-3, eu-north-1, sa-east-1

## Pricing

Consumption-based, per-second billing (1s minimum) for active CPU + peak memory. No upfront costs. Memory charged per event (short-term) and per record processed (long-term). Gateway charged per MCP operation. Identity free when used through Runtime/Gateway.

## Key Documentation

- Developer Guide: https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/
- API Reference: https://docs.aws.amazon.com/bedrock-agentcore/latest/APIReference/
- Samples: https://github.com/awslabs/amazon-bedrock-agentcore-samples
- Starter Toolkit: https://github.com/aws/bedrock-agentcore-starter-toolkit
- Full-Stack Template: https://github.com/awslabs/fullstack-solution-template-for-agentcore
- CDK Constructs: https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_bedrockagentcore-readme.html
