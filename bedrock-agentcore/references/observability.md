# AgentCore Observability

## Table of Contents
- Overview
- Metrics
- Logs
- Traces
- Vended Log Delivery
- Dashboard Setup
- OpenTelemetry Integration

## Overview

AgentCore observability is built on CloudWatch + OpenTelemetry. Three data types:
- **Metrics**: CloudWatch metrics in `AWS/Bedrock-AgentCore` namespace (auto-emitted)
- **Logs**: Container stdout/stderr + structured OTEL logs
- **Traces/Spans**: Distributed tracing via CloudWatch Transaction Search

## Metrics

Auto-emitted to `AWS/Bedrock-AgentCore` namespace (1-minute batches):

| Metric | Description |
|--------|-------------|
| Invocations | Total invocation count |
| Throttles | Throttled invocation count |
| SystemErrors | 5xx errors |
| UserErrors | 4xx errors |
| Latency | End-to-end latency |
| CPUConsumption | CPU usage (account/runtime/endpoint) |
| MemoryConsumption | Memory usage |

Dimensions: AccountId, RuntimeId, EndpointId.

## Logs

### Container Logs (stdout/stderr)
Log group: `/aws/bedrock-agentcore/runtimes/<runtime_id>-<endpoint_name>/`

Log streams:
- `runtime-logs-<UUID>`: Application stdout/stderr
- `otel-rt-logs`: OpenTelemetry structured logs

### Structured OTEL Logs
Include execution details, error tracking, performance data. Available when using `opentelemetry-instrument` command or ADOT SDK.

### Resource Usage Logs
1-second granularity telemetry for vCPU-hours and GB-hours consumption.

## Traces

### Enable CloudWatch Transaction Search (one-time)
Required for viewing traces. Enable in CloudWatch console → Settings → Transaction Search.

### Structured Spans
Available in `/aws/spans` log group after enabling Transaction Search. View in CloudWatch → Transaction Search → filter by service name.

### Custom Trace Attributes
```python
agent = Agent(
    trace_attributes={
        "user.id": user_id,
        "session.id": session_id,
        "channel": "telegram",
    }
)
```

## Vended Log Delivery

For invocation-level logs (request/response payloads), set up vended log delivery:

```python
import boto3

logs = boto3.client("logs", region_name=region)
runtime_arn = f"arn:aws:bedrock-agentcore:{region}:{account}:runtime/{runtime_id}"
log_group = f"/aws/vendedlogs/bedrock-agentcore/runtimes/{runtime_id}"

# 1. Create log group
logs.create_log_group(logGroupName=log_group)

# 2. Create delivery source
logs.put_delivery_source(
    name=f"agentcore-runtime-{runtime_id}",
    resourceArn=runtime_arn,
    logType="APPLICATION_LOGS",
)

# 3. Create delivery destination
logs.put_delivery_destination(
    name=f"agentcore-logs-{runtime_id}",
    outputFormat="json",
    deliveryDestinationConfiguration={"destinationResourceArn": f"arn:aws:logs:{region}:{account}:log-group:{log_group}"},
)

# 4. Create delivery
logs.create_delivery(
    deliverySourceName=f"agentcore-runtime-{runtime_id}",
    deliveryDestinationArn=f"arn:aws:logs:{region}:{account}:delivery-destination:agentcore-logs-{runtime_id}",
)
```

Vended logs contain structured JSON with: `runtime_arn`, `session_id`, `request_id`, `trace_id`, `span_id`, `request_payload`, `response_payload`.

## Dashboard Setup

### CloudWatch GenAI Dashboard
Pre-built dashboard for AgentCore: CloudWatch → GenAI Observability → select agent.

### Custom Dashboard
```python
from aws_cdk import aws_cloudwatch as cw

dashboard = cw.Dashboard(self, "AgentDashboard")
dashboard.add_widgets(
    cw.GraphWidget(title="Invocations",
        left=[cw.Metric(namespace="AWS/Bedrock-AgentCore",
            metric_name="Invocations", dimensions_map={"RuntimeId": runtime_id})],
    ),
    cw.GraphWidget(title="Latency",
        left=[cw.Metric(namespace="AWS/Bedrock-AgentCore",
            metric_name="Latency", dimensions_map={"RuntimeId": runtime_id},
            statistic="p99")],
    ),
    cw.GraphWidget(title="Errors",
        left=[
            cw.Metric(namespace="AWS/Bedrock-AgentCore",
                metric_name="SystemErrors", dimensions_map={"RuntimeId": runtime_id}),
            cw.Metric(namespace="AWS/Bedrock-AgentCore",
                metric_name="UserErrors", dimensions_map={"RuntimeId": runtime_id}),
        ],
    ),
)
```

### Alarms
```python
cw.Alarm(self, "ErrorAlarm",
    metric=cw.Metric(namespace="AWS/Bedrock-AgentCore",
        metric_name="SystemErrors", dimensions_map={"RuntimeId": runtime_id},
        statistic="Sum", period=Duration.minutes(5)),
    threshold=5,
    evaluation_periods=1,
    alarm_description="AgentCore runtime system errors > 5 in 5 minutes",
)
```

## OpenTelemetry Integration

### Auto-instrumentation (recommended)
```dockerfile
RUN pip install aws-opentelemetry-distro>=0.10.1
CMD ["opentelemetry-instrument", "python", "agent.py"]
```

### Manual instrumentation
```python
from opentelemetry import trace
tracer = trace.get_tracer("my-agent")

with tracer.start_as_current_span("process_request") as span:
    span.set_attribute("user.id", user_id)
    result = agent(user_message)
    span.set_attribute("response.length", len(result))
```
