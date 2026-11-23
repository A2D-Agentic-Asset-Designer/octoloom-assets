# Policies, secured connections and governance rulesets

!!! tip "Use this skill"
    Use to add gateway policies to an agent network (v1 spec.policies, v2 inbound and outbound policies), build governed and secured variants with authenticated connections, and check the project against governance rulesets with anypoint-cli-v4. Governance is a local check, not part of build or deploy.

    Source: [`skills/agent-network-governance/SKILL.md`](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/blob/main/skills/agent-network-governance/SKILL.md) · [raw](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/skills/agent-network-governance/SKILL.md). Copy the folder into `.claude/skills/` of your project (or `~/.claude/skills/`).

Two different things:
- **Policies** are part of the network. They run on the gateway: rate limiting, PII detection, schema validation, header injection, prompt decoration, message logging.
- **Governance rulesets** are a local check of your project text. They never change the build.

Examples: `templates/v1-hr-leave-governed`, `templates/v2-retail-returns-governed`, `templates/v1-hr-leave-secured`, `templates/v2-supply-chain-secured`.

## Applying a policy: three steps

1. Reference the policy with the MuleSoft policy namespace `68ef9520-24e9-4cf2-b2f5-620025690913`.
2. Add a dependency for each policy to `exchange.json`.
3. Build. The CLI also adds tracing, telemetry, MCP support, card and user-context policies itself. Do not add those.

Dependency entry (versions as in the templates; use the current version from Exchange):

```json
{ "classifier": "schema", "packaging": "zip", "groupId": "68ef9520-24e9-4cf2-b2f5-620025690913",
  "assetId": "rate-limiting", "version": "1.5.1" }
```

Policies used by the governed templates, with `assetId` and the version they ship with:

| Policy | assetId | Version | Use |
|---|---|---|---|
| Rate limiting | `rate-limiting` | 1.5.1 | Broker inbound |
| MCP PII detector | `mcp-pii-detector` | 1.0.1 | MCP connections |
| MCP schema validation | `mcp-schema-validation` | 1.3.0 | MCP connections |
| Header injection | `header-injection` | 1.3.3 | Agent or MCP connections |
| A2A PII detector (0.3.0) | `a-two-a-pii-detector` | 1.0.2 | A2A 0.3.0 agent connections |
| A2A 1.0 PII detector | `a2a-v1-pii-detector` | 1.0.0 | A2A 1.0 agent connections (v2) |
| Message logging (outbound) | `message-logging-outbound` | 2.1.0 | v2 outbound, used in the secured templates (key `log_upstream`) |
| A2A prompt decorator | `a-two-a-prompt-decorator` | 1.0.2 | A2A 0.3.0 agent connections |

## v1: `spec.policies`

A list on the broker `spec` and on each connection:

```yaml
brokers:
  octo_hl1g_leave-broker:
    spec:
      policies:
        - ref:
            name: rate-limiting
            namespace: 68ef9520-24e9-4cf2-b2f5-620025690913
          configuration:
            rateLimits:
              - maximumRequests: 60
                timePeriodInMilliseconds: 60000
            exposeHeaders: true
connections:
  hris-mcp-connection:
    kind: mcp
    ref: { name: octo_hl1g_hris-mcp }
    spec:
      url: ${hrisMcp.url}
      policies:
        - ref:
            name: mcp-pii-detector
            namespace: 68ef9520-24e9-4cf2-b2f5-620025690913
          configuration:
            entities: [Email, US SSN, Credit Card, Phone Number]
            action: Log and mask
```

## v2: named policies, then `inbound` / `outbound`

Declare policies once under `context.policies`, then reference them by key from a connection or a broker:

```yaml
context:
  policies:
    rate_limit:
      ref: { name: rate-limiting, namespace: 68ef9520-24e9-4cf2-b2f5-620025690913 }
      configuration:
        rateLimits:
          - { maximumRequests: 30, timePeriodInMilliseconds: 60000 }
        exposeHeaders: true
    mcp_pii:
      ref: { name: mcp-pii-detector, namespace: 68ef9520-24e9-4cf2-b2f5-620025690913 }
      configuration:
        entities: [Email, US SSN, Credit Card, Phone Number]
        action: Log and mask
  connections:
    orders_mcp_connection:
      kind: mcp
      ref: { name: octo_rr2g_orders_mcp }
      url: ${ordersMcp.url}
      policies:
        inbound:
          - ref: { name: mcp_pii }
brokers:
  octo_rr2g_returns_broker:
    interfaces:
      a2a:
        policies:
          inbound:
            - ref: { name: rate_limit }
```

- `inbound` runs on requests going to that connection (or into the broker). `outbound` runs on calls the broker makes upstream (for example message logging in the secured v2 templates).
- A policy can also be written inline: `- policy: { ref: { name, namespace }, configuration: {...} }` (see header injection in `v2-retail-returns-governed`).
- Policies apply to a connection key. In a v2 project, use the policy key from `context.policies`, not the Exchange name.

Check the exact placement in the template (`diff v2-retail-returns/agent-network.yaml v2-retail-returns-governed/agent-network.yaml`).

## Secured variants: authenticated connections

Add `authentication` to a connection and make every credential a variable. Secret variables have `"secret": true` and empty defaults in `exchange.json`.

```yaml
# Basic
authentication:
  kind: basic
  username: ${calendarMcp.username}
  password: ${calendarMcp.password}
# Client ID enforcement
authentication:
  kind: apikey-client-credentials
  clientId:     { value: ${hrisMcp.clientId},     name: client_id }
  clientSecret: { value: ${hrisMcp.clientSecret}, name: client_secret }
```

- v1: under the connection `spec`. v2: directly on the connection.
- Make the LLM URL a variable (`${llmGateway.url}/`) so it can sit behind a gateway.
- The upstream must enforce the same scheme. A mock that ignores auth proves nothing; say so in your test notes.
- A broker that clients must authenticate to: on a v2 broker set `interfaces.a2a.authorization` with `allowAnonymousAccess: false`. The CLI warns when it is missing.
- Never write a real credential as a default.

## Governance rulesets (local check)

```sh
anypoint-cli-v4 governance api validate <path-to-agent-network.yaml> --rulesets <ruleset>
```

Run `anypoint-cli-v4 governance api validate --help` for the exact flags (`--rulesets`, `--remote-rulesets`, `--remote`). Octoloom runs the same command from its Governance panel.

Sources of rulesets:
- Agent Fabric rulesets from MuleSoft (for example "Agent Network Best Practices"). The CLI downloads them from Exchange on first use (needs a login once), then caches them.
- Community rulesets (P4A) and your own.
- Your organization's rulesets in Exchange.
- Local ruleset YAML files.

Reading results:
- Severities: violation, warning, info. Fix violations first.
- Each finding names a rule and a path in the file. Many are reference fixes: card capabilities, `protocolVersion`, a `streamableHttp` transport, the `allowed` tools list, `allowAnonymousAccess: false` on a v2 broker, or moving an inline secret into a secret variable.
- Some P4A MCP-server rules are written for MCP server specs, not for `agent-network.yaml`. The CLI can keep reporting them after you fix the file. Treat those as known noise, but keep the fix that is correct.
- Governance is local. Do not make build, publish or deploy depend on it, and do not commit its output into the project.

## Checklist

1. Policies referenced with the namespace and listed in `exchange.json` dependencies.
2. Every credential is a secret variable with an empty default.
3. `anypoint-cli-v4 agent-network project build` passes.
4. Governance validate shows no violations you did not accept.
5. After deploy, a prompt that carries test PII shows the policy working (the governed templates have one in their README under *Try it*).
