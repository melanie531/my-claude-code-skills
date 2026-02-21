# AgentCore Gateway

## Table of Contents
- Overview
- Gateway Targets
- MCP Protocol
- Authentication
- CDK Configuration
- Using Gateway from Agents

## Overview

Gateway provides a unified MCP endpoint for agents to access tools. Converts APIs, Lambda functions, and MCP servers into MCP-compatible tools with built-in auth, credential management, and semantic search.

## Gateway Targets

| Target Type | Source | Use Case |
|-------------|--------|----------|
| **Lambda** | AWS Lambda function | Custom business logic |
| **OpenAPI** | OpenAPI specification | Expose REST APIs |
| **Smithy** | Smithy model definition | AWS-style APIs |
| **MCP Server** | External MCP server URL | Connect existing MCP servers |
| **API Gateway** | REST API stage | Expose API Gateway endpoints |

### Pre-built Integration Providers
Salesforce, Slack, Jira, Asana, Zendesk — configure via templates.

## MCP Protocol

Gateway speaks MCP (Model Context Protocol), versions 2025-06-18 and 2025-03-26.

### Operations

```python
import requests

GATEWAY_URL = "https://bedrock-agentcore-gateway.<region>.amazonaws.com/gateways/<gateway-id>/mcp"

# List tools
response = requests.post(GATEWAY_URL, json={
    "jsonrpc": "2.0", "method": "tools/list", "id": "1"
}, headers={"Authorization": f"Bearer {token}"})

# Call tool
response = requests.post(GATEWAY_URL, json={
    "jsonrpc": "2.0", "method": "tools/call", "id": "2",
    "params": {"name": "get_weather", "arguments": {"city": "Seattle"}}
}, headers={"Authorization": f"Bearer {token}"})

# Semantic search (find tools by natural language)
response = requests.post(GATEWAY_URL, json={
    "jsonrpc": "2.0", "method": "search", "id": "3",
    "params": {"query": "how to check order status"}
}, headers={"Authorization": f"Bearer {token}"})
```

## Authentication

### Inbound (who can call the gateway)
- **IAM_SIGV4**: AWS IAM credentials
- **CUSTOM_JWT**: OAuth 2.0 with JWT token validation
- **None**: No auth (testing only)

### Outbound (how gateway calls backends)
- **IAM Role**: For Lambda/Smithy targets
- **API Key**: For OpenAPI targets
- **OAuth 2.0**: Client credentials or authorization code grant
- **Credential Providers**: Stored in Token Vault

## CDK Configuration

```python
from aws_cdk import aws_bedrockagentcore as agentcore, aws_iam as iam

# Gateway execution role
gateway_role = iam.Role(self, "GatewayRole",
    assumed_by=iam.ServicePrincipal("bedrock-agentcore.amazonaws.com"),
)

# Create gateway
gateway = agentcore.CfnGateway(self, "Gateway",
    name="my_gateway",
    protocol_type="MCP",
    role_arn=gateway_role.role_arn,
    authorizer_type="CUSTOM_JWT",
    authorizer_configuration={
        "customJWTAuthorizerConfiguration": {
            "discoveryUrl": f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/openid-configuration",
            "allowedAudiences": [client_id],
        }
    },
)

# Add Lambda target
target = agentcore.CfnGatewayTarget(self, "WeatherTarget",
    name="weather_tool",
    gateway_identifier=gateway.attr_gateway_id,
    target_configuration={
        "lambdaTargetConfiguration": {
            "lambdaArn": weather_fn.function_arn,
        }
    },
)
```

## Using Gateway from Agents

### Strands + MCP Client
```python
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamablehttp_client

def create_gateway_client(access_token, gateway_url):
    return MCPClient(
        lambda: streamablehttp_client(
            url=gateway_url,
            headers={"Authorization": f"Bearer {access_token}"}
        ),
        prefix="gateway"
    )

gateway_client = create_gateway_client(token, gateway_url)
agent = Agent(tools=[gateway_client])
result = agent("Check the weather in Seattle")
```

### Interceptors
Lambda functions that run pre/post tool invocation for request transformation, access control, data filtering:

```python
interceptor_configurations=[{
    "lambdaInterceptorConfiguration": {
        "lambdaArn": interceptor_fn.function_arn,
        "interceptorType": "REQUEST",  # or "RESPONSE"
    }
}]
```
