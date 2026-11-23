# Write a v1 agent network

!!! tip "Use this skill"
    Use to write or fix a v1 (Agent Network 1.0, LLM-routed) agent-network.yaml and exchange.json for MuleSoft Agent Fabric - brokers, agents, MCP servers, LLM provider, instructions, connections and policies - and to pass the anypoint-cli-v4 build.

    Source: [`skills/agent-network-v1/SKILL.md`](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/blob/main/skills/agent-network-v1/SKILL.md) · [raw](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/skills/agent-network-v1/SKILL.md). Copy the folder into `.claude/skills/` of your project (or `~/.claude/skills/`).

v1 has one broker whose LLM reads `instructions` and picks agents and tools. Files: `agent-network.yaml` and `exchange.json`. Copy a template such as `templates/v1-it-helpdesk/` and edit. Every snippet below is from it.

## File layout of agent-network.yaml

Top-level keys, in this order: `schemaVersion`, `label`, `brokers`, `llmProviders`, `connections`, `mcpServers`, `agents`.

```yaml
schemaVersion: 1.0.0
label: IT Helpdesk
```

## Broker

```yaml
brokers:
  octo_ih1_it-helpdesk-broker:
    card:
      protocolVersion: 0.3.0
      name: octo_ih1_it-helpdesk-broker
      description: Triage and access agents work with ITSM, monitoring and knowledge-base tools to resolve tickets.
      url: ${ingressgw.url}/octo_ih1_it-helpdesk-broker
      version: 1.0.0
      capabilities: { streaming: false, pushNotifications: false, stateTransitionHistory: false }
      defaultInputModes: [application/json, text/plain]
      defaultOutputModes: [application/json, text/plain]
      skills:
        - id: it-support
          name: IT Support
          description: Resolve IT problems and access requests.
          tags: [it, helpdesk]
          examples: [VPN is not connecting since this morning]
    spec:
      llm:
        ref: { name: octo_ih1_openai }
        configuration:
          model: gpt-5-mini
          openAI: { reasoningEffort: MINIMAL }
      instructions:
        - You are the IT helpdesk for employees.
        - Before opening an incident, check service health with get_service_health and search the knowledge base with search_articles.
        - Open an incident with create_incident only when no article or known outage explains the problem.
      links:
        - agent: { ref: { name: octo_ih1_triage-agent } }
      tools:
        - mcp:
            ref: { name: octo_ih1_itsm-mcp }
            allowed: [create_incident, get_incident]
      maxNumberOfLoops: 25
      maxConsecutiveErrors: 3
      taskTimeoutSecs: 90
```

(The template writes the same content in block style. Both are valid YAML.)

Rules:
- `card.url` is `${ingressgw.url}/<broker key>`. Always a variable.
- `instructions` is a list of short sentences. Name every tool you want called and say when. Say what the answer must contain (ids, dates).
- `tools[].mcp.allowed` lists the tool names the broker may use. Leave out the dangerous ones.
- `links` lists agents the broker may call.
- Use `reasoningEffort: MINIMAL` with `gpt-5-mini` for fast answers. Gateways time out near 15 s with `MEDIUM`.

## LLM provider and connection

```yaml
llmProviders:
  octo_ih1_openai:
    label: OpenAI
    description: OpenAI LLM provider
    metadata: { platform: OpenAI, models: [gpt-5-mini] }
connections:
  openai-connection:
    kind: llm
    ref: { name: octo_ih1_openai }
    spec:
      url: https://api.openai.com/v1/
      configuration:
        apiKey: ${openai.apiKey}
        timeout: 600000
```

For an LLM gateway or a mock, make the url a variable: `url: ${llmGateway.url}/`.

## MCP servers

```yaml
connections:
  itsm-mcp-connection:
    kind: mcp
    ref: { name: octo_ih1_itsm-mcp }
    spec:
      url: ${itsmMcp.url}
mcpServers:
  octo_ih1_itsm-mcp:
    label: ITSM MCP
    description: Incident management.
    metadata:
      transport: { kind: streamableHttp, path: /mcp }
      tools:
        - name: create_incident
          description: Open an incident.
          inputSchema:
            type: object
            properties:
              summary: { type: string, description: Problem summary }
              priority: { type: string, description: P1-P4 }
            required: [summary]
```

- The connection `url` is the server base. The runtime appends `transport.path`. Do not put `/mcp` in the url.
- Quote a protocol version if you write one: `"2025-06-18"`.
- Describe every tool and every parameter. The broker LLM reads them.

## Agents

```yaml
connections:
  triage-agent-connection:
    kind: agent
    ref: { name: octo_ih1_triage-agent }
    spec:
      url: ${triageAgent.url}
agents:
  octo_ih1_triage-agent:
    label: IT Triage Agent
    description: Classifies IT problems, sets priority and proposes first steps.
    metadata: { platform: OpenAI, protocol: a2a }
    card:
      name: IT Triage Agent
      description: Classifies IT problems, sets priority and proposes first steps.
      url: ${triageAgent.url}
      protocolVersion: 0.3.0
      version: 1.0.0
      capabilities: { streaming: false, pushNotifications: false }
      defaultInputModes: [application/json, text/plain]
      defaultOutputModes: [application/json, text/plain]
      skills:
        - { id: triage-ticket, name: Triage Ticket, description: Classify an IT problem and set its priority., tags: [triage], examples: [VPN is not connecting] }
```

v1 agents speak A2A 0.3.0 only. The card needs `capabilities`, `defaultInputModes` and `defaultOutputModes`.

## exchange.json

```json
{
  "main": "agent-network.yaml",
  "name": "it-helpdesk-v1",
  "classifier": "agent-network",
  "descriptorVersion": "1.0.0",
  "apiVersion": "v1",
  "tags": ["my-project"],
  "metadata": { "variables": { "...": "one group per ${group.name}" } },
  "dependencies": [],
  "groupId": "<your-org-id>",
  "assetId": "it-helpdesk-v1",
  "version": "1.0.0"
}
```

- Every `${group.name}` in the YAML needs `metadata.variables.group.name`.
- Policies add entries to `dependencies` (see `agent-network-governance`).
- Bump `version` before each publish.

## Policies

Put `policies` as a list under a broker `spec`, an MCP connection or an agent connection. Details and the two policy namespaces are in `agent-network-governance`.

## CLI build rules (learned the hard way)

- Policy refs need `namespace: 68ef9520-24e9-4cf2-b2f5-620025690913` (MuleSoft's published policies), and each applied policy needs a `schema` / `zip` dependency in `exchange.json`.
- The CLI adds tracing, telemetry, MCP support, card and user-context policies itself. Do not add them.
- `ingressgw.url` must have a value at deploy, or the card url is wrong.
- A card without `capabilities`, `defaultInputModes` or `defaultOutputModes` is rejected.
- Build in a folder under your home directory. The CLI rejects project paths under `/tmp` on macOS (error 1017).
- Do not leave a real key as a default in `exchange.json`.

## Check

```sh
cd <project>
anypoint-cli-v4 agent-network project build
```

Success ends with `Agent Network project '<name>' built successfully.` The build needs no deploy rights. In our check it also passed with no Anypoint login, printing 401 warnings for lookups it could not make. Publish and deploy need a login (see `agent-network-deploy-test`).

Next: `agent-network-a2d-mocks` to mock the upstreams, `agent-network-deploy-test` to ship.
