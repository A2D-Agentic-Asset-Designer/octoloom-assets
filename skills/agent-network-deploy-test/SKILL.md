---
name: agent-network-deploy-test
description: Use to validate, build, publish and deploy an agent network with anypoint-cli-v4, chat with the deployed broker over A2A (including SendStreamingMessage progress updates), check the replies against expected results, and stay safe in a shared Anypoint organization.
---

# Build, deploy and test

Commands run in the project folder (or pass `--path <dir>`). Use a folder under your home directory, not `/tmp`: the CLI rejects `.agent` files under `/tmp` on macOS (error 1017).

## Prerequisites

- Node.js, Java and `anypoint-cli-v4` with the `agent-network` plugin. `anypoint-cli-v4 agent-network project --help` lists `build`, `publish`, `deploy` and `undeploy`.
- Login for publish and deploy: a connected app (client id and secret) or a bearer token, via flags or env vars `ANYPOINT_CLIENT_ID`, `ANYPOINT_CLIENT_SECRET`, `ANYPOINT_ORG`, `ANYPOINT_ENV`, `ANYPOINT_HOST`. Keep them in your shell, not in files.
- A Flex gateway you may deploy to, with its name (and space).
- `groupId` in `exchange.json` set to your organization id.

## 1. Validate (before you build)

Read the project, then check by hand:
- Every `${group.name}` in the YAML exists in `exchange.json` `metadata.variables`.
- Secrets are `"secret": true` with empty defaults. Run `grep -rE "sk-[A-Za-z0-9_-]{20,}" .` and expect nothing.
- v2: every node has `on_exit`, every path ends in a terminal echo, every `target` names a connection key that exists.
- Every applied policy has a dependency in `exchange.json` (see `agent-network-governance`).
- Optional governance check: `anypoint-cli-v4 governance api validate agent-network.yaml --rulesets <ruleset>`.

## 2. Build

```sh
anypoint-cli-v4 agent-network project build
```
Ends with `Agent Network project '<assetId>' built successfully.` Fix the first error, rebuild. Common ones:

| Symptom | Fix |
|---|---|
| Policy not found / unresolved | Add the `namespace` and the `exchange.json` dependency |
| MCP protocol version error | Quote it: `"2025-06-18"` |
| Syntax error in an `.agent` file | `on_exit` must be a block, `and` not `&&`, `set @variables.x` needs a `variables:` block |
| `terminal-requires-status-update` | A final echo used `TASK_STATE_INPUT_REQUIRED`. Use COMPLETED, FAILED, CANCELED or REJECTED |
| Card rejected | Add `capabilities`, `defaultInputModes`, `defaultOutputModes` |
| LLM connection rejected (v2) | Do not use `amazonSigv4`; non-apiKey needs `inputFormat` and `authentication` |
| 1017 unsafe path | Move the project out of `/tmp` |
| MCP calls hit the wrong path | The connection url is the base. Do not add `/mcp` |

## 3. Publish (to Exchange)

```sh
anypoint-cli-v4 agent-network project publish
```
Bump `version` in `exchange.json` first; Exchange rejects a version that exists. Deploy publishes automatically unless you pass `--disable-autopublish`.

## 4. Deploy

Pass every variable. The CLI ignores `exchange.json` defaults and prompts for each missing one. Secrets: put them in env vars and expand them in your shell, never type them in a command you save.

```sh
anypoint-cli-v4 agent-network project deploy \
  -g <your-gateway> \
  --property ingressgw.url:<your-gateway-base-url> \
  --property openai.apiKey:"$OPENAI_API_KEY" \
  --property ordersMcp.url:https://<mock-or-service>/ \
  --property refundAgent.url:https://<mock-or-service>/a2a
```

- `-g` is single-gateway mode (recommended). For separate ingress and egress use `-i <ingress> -e <egress> -t <target-space>`.
- `--property name:value` is repeatable. One per `${group.name}`, written `group.name`.
- `--deployment-property brokers:replicas:2` sets sizing. `--disable-tracing` turns tracing off. `--dont-wait-for-agent-network` returns before the broker is ready.
- v1: `ingressgw.url` is the base URL of the ingress gateway. The card url is `<that>/<broker key>`.
- Check the broker is up: `GET <gateway-base>/<broker-key>/.well-known/agent-card.json` returns 200.

## 5. Chat over A2A

v1 brokers speak A2A 0.3.0 and answer in one response. v2 brokers speak A2A 1.0.

A JSON-RPC `id` must be a **string** for v1 (a large number resets the connection with 503).

v1:
```sh
curl -s "<broker-url-from-the-agent-card>" -H "Content-Type: application/json" -d '{
  "jsonrpc":"2.0","id":"1","method":"message/send",
  "params":{"message":{"kind":"message","messageId":"m-1","role":"user",
    "parts":[{"kind":"text","text":"VPN is not connecting since this morning"}]}}}'
```

v2 (header `A2A-Version: 1.0`, method `SendMessage`; a 0.3.0 call is rejected with -32009):
```sh
curl -s "<broker-url-from-the-agent-card>" -H "Content-Type: application/json" -H "A2A-Version: 1.0" -d '{
  "jsonrpc":"2.0","id":"1","method":"SendMessage",
  "params":{"message":{"messageId":"m-1","role":"ROLE_USER","parts":[{"text":"Return ORD-1002 please"}]}}}'
```

v2 with progress updates, `SendStreamingMessage` (server-sent events):
```sh
curl -sN "<broker-url-from-the-agent-card>" -H "Content-Type: application/json" -H "A2A-Version: 1.0" \
  -H "Accept: text/event-stream" -d '{
  "jsonrpc":"2.0","id":"1","method":"SendStreamingMessage",
  "params":{"message":{"messageId":"m-2","role":"ROLE_USER","parts":[{"text":"I want to return order ORD-1001, the jacket is too small"}]}}}'
```
Each `data:` line is a JSON-RPC result. A `TASK_STATE_WORKING` status update carries the progress text (for example "Checking return eligibility with the Orders MCP..."). The last event has a terminal state (`TASK_STATE_COMPLETED`) and the final reply text. Expected order for retail returns: Extracting..., Checking..., Creating..., Issuing..., then the final reply. v1 brokers do not stream.

The broker URL and A2A version are in the agent card: `GET <gateway-base>/<broker-key>/.well-known/agent-card.json`.

Auth: if the gateway answers 401 or 403 (a secured variant), add the header the policy wants (`Authorization: Bearer ...` or the client id and secret headers).

A 502 or 429 from the gateway is infrastructure (gateway down or deploy rate limit), not a flow bug. Wait and retry. Do not change the gateway.

Broker logs hold the real cause when a reply says only "internal error": `anypoint-cli-v4 runtime-mgr application download-logs` (see its `--help`).

## 6. Expected-reply checks

For each use case write 3 to 5 prompts and what must be in the reply. The template READMEs do this under *Try it* with *You should see*. Example, `v2-retail-returns`:

| Prompt | Expect |
|---|---|
| `I want to return order ORD-1001, the jacket is too small` | An RMA id (`RMA-88001`) and a refund id (`RF-1001`) |
| `Return ORD-1002 please` | A decline (outside the 30-day window) and an offer of an alternative; no RMA |
| `Return ORD-9999` | Order not found, decline branch, no RMA |

Rules:
- Check ids, branch and state, not the exact wording.
- Cover every branch of a router, plus one prompt the flow does not know.
- Run the prompts after every deploy and compare. Stop on the first mismatch and read the logs.
- With A²D mocks the answers are the same every time; with real services expect small differences.

## 7. Org safety (shared organizations)

- Only add. Deploy copies of your own project, with unique prefixes (see `agent-network-design`).
- Never undeploy, delete or overwrite a deployment you did not create. Other people demo them. `agent-network project undeploy` is only for your own test deployment, and only when you were asked to.
- Never modify a shared gateway: no `agent-network setup` commands, no policy changes on a gateway you do not own. If a gateway looks broken, report it.
- Check for connection-key collisions before a deploy (v2 keys become API instance ids): `anypoint-cli-v4 api-mgr api list`.
- Never commit or print keys, client secrets or tokens. Read them from environment variables or a file outside the project. Before you commit, run `git diff --cached | grep -cE "sk-[A-Za-z0-9_-]{20,}"` and expect 0.
- Keep real organization ids, gateway URLs and customer data out of shared files. Use placeholders such as `<your-gateway>`.
- Ask the user before any deploy. Say which gateway and which asset id.
