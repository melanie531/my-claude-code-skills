# AgentCore Memory

## Table of Contents
- Overview
- Short-Term Memory (Events)
- Long-Term Memory (Records)
- Memory Strategies
- CDK Configuration
- Integration with Agents
- Best Practices

## Overview

AgentCore Memory enables agents to remember past interactions. Two tiers:
- **Short-term**: Raw interaction events within/across sessions (immutable, timestamped)
- **Long-term**: Structured knowledge extracted from events (semantic search, consolidation)

## Short-Term Memory (Events)

Store raw interactions as events associated with `actorId` + `sessionId`:

```python
import boto3
client = boto3.client('bedrock-agentcore')

# Create event
client.create_event(
    memoryId="my_memory_id",
    actorId="user:12345",
    sessionId="session-abc",
    eventPayload={"role": "user", "content": "What's the weather?"},
    eventMetadata={"channel": "telegram", "timestamp": "2025-01-01T00:00:00Z"}
)

# List events
events = client.list_events(memoryId="my_memory_id", actorId="user:12345", sessionId="session-abc")

# List sessions
sessions = client.list_sessions(memoryId="my_memory_id", actorId="user:12345")
```

## Long-Term Memory (Records)

Extracted from events via LLM-powered pipeline:

```python
# Semantic search for relevant memories
records = client.retrieve_memory_records(
    memoryId="my_memory_id",
    actorId="user:12345",
    query="What does the user prefer for lunch?",
    maxResults=5
)

# List all memory records in a namespace
records = client.list_memory_records(
    memoryId="my_memory_id",
    actorId="user:12345",
    namespace="user_preferences"
)
```

## Memory Strategies

### Built-in Strategies
Managed by AgentCore, predefined extraction algorithms:

| Strategy | Namespace | Extracts |
|----------|-----------|----------|
| `SemanticMemoryStrategy` | `semantic` | Facts, knowledge, entities |
| `UserPreferencesMemoryStrategy` | `user_preferences` | Preferences, choices, styles |
| `SessionSummariesMemoryStrategy` | `session_summaries` | Conversation summaries |
| `EpisodicStrategy` | `episodic` | Scenarios, intents, actions, outcomes |

### Built-in Overrides
Extend built-in strategies with custom prompts. Still uses AgentCore's extraction pipeline.

### Self-Managed
Complete control over extraction/consolidation. Custom schemas, external system integration. Implement your own extraction logic.

## CDK Configuration

```python
from aws_cdk import aws_bedrockagentcore as agentcore, aws_iam as iam

# Memory execution role — must trust BOTH services
memory_role = iam.Role(self, "MemoryExecRole",
    assumed_by=iam.CompositePrincipal(
        iam.ServicePrincipal("bedrock.amazonaws.com"),
        iam.ServicePrincipal("bedrock-agentcore.amazonaws.com"),
    ),
)
memory_role.add_to_policy(iam.PolicyStatement(
    actions=["bedrock:InvokeModel"],
    resources=["arn:aws:bedrock:*::foundation-model/*"],
))

# Memory resource
memory = agentcore.CfnMemory(self, "Memory",
    name="my_agent_memory",                    # underscores, no hyphens
    event_expiry_duration=90,                   # DAYS (3-365), not seconds
    memory_execution_role_arn=memory_role.role_arn,
    encryption_key_arn=kms_key.key_arn,         # optional KMS CMK
    memory_strategies=[
        {"semanticMemoryStrategy": {}},
        {"summaryMemoryStrategy": {}},
        {"userPreferenceMemoryStrategy": {}},
    ],
)
```

## Integration with Agents

### Strands Agent with Memory
```python
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from strands import Agent

memory_config = AgentCoreMemoryConfig(
    memory_id="my_memory_id",
    session_id="session-abc",
    actor_id="user:12345"
)
session_manager = AgentCoreMemorySessionManager(agentcore_memory_config=memory_config)
agent = Agent(session_manager=session_manager)
result = agent("Remember that I prefer vegetarian food.")
```

### Manual Memory Integration
```python
# In your /invocations handler:
# 1. Retrieve relevant memories before agent call
memories = client.retrieve_memory_records(
    memoryId=MEMORY_ID, actorId=actor_id,
    query=user_message, maxResults=5
)
context = "\n".join([m["content"] for m in memories.get("memoryRecords", [])])

# 2. Include in system prompt
system_prompt = f"User context from memory:\n{context}\n\nBe helpful."

# 3. After agent response, create event for memory extraction
client.create_event(
    memoryId=MEMORY_ID, actorId=actor_id, sessionId=session_id,
    eventPayload={"messages": [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": agent_response}
    ]}
)
```

## Best Practices

- **Event expiry**: Set appropriate TTL (default 90 days, max 365)
- **Actor IDs**: Use channel-prefixed IDs for multi-channel agents (`telegram:12345`, `slack:U01ABC`)
- **KMS encryption**: Use customer-managed keys for sensitive data
- **Memory execution role**: Must trust both `bedrock.amazonaws.com` AND `bedrock-agentcore.amazonaws.com`
- **Extraction is async**: Memories are not instantly available after event creation
- **Cross-region inference**: Memory extraction uses CRIS (stays within geography)
- **Failed extractions**: Check with `ListMemoryExtractionJobs`, re-trigger with `StartMemoryExtractionJobs`
