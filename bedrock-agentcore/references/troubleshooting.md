# AgentCore Troubleshooting

## Table of Contents
- Runtime Errors
- Container Issues
- Network and VPC
- Memory Issues
- Gateway Issues
- CDK/CloudFormation
- CLI and SDK
- Node.js Specific

## Runtime Errors

### 504 Gateway Timeout
- Container doesn't expose port 8080
- Container isn't ARM64
- `/ping` endpoint not responding
- Container crashing during startup
- **Fix**: Check container logs at `/aws/bedrock-agentcore/runtimes/<id>-<endpoint>/`

### RuntimeClientError 500
- Container returned HTTP 500 from `/invocations`
- Check: is payload base64-encoded (CLI) or raw bytes (SDK)?
- Check container logs for stack traces
- **Fix**: Verify `/invocations` handler returns valid JSON

### RuntimeClientError 403
- IAM permissions insufficient
- JWT token expired or invalid
- Execution role cannot pull ECR image
- **Fix**: Check execution role has ECR, Bedrock, and Logs permissions

### Session Not Found
- Session already terminated (idle timeout or max lifetime reached)
- Session ID doesn't exist (never created)
- **Fix**: Use new session ID to start fresh

### Code Changes Not Reflected
- Existing sessions continue running old image
- **Fix**: Bump `IMAGE_VERSION` env var, redeploy, then use new `runtimeSessionId`

## Container Issues

### exec format error
- Building ARM64 image on x86 machine without cross-platform support
- **Fix**: Use `docker buildx build --platform linux/arm64` or CodeBuild with ARM environment

### CannotPullContainerError
- Image not in ECR
- ECR permissions missing on execution role
- **Fix**: Push image to ECR first, then deploy. Ensure role has `ecr:BatchGetImage`, `ecr:GetDownloadUrlForLayer`, `ecr:GetAuthorizationToken`

### Docker Hub Rate Limit (CodeBuild)
- `toomanyrequests: You have reached your unauthenticated pull rate limit`
- **Fix**: Replace `FROM node:22-slim` with `FROM public.ecr.aws/docker/library/node:22-slim`

### Container Starts but Returns 500
- Startup script failing silently
- Missing environment variables
- Secrets Manager access denied
- **Fix**: Check container stdout logs, verify IAM role has secretsmanager permissions

### OCI Image Index Issues
- Docker Desktop creates multi-platform manifests with attestation
- AgentCore may not resolve correctly
- **Fix**: Build with `--provenance=false` to push single-platform manifest

## Network and VPC

### ETIMEDOUT / ENETUNREACH
- No internet access in VPC (missing NAT Gateway)
- Missing VPC endpoints
- Security group blocking outbound traffic
- **Fix**: Add NAT Gateway to public subnet, or add VPC endpoints for required services

### DNS Resolution Failures
- DNS resolution not enabled in VPC
- Missing VPC endpoints for service
- **Fix**: Ensure VPC has `enableDnsSupport: true` and `enableDnsHostnames: true`

### Node.js 22 IPv6 Issue in VPC
- Node.js 22 Happy Eyeballs (`autoSelectFamily`) tries IPv6 first
- VPCs without IPv6 get `ETIMEDOUT` on IPv4 + `ENETUNREACH` on IPv6
- `curl` works but Node.js `fetch`/`https.get` fails
- **Fix**: Patch DNS lookup to force IPv4:

```javascript
// force-ipv4.js — load via NODE_OPTIONS="-r /app/force-ipv4.js"
const dns = require('dns');
const origLookup = dns.lookup;
dns.lookup = function(hostname, options, callback) {
  if (typeof options === 'function') { callback = options; options = {}; }
  if (typeof options === 'number') { options = { family: options }; }
  options = Object.assign({}, options, { family: 4 });
  return origLookup.call(dns, hostname, options, callback);
};
```

Also set: `NODE_OPTIONS="--dns-result-order=ipv4first --no-network-family-autoselection -r /app/force-ipv4.js"`

### VPC Endpoint Not Available
- `bedrock-agentcore-runtime` VPC endpoint not available in all regions
- **Fix**: Omit from VPC stack, use NAT Gateway instead for AgentCore connectivity

## Memory Issues

### Failed Memory Extractions
- Insufficient permissions on memory execution role
- Model access denied
- Quota exceeded
- **Fix**: Check with `ListMemoryExtractionJobs`, verify role trusts both `bedrock.amazonaws.com` AND `bedrock-agentcore.amazonaws.com`

### EventExpiryDuration Validation Error
- Value passed as seconds instead of days
- Value outside 3-365 range
- **Fix**: Use days (integer 3-365), not seconds

### Memory Records Not Appearing
- Extraction is asynchronous — records not instantly available
- **Fix**: Wait for extraction job to complete, check `ListMemoryExtractionJobs`

## Gateway Issues

### MCP Protocol Version Mismatch
- Gateway expects specific MCP versions: 2025-06-18 or 2025-03-26
- **Fix**: Use supported MCP client version

### Authentication Errors
- JWT token invalid or expired
- OAuth configuration mismatch
- **Fix**: Verify discovery URL, allowed audiences, token expiry

### Target Synchronization
- Tools not appearing after target creation
- **Fix**: Call `SynchronizeGatewayTargets` explicitly

## CDK/CloudFormation

### Resource Name Validation
- Names must match `^[a-zA-Z][a-zA-Z0-9_]{0,47}$`
- **Fix**: Use underscores not hyphens, start with letter, max 48 chars

### Cyclic Dependencies
- Cross-stack references creating circular deps
- **Fix**: Use string ARN construction instead of `grant_*()` methods

### Deployment Fails — Image Not Found
- CfnRuntime references ECR image that doesn't exist
- **Fix**: Push image to ECR before `cdk deploy`

### ROLLBACK_FAILED Stacks
- Stack stuck in ROLLBACK_FAILED state
- **Fix**: `aws cloudformation delete-stack --stack-name X --retain-resources <logicalId>`

### RetentionDays Enum
- `logs.RetentionDays` is an enum, not constructable from int
- **Fix**: Use a converter helper or reference enum values directly

## CLI and SDK

### CLI Payload Encoding
- `aws bedrock-agentcore invoke-agent-runtime --payload` expects base64
- Passing raw JSON string causes `Invalid base64` error
- **Fix**: `PAYLOAD=$(echo -n '{"action":"status"}' | base64) && aws ... --payload "$PAYLOAD"`

### boto3 Unknown Service
- Old boto3/botocore version doesn't know AgentCore
- **Fix**: `pip install --upgrade boto3 botocore`

### Control Plane vs Data Plane
- `get-agent-runtime` is on `bedrock-agentcore-control`, not `bedrock-agentcore`
- `invoke-agent-runtime` is on `bedrock-agentcore`
- **Fix**: Use correct service for the operation

```bash
# Control plane operations
aws bedrock-agentcore-control get-agent-runtime --agent-runtime-id <ID>
aws bedrock-agentcore-control update-agent-runtime --agent-runtime-id <ID> ...

# Data plane operations
aws bedrock-agentcore invoke-agent-runtime --agent-runtime-arn <ARN> ...
aws bedrock-agentcore stop-runtime-session --agent-runtime-arn <ARN> ...
```

### Session ID Length
- Minimum 33 characters required
- **Fix**: Use descriptive, long session IDs like `myapp-user-12345-session-primary-001`

## Node.js Specific

### OpenClaw on AgentCore
Common issues running Node.js messaging bridges:
- Startup takes ~4 minutes (plugin registration, channel connections)
- `controlUi.allowInsecureAuth: true` needed when proxy terminates TLS
- Telegram `dmPolicy: "open"` requires `allowFrom: ["*"]`
- Slack Socket Mode requires both `botToken` (xoxb-) AND `appToken` (xapp-)
- Skills installed to `/skills/`, not `~/.openclaw/skills`
- `skills.allowBundled` must be array (`["*"]`), not boolean

### Rate Limiting During Docker Build
- ClawHub/npm registries may rate-limit during skill installs
- **Fix**: Use retry wrapper with exponential backoff (30s, 60s, 120s, 240s) and 10s delays between installs
