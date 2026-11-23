# Mock the upstreams on A²D, then swap to the real services

!!! tip "Use this skill"
    Use to mock every upstream of an agent network on A²D (A2A agents, MCP servers and an LLM mock with scripted scenarios) so the network builds, deploys and answers without real systems, and to swap the mocks for the real services later.

    Source: [`skills/agent-network-a2d-mocks/SKILL.md`](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/blob/main/skills/agent-network-a2d-mocks/SKILL.md) · [raw](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/skills/agent-network-a2d-mocks/SKILL.md). Copy the folder into `.claude/skills/` of your project (or `~/.claude/skills/`).

A²D hosts mock agents (A2A), MCP servers and OpenAI-compatible LLMs at public URLs. A network that points at them runs end to end with no other system. The bundled templates do this. Build the mock first, prove the flow, then change the URL variables.

You need an A²D API key. Keep it in an environment variable (`A2D_KEY`). Never put it in a project file or a commit.

## How to create mocks

Use the A²D Platform MCP server (tools such as `design_mcp_server`, `add_mcp_tool`, `design_agent_card`, `add_agent_skill`, `add_mock_scenario`) or the Octoloom A²D palette. Create assets with the scripted tools. Do not use the AI-generation tools: their output is not repeatable. Give every mock a unique name in your org.

Platform MCP endpoint: `https://www.a2d-ai.com/api/platform-mcp/mcp` with `Authorization: Bearer $A2D_KEY` (streamable HTTP, protocol `2025-06-18`).

The reference script is `templates/tools/create-a2d.mjs` in this repo.

## Public URLs of a published mock

| Mock | URL to use in the network |
|---|---|
| MCP server | `https://www.a2d-ai.com/api/platform/<mock-id>/` (the base; the runtime adds `/mcp`) |
| A2A agent | `https://www.a2d-ai.com/api/platform/<mock-id>/a2a` |
| LLM | `https://www.a2d-ai.com/api/platform/<mock-id>/llm/v1` |

Set `status: published` on each mock, or the URL does not answer. Put each URL in the matching `exchange.json` variable default (`ordersMcp.url`, `refundAgent.url`, `a2dLlm.url`).

## MCP server mock

Design the server with the same tools as in `agent-network.yaml`. Give each tool scenarios: a condition on an input field, a JSON response, and a default.

```js
design_mcp_server({ name: "My Orders MCP", type: "mock", description: "Orders", protocol_version: "2025-06-18" })
add_mcp_tool({
  server_id, name: "check_return_eligibility", description: "Check whether an order can be returned.",
  input_schema: { type: "object", properties: { order_id: { type: "string", description: "Order id" } }, required: ["order_id"] },
  mock_scenarios: [
    { name: "ORD-1001", condition: { field: "order_id", operator: "===", value: "ORD-1001" }, response: "{\"eligible\":true}", responseType: "json" },
    { name: "default",  condition: { field: "order_id", operator: "exists" },                   response: "{\"eligible\":false}", responseType: "json" }
  ] })
update_mcp_server({ id: server_id, status: "published" })
```

Make the data tell a story: one id for the happy path, one for each branch, a default for "not found".

## A2A agent mock

```js
design_agent_card({ name: "Refund Agent", description: "Issues refunds.", platform: "mulesoft", protocol_version: "0.3.0", type: "mock", version: "1.0.0" })
add_agent_skill({ card_id, skill_id: "issue-refund", name: "Issue Refund", description: "Refund a returned order.", tags: ["refunds"], examples: ["Refund ORD-1001"] })
add_mock_scenario({ scope_type: "agent_card", scope_id: card_id,
  scenario: { name: "ORD-1001", condition: { field: "text", operator: "contains", value: "ORD-1001" }, response: "Refund RF-1001 issued: 129 CHF.", responseType: "text" } })
add_mock_scenario({ scope_type: "agent_card", scope_id: card_id,
  scenario: { name: "default", condition: { field: "text", operator: "exists" }, response: "Refund issued.", responseType: "text" } })
update_agent_card({ id: card_id, status: "published" })
```

`protocol_version` is `0.3.0` or `1.0`. Use both across a v2 network to prove mixed versions work.

## LLM mock (no OpenAI key)

An A²D LLM mock is an OpenAI-compatible endpoint that answers from scenarios. Create it with `auth_mode: any_key`, so any API key works. In the network, make the LLM URL `${a2dLlm.url}` and the key `${a2dLlm.apiKey}` with the placeholder value `a2d-mock-key`. Remove the OpenAI variable.

```js
design_llm_mock({ name: "My Returns LLM", provider: "openai", flavor: "openai", models: ["gpt-5-mini"], auth_mode: "any_key", mock_scenarios })
update_llm_mock({ id, mock_scenarios })   // re-send to change them
update_llm_mock({ id, status: "published" })
```

(`design_llm_mock` and `update_llm_mock` are the tool names used by `templates/tools/create-a2d.mjs`. If your A²D server lists different names, use its list.)

A scenario has `name`, `priority` (lower runs first), `conditions` (all must match) and a `response`.

Condition sources used by the templates:

| `source` | Meaning |
|---|---|
| `last_user_text` + `contains` | The user prompt contains a keyword |
| `body` + `field` + `exists` / `ends_with` | Look into the request body (for example the requested JSON schema or the tool list) |
| `tool_available` + `exists` | A given tool is offered to the model |
| `last_tool_name` + `===` / `ends_with` | The previous step was this tool call |
| `last_tool_output` + `field` + `===` | A field of the last tool result |

Response kinds: `text`, `structured_answer` (a final `result`), `tool_call` (name plus `arguments` or `input`).

### v2 recipe

The flow's generator and subagent ask for JSON with `text.format` and a json_schema whose `result` is an object. Match the node by its schema fields, and answer with `kind: text` carrying the whole JSON:

```js
const has = (f) => ({ source: "body", field: `text.format.schema.properties.result.properties.${f}`, operator: "exists", value: "" });
const say = (v) => ({ source: "last_user_text", operator: "contains", value: v });
// extract step
{ name: "extract ORD-1001", priority: 10, conditions: [has("order_id"), say("ORD-1001")],
  response: { kind: "text", text: JSON.stringify({ result: { order_id: "ORD-1001", reason: "too small" },
    reasoning: "mock", additionalInputRequired: false, goalComplete: true, goalFailed: false, authRequired: false }) } }
// gate step: call the tool, then answer from its output
{ name: "gate: call", priority: 30, conditions: [has("eligible"), say("ORD-1001")],
  response: { kind: "tool_call", name: "check_return_eligibility-client__check_return_eligibility", arguments: { order_id: "ORD-1001" } } }
{ name: "gate: yes", priority: 20, conditions: [has("eligible"), { source: "last_tool_name", operator: "===", value: "check_return_eligibility-client__check_return_eligibility" },
  { source: "last_tool_output", field: "content.eligible", operator: "===", value: true }], response: /* JSON text with eligible: "yes" */ }
```

- v2 tool names: MCP `<action>-client__<tool>`, A2A `<action>-client` (with a `message` argument).
- MCP tool output is under `last_tool_output.content.*`. The templates match a field of the tool JSON, for example `content.eligible` equal to `true`.
- A2A reply text does not resolve by path in v2. Write the reply text into the scenario.
- A final reply of a node without `outputs` is `structured_answer` with a string `result`.
- End with a catch-all at priority 900 that returns a short hint about which prompts the mock knows.

### v1 recipe

The v1 broker prefixes tool names with a random id per deployment (`<rand10>_get_member`). So:

- Emit one scenario per tool position N: condition `body` `tools.N.name` `ends_with` `_<tool>`, response `tool_call` with `name: "{{body.tools.N.name}}"`.
- Chain steps with `last_tool_name` `ends_with`.
- Give the first step of a plan a high number (priority 500 and up), so later steps win once a tool has run.
- Put the final answer scenario first: previous tool matches, response `structured_answer`.
- Agents are `toolKind: "custom"` calls with `input`. MCP tools use `toolKind: "function"` with `arguments`.
- A v1 MCP result only interpolates as a whole string. For an agent result, a path works: `{{last_tool_output.artifacts.0.parts.0.text}}`.
- A catch-all at priority 900.

Full generator code: `templates/tools/mocked.mjs` (`v1Scenarios`, `v2Scenarios`). Try a fully mocked template first: `v1-hotel-concierge`, `v2-warranty-repair`.

## Test the mock before you wire it

```sh
curl -s "https://www.a2d-ai.com/api/platform/<mock-id>/llm/v1/chat/completions" \
  -H "Authorization: Bearer a2d-mock-key" -H "Content-Type: application/json" \
  -d '{"model":"gpt-5-mini","messages":[{"role":"user","content":"Return ORD-1001"}]}'
```
For an agent mock, open `<url minus /a2a>/.well-known/agent-card.json` or send an A2A message (see `agent-network-deploy-test`).

## Swap to the real services

1. Do not change the YAML. Change only the variables in `exchange.json` (or pass them with `--property` at deploy): `ordersMcp.url`, `refundAgent.url`, and for the LLM `a2dLlm.url` to your LLM gateway plus an `openai.apiKey` secret.
2. If the real service needs authentication, add `authentication` to the connection (see `agent-network-governance`, secured variants) and new secret variables.
3. Check that the real service has the same tool names and schemas as the mock. The registry entry in `agent-network.yaml` must describe the real tools.
4. Re-run the build and the expected-reply checks. Expect different wording from real services; check ids and branches, not exact text.
5. Keep the mock project as your test fixture. Deploy it under another prefix, so the two do not collide.
