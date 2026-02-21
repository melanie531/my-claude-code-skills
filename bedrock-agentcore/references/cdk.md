# AgentCore CDK/CloudFormation

## Table of Contents
- Available Constructs
- CfnRuntime
- CfnRuntimeEndpoint
- CfnMemory
- CfnWorkloadIdentity
- CfnGateway and CfnGatewayTarget
- Full Stack Example
- Common Patterns

## Available Constructs

### L1 (Stable) — `aws_cdk.aws_bedrockagentcore`
| Construct | CloudFormation Type |
|-----------|-------------------|
| `CfnRuntime` | `AWS::BedrockAgentCore::Runtime` |
| `CfnRuntimeEndpoint` | `AWS::BedrockAgentCore::RuntimeEndpoint` |
| `CfnMemory` | `AWS::BedrockAgentCore::Memory` |
| `CfnWorkloadIdentity` | `AWS::BedrockAgentCore::WorkloadIdentity` |
| `CfnGateway` | `AWS::BedrockAgentCore::Gateway` |
| `CfnGatewayTarget` | `AWS::BedrockAgentCore::GatewayTarget` |
| `CfnBrowserCustom` | `AWS::BedrockAgentCore::BrowserCustom` |
| `CfnCodeInterpreterCustom` | `AWS::BedrockAgentCore::CodeInterpreterCustom` |

### L2 (Alpha) — `@aws-cdk/aws-bedrock-agentcore-alpha`
Higher-level constructs with defaults: `Runtime`, `RuntimeEndpoint`, `Memory`, `Gateway`, `WorkloadIdentity`. Install separately: `pip install aws-cdk.aws-bedrock-agentcore-alpha`.

## CfnRuntime

```python
from aws_cdk import aws_bedrockagentcore as agentcore

runtime = agentcore.CfnRuntime(self, "Runtime",
    agent_runtime_name="my_agent",  # ^[a-zA-Z][a-zA-Z0-9_]{0,47}$
    role_arn=execution_role.role_arn,

    # Container-based
    agent_runtime_artifact={
        "containerConfiguration": {
            "containerUri": f"{account}.dkr.ecr.{region}.amazonaws.com/my-agent:latest",
        }
    },

    # OR Direct code (Python only)
    # agent_runtime_artifact={
    #     "s3Configuration": {
    #         "s3Uri": "s3://bucket/agent-code.zip",
    #         "agentCoreRuntime": "PYTHON_3_13",
    #     }
    # },

    environment_variables={
        "MEMORY_ID": memory.attr_memory_id,
        "IMAGE_VERSION": "1",  # bump to force container redeploy
    },

    # Network: PUBLIC or VPC
    network_configuration={
        "networkMode": "VPC",
        "networkModeConfig": {
            "vpcEndpointConfiguration": {
                "securityGroupIds": [sg.security_group_id],
                "subnetIds": [s.subnet_id for s in vpc.private_subnets],
            }
        }
    },

    # Lifecycle
    lifecycle_configuration={
        "idleRuntimeSessionTimeout": 900,  # 60-28800s
        "maxLifetime": 28800,               # 60-28800s
    },

    # JWT authorizer (optional)
    authorizer_configuration={
        "type": "JWT",
        "jwtAuthorizerConfiguration": {
            "discoveryUrl": f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/openid-configuration",
            "allowedAudiences": [client_id],
        }
    },

    # Protocol
    protocol_configuration={"serverProtocol": "HTTP"},
)
```

## CfnRuntimeEndpoint

```python
endpoint = agentcore.CfnRuntimeEndpoint(self, "Endpoint",
    name="my_agent_live",
    agent_runtime_id=runtime.attr_agent_runtime_id,
    # Optionally pin version:
    # agent_runtime_version="3",
)
```

Use `endpoint.attr_id` for the endpoint ID. DEFAULT endpoint is auto-created.

## CfnMemory

```python
memory = agentcore.CfnMemory(self, "Memory",
    name="my_agent_memory",
    event_expiry_duration=90,  # DAYS (3-365)
    memory_execution_role_arn=memory_role.role_arn,
    encryption_key_arn=kms_key.key_arn,
    memory_strategies=[
        {"semanticMemoryStrategy": {}},
        {"summaryMemoryStrategy": {}},
        {"userPreferenceMemoryStrategy": {}},
    ],
)
```

## CfnWorkloadIdentity

```python
identity = agentcore.CfnWorkloadIdentity(self, "Identity",
    name="my_agent_identity",
    # Optional: OAuth2 return URLs for 3LO flows
    # allowed_resource_oauth2_return_urls=["https://myapp.com/callback"],
)
```

## Full Stack Example

```python
from aws_cdk import Stack, RemovalPolicy, aws_bedrockagentcore as agentcore, aws_ecr as ecr, aws_ec2 as ec2, aws_iam as iam
from constructs import Construct

class AgentCoreStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)
        region = Stack.of(self).region
        account = Stack.of(self).account

        # ECR repo
        repo = ecr.Repository(self, "Repo",
            repository_name="my-agent",
            removal_policy=RemovalPolicy.DESTROY,
            empty_on_delete=True,
        )

        # Execution role
        role = iam.Role(self, "ExecRole",
            assumed_by=iam.ServicePrincipal("bedrock-agentcore.amazonaws.com"),
        )
        role.add_to_policy(iam.PolicyStatement(
            actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"],
            resources=["arn:aws:bedrock:*::foundation-model/*"],
        ))
        role.add_to_policy(iam.PolicyStatement(
            actions=["ecr:GetAuthorizationToken"],
            resources=["*"],
        ))
        role.add_to_policy(iam.PolicyStatement(
            actions=["ecr:BatchCheckLayerAvailability", "ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"],
            resources=[repo.repository_arn],
        ))
        role.add_to_policy(iam.PolicyStatement(
            actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
            resources=["*"],
        ))

        # Runtime
        runtime = agentcore.CfnRuntime(self, "Runtime",
            agent_runtime_name="my_agent",
            role_arn=role.role_arn,
            agent_runtime_artifact={
                "containerConfiguration": {
                    "containerUri": f"{account}.dkr.ecr.{region}.amazonaws.com/my-agent:latest",
                }
            },
            network_configuration={"networkMode": "PUBLIC"},
            environment_variables={"IMAGE_VERSION": "1"},
        )

        # Endpoint
        endpoint = agentcore.CfnRuntimeEndpoint(self, "Endpoint",
            name="my_agent_live",
            agent_runtime_id=runtime.attr_agent_runtime_id,
        )
```

## Common Patterns

### Cross-stack references
Pass runtime ARN and endpoint ID as string parameters to avoid cyclic dependencies:
```python
# In consuming stack
runtime_arn = f"arn:aws:bedrock-agentcore:{region}:{account}:runtime/{runtime_id}"
```

### Environment variable bumping
To force container redeploy after pushing new ECR image:
```python
environment_variables={"IMAGE_VERSION": "2"}  # increment to trigger update
```

### CDK-nag suppressions
```python
import cdk_nag
cdk_nag.NagSuppressions.add_resource_suppressions(role, [
    cdk_nag.NagPackSuppression(
        id="AwsSolutions-IAM5",
        reason="AgentCore requires wildcard for ECR auth token and CloudWatch logs",
        applies_to=["Resource::*"],
    ),
], apply_to_children=True)
```
