# AgentCore Runtime

## Table of Contents
- Deployment Methods
- Container-Based Deployment
- Direct Code Deployment
- Custom HTTP Contract
- Lifecycle Configuration
- Network Modes
- Versioning and Endpoints
- Session Management
- Keepalive Patterns
- Async and Long-Running Tasks
- Framework Examples

## Deployment Methods

**Container-based** (any language): Package as ARM64 Docker image, push to ECR, reference in runtime config. Full control over dependencies and system packages.

**Direct code** (Python only): Package as .zip with dependencies, upload to S3. Supported runtimes: Python 3.10, 3.11, 3.12, 3.13. Simpler but less flexible.

## Container-Based Deployment

### Minimal Python Dockerfile
```dockerfile
FROM --platform=linux/arm64 ghcr.io/astral-sh/uv:python3.13-bookworm-slim
WORKDIR /app
ENV UV_SYSTEM_PYTHON=1 PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN uv pip install -r requirements.txt
RUN useradd -m -u 1000 bedrock_agentcore
USER bedrock_agentcore
COPY . .
EXPOSE 8080
CMD ["python", "agent.py"]
```

### Node.js Dockerfile
```dockerfile
FROM --platform=linux/arm64 public.ecr.aws/docker/library/node:22-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl jq && rm -rf /var/lib/apt/lists/*
COPY package*.json ./
RUN npm ci --omit=dev
COPY . .
EXPOSE 8080
ENTRYPOINT ["node", "server.js"]
```

### Key requirements
- **Platform**: ARM64 (`--platform=linux/arm64`)
- **Port**: 8080 (required, not configurable)
- **Non-root user**: Recommended for security (`useradd -m -u 1000 bedrock_agentcore`)
- **ECR**: Image must be pushed to ECR before runtime creation
- **Base image**: Use `public.ecr.aws/docker/library/` prefix in CodeBuild to avoid Docker Hub rate limits

### Build with CodeBuild (ARM64)
When local machine is x86, use CodeBuild with ARM environment:
```yaml
# buildspec.yml
version: 0.2
phases:
  pre_build:
    commands:
      - aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
  build:
    commands:
      - docker build -t $ECR_REPO_NAME:latest .
      - docker tag $ECR_REPO_NAME:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$ECR_REPO_NAME:latest
  post_build:
    commands:
      - docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/$ECR_REPO_NAME:latest
```

CodeBuild project: ARM_CONTAINER type, `aws/codebuild/amazonlinux2-aarch64-standard:2.0` image, `BUILD_GENERAL1_LARGE` compute, privileged mode enabled.

## Custom HTTP Contract

If not using `BedrockAgentCoreApp`, implement these endpoints on port 8080:

### GET /ping
```javascript
// Health check — return 200 with optional status
server.get('/ping', (req, res) => {
  res.json({ status: 'HealthyBusy' }); // HealthyBusy prevents idle termination
});
```

Ping response statuses:
- `Healthy`: Ready for work, can be terminated if idle
- `HealthyBusy`: Healthy but busy (keeps session alive, prevents idle termination)
- `Unhealthy`: Something is wrong

### POST /invocations
```javascript
// Main invocation endpoint
server.post('/invocations', async (req, res) => {
  const payload = req.body;
  const action = payload.action || 'default';

  // Handle different actions
  if (action === 'keepalive') {
    return res.json({ status: 'running', uptime: process.uptime() });
  }

  // Process the request
  const result = await processRequest(payload);
  res.json(result);
});
```

### SSE Streaming Response
```javascript
server.post('/invocations', async (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Transfer-Encoding', 'chunked');

  for await (const chunk of agent.stream(req.body.prompt)) {
    res.write(`data: ${JSON.stringify({ delta: chunk })}\n\n`);
  }
  res.write('data: [DONE]\n\n');
  res.end();
});
```

## Lifecycle Configuration

```python
lifecycle_configuration = {
    "idleRuntimeSessionTimeout": 900,  # 60-28800 seconds (default 900 = 15 min)
    "maxLifetime": 28800,              # 60-28800 seconds (default 28800 = 8 hours)
}
```

- `idleRuntimeSessionTimeout` must be <= `maxLifetime`
- For long-running agents (chat bots, messaging bridges): set both to 28800
- For request-response agents: lower idle timeout to save costs

## Network Modes

**PUBLIC**: Internet access enabled. Simpler setup. Use for agents that call external APIs.

**VPC**: Private networking via ENIs in your subnets. Required for accessing private resources (RDS, ElastiCache, etc.).

VPC minimum requirements:
- Subnets in supported AZs (at least 2 recommended)
- Security groups with appropriate egress rules
- NAT Gateway (for internet access) OR VPC endpoints:
  - `com.amazonaws.<region>.ecr.api` + `com.amazonaws.<region>.ecr.dkr` (image pull)
  - `com.amazonaws.<region>.s3` (Gateway endpoint, for ECR layers)
  - `com.amazonaws.<region>.logs` (CloudWatch Logs)
  - `com.amazonaws.<region>.secretsmanager` (if using Secrets Manager)

## Versioning and Endpoints

Each `UpdateAgentRuntime` creates a new immutable version. Endpoints provide stable access:

- **DEFAULT**: Auto-points to latest version. Always exists.
- **Custom endpoints**: Pin to specific version for stability.

```python
# Create custom endpoint
endpoint = agentcore.CfnRuntimeEndpoint(self, "LiveEndpoint",
    name="my_agent_live",
    agent_runtime_id=runtime.attr_agent_runtime_id,
    # Optionally pin to specific version:
    # agent_runtime_version="3",
)
```

## Session Management

### Session ID requirements
- Minimum 33 characters
- Unique per user/conversation for isolation
- Reuse same ID for related invocations (preserves state)

### Invoke via boto3
```python
import boto3, json

client = boto3.client('bedrock-agentcore')
response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:<region>:<account>:runtime/<id>",
    qualifier="my_agent_live",
    runtimeSessionId="user-session-abc123-conversation-001",
    payload=json.dumps({"prompt": "Hello"}).encode(),
    contentType="application/json",
    accept="application/json",
)
body = response["response"].read().decode()
```

### Invoke via CLI
```bash
# CLI requires base64-encoded payload
PAYLOAD=$(echo -n '{"action":"status"}' | base64)
aws bedrock-agentcore invoke-agent-runtime \
  --agent-runtime-arn "arn:aws:bedrock-agentcore:<region>:<account>:runtime/<id>" \
  --qualifier my_agent_live \
  --runtime-session-id "my-session-id-must-be-33-chars-min" \
  --payload "$PAYLOAD" \
  --region <region> \
  /tmp/output.json
```

### Stop a session
```bash
aws bedrock-agentcore stop-runtime-session \
  --agent-runtime-arn "arn:aws:bedrock-agentcore:<region>:<account>:runtime/<id>" \
  --runtime-session-id "my-session-id-must-be-33-chars-min" \
  --region <region>
```

## Keepalive Patterns

For agents that maintain persistent connections (messaging bots, WebSocket servers), use a keepalive to prevent idle timeout:

### Lambda + EventBridge (recommended)
```python
# Lambda invoked every 5 minutes by EventBridge
import boto3, json, os

client = boto3.client('bedrock-agentcore')
RUNTIME_ARN = os.environ["AGENTCORE_RUNTIME_ARN"]
QUALIFIER = os.environ["AGENTCORE_QUALIFIER"]
SESSION_ID = os.environ["SESSION_ID"]

def handler(event, context):
    response = client.invoke_agent_runtime(
        agentRuntimeArn=RUNTIME_ARN,
        qualifier=QUALIFIER,
        runtimeSessionId=SESSION_ID,
        payload=json.dumps({"action": "keepalive"}).encode(),
        contentType="application/json",
        accept="application/json",
    )
    return {"statusCode": 200, "body": response["response"].read().decode()}
```

### Container-side keepalive handler
Return `HealthyBusy` from `/ping` and handle `keepalive` action in `/invocations`:
```javascript
if (action === 'keepalive') {
  res.json({ status: 'running', uptime_seconds: Math.floor(process.uptime()) });
  return;
}
```

### Forcing image updates
After pushing a new image to ECR:
1. Bump an environment variable (e.g., `IMAGE_VERSION`) in the runtime config and redeploy
2. Start a new session with a different `runtimeSessionId` — old session keeps running old image
3. Stop old session with `StopRuntimeSession` API

## Async and Long-Running Tasks

For tasks exceeding the invocation timeout, use async processing:

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
async def invoke(payload):
    task_id = payload.get("task_id")
    if payload.get("action") == "check_status":
        # Return status of previously started task
        return {"status": get_task_status(task_id)}

    # Start long-running task
    app.add_async_task(task_id, run_long_task, payload)
    return {"task_id": task_id, "status": "started"}
```

## Framework Examples

### Strands Agent
```python
from strands import Agent
from strands.models import BedrockModel
agent = Agent(model=BedrockModel(model_id="us.anthropic.claude-sonnet-4-6"))
result = agent("What is the weather?")
```

### LangGraph Agent
```python
from langgraph.graph import StateGraph
# Deploy LangGraph graph as container on AgentCore
# See: aws-agentcore-langgraph skill on GitHub
```

### Custom Framework
Implement the HTTP contract (GET /ping, POST /invocations) on port 8080. Any language, any framework.
