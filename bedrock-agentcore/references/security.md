# AgentCore Security

## Table of Contents
- IAM Permissions
- VPC Configuration
- Authentication and Identity
- Encryption
- Service-Linked Roles
- Best Practices

## IAM Permissions

### Runtime Execution Role
Trust policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
```

Minimum permissions:
```python
# Bedrock model invocation
iam.PolicyStatement(
    actions=["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream",
             "bedrock:Converse", "bedrock:ConverseStream"],
    resources=["arn:aws:bedrock:*::foundation-model/*",
               f"arn:aws:bedrock:{region}:{account}:inference-profile/*"],
)

# ECR image pull
iam.PolicyStatement(actions=["ecr:GetAuthorizationToken"], resources=["*"])
iam.PolicyStatement(
    actions=["ecr:BatchCheckLayerAvailability", "ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"],
    resources=[repo_arn],
)

# CloudWatch Logs
iam.PolicyStatement(
    actions=["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
    resources=["*"],
)
```

Add as needed:
```python
# Secrets Manager
iam.PolicyStatement(
    actions=["secretsmanager:GetSecretValue", "secretsmanager:DescribeSecret"],
    resources=[f"arn:aws:secretsmanager:{region}:{account}:secret:myapp/*"],
)

# KMS decrypt
iam.PolicyStatement(actions=["kms:Decrypt"], resources=[kms_key_arn])

# Cognito (for auto-provisioning users)
iam.PolicyStatement(
    actions=["cognito-idp:AdminCreateUser", "cognito-idp:AdminGetUser",
             "cognito-idp:AdminInitiateAuth", "cognito-idp:AdminSetUserPassword"],
    resources=[f"arn:aws:cognito-idp:{region}:{account}:userpool/*"],
)

# AgentCore Memory
iam.PolicyStatement(
    actions=["bedrock-agentcore:CreateEvent", "bedrock-agentcore:ListEvents",
             "bedrock-agentcore:RetrieveMemoryRecords", "bedrock-agentcore:ListMemoryRecords"],
    resources=["*"],
)
```

### Memory Execution Role
Must trust BOTH services:
```python
memory_role = iam.Role(self, "MemoryRole",
    assumed_by=iam.CompositePrincipal(
        iam.ServicePrincipal("bedrock.amazonaws.com"),
        iam.ServicePrincipal("bedrock-agentcore.amazonaws.com"),
    ),
)
memory_role.add_to_policy(iam.PolicyStatement(
    actions=["bedrock:InvokeModel"],
    resources=["arn:aws:bedrock:*::foundation-model/*"],
))
```

### Invoker Permissions
```python
# For Lambda/services that invoke the runtime
iam.PolicyStatement(
    actions=["bedrock-agentcore:InvokeAgentRuntime"],
    resources=["*"],  # AgentCore does not support resource-level ARNs for this action
)
```

### Control Plane vs Data Plane
| API | Service | Example Operations |
|-----|---------|-------------------|
| `bedrock-agentcore-control` | Control plane | `GetAgentRuntime`, `UpdateAgentRuntime`, `CreateMemory` |
| `bedrock-agentcore` | Data plane | `InvokeAgentRuntime`, `StopRuntimeSession` |

## VPC Configuration

### Minimum VPC endpoints (no internet)
```python
# ECR API
vpc.add_interface_endpoint("EcrApi", service=ec2.InterfaceVpcEndpointAwsService.ECR)
# ECR Docker
vpc.add_interface_endpoint("EcrDkr", service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER)
# S3 Gateway (for ECR layers)
vpc.add_gateway_endpoint("S3", service=ec2.GatewayVpcEndpointAwsService.S3)
# CloudWatch Logs
vpc.add_interface_endpoint("Logs", service=ec2.InterfaceVpcEndpointAwsService.CLOUDWATCH_LOGS)
# Secrets Manager (if used)
vpc.add_interface_endpoint("SM", service=ec2.InterfaceVpcEndpointAwsService.SECRETS_MANAGER)
# Bedrock
vpc.add_interface_endpoint("Bedrock", service=ec2.InterfaceVpcEndpointAwsService("bedrock-runtime"))
```

### Security group
```python
agent_sg = ec2.SecurityGroup(self, "AgentSG", vpc=vpc,
    description="AgentCore runtime security group",
    allow_all_outbound=True,  # or restrict to specific ports
)
# Allow HTTPS from VPC CIDR
agent_sg.add_ingress_rule(ec2.Peer.ipv4(vpc.vpc_cidr_block), ec2.Port.tcp(443))
```

Note: `bedrock-agentcore-runtime` VPC endpoint is NOT available in all regions. Check availability before adding.

## Authentication and Identity

### JWT Authorizer (Cognito)
```python
authorizer_configuration={
    "type": "JWT",
    "jwtAuthorizerConfiguration": {
        "discoveryUrl": f"https://cognito-idp.{region}.amazonaws.com/{pool_id}/.well-known/openid-configuration",
        "allowedAudiences": [client_id],
    }
}
```

### Workload Identity
Digital identity for agents. Created automatically by Runtime/Gateway or manually:
```python
identity = agentcore.CfnWorkloadIdentity(self, "Identity", name="my_agent_identity")
```

### Identity-Aware Invocation
User ID propagated via header: `X-Amzn-Bedrock-AgentCore-Runtime-User-Id`

Access in agent code:
```python
@app.entrypoint
async def invoke(payload, context):
    user_id = context.identity.claims.get("sub")  # From validated JWT
```

### HMAC Password Derivation (for Cognito auto-provisioning)
Deterministic passwords derived from secret + actor ID — never stored:
```javascript
const crypto = require('crypto');
function derivePassword(secret, actorId) {
    return crypto.createHmac('sha256', secret).update(actorId).digest('hex').slice(0, 32);
}
```

## Encryption

- **Data at rest**: KMS CMK for Memory (`encryption_key_arn`), Secrets Manager secrets
- **Data in transit**: TLS 1.2+ for all API calls
- **Token Vault**: Encrypted storage for OAuth tokens, API keys, credentials

## Service-Linked Roles

| Role | Trust | Purpose |
|------|-------|---------|
| `AWSServiceRoleForBedrockAgentCoreNetwork` | `network.bedrock-agentcore.amazonaws.com` | Manages ENIs in VPC |
| `AWSServiceRoleForBedrockAgentCoreRuntimeIdentity` | `runtime-identity.bedrock-agentcore.amazonaws.com` | Manages workload access tokens |

Auto-created when using VPC resources or creating/updating Runtime.

## Best Practices

- **Least privilege**: Start with minimum permissions, add as needed
- **No hardcoded credentials**: Use Secrets Manager, environment variables, or IAM roles
- **VPC for private resources**: Use VPC mode when accessing RDS, ElastiCache, etc.
- **KMS encryption**: Use customer-managed keys for sensitive memory data
- **Non-root container user**: Create `bedrock_agentcore` user (UID 1000)
- **Resource-based policies**: Use for cross-account access to Runtime/Gateway
- **Condition keys**: Restrict VPC settings with `bedrock-agentcore:subnets` and `bedrock-agentcore:securityGroups`
- **Audit**: Enable CloudTrail for all AgentCore API calls
