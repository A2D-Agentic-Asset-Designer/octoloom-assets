# Write a v2 agent network and its AgentScript flows

!!! tip "Use this skill"
    Use to write v2 (Agent Network 2.0) agent-network.yaml and the AgentScript flows in brokers/*.agent for MuleSoft Agent Fabric - triggers, generators, subagents, orchestrators, executors, routers, echo Replies (final and working progress updates), variables and outputs - so the flow builds with anypoint-cli-v4.

    Source: [`skills/agent-network-v2-flows/SKILL.md`](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/blob/main/skills/agent-network-v2-flows/SKILL.md) · [raw](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/skills/agent-network-v2-flows/SKILL.md). Copy the folder into `.claude/skills/` of your project (or `~/.claude/skills/`).

v2 has a broker whose behavior is an AgentScript program. The LLM only extracts fields, calls tools and writes text. Branching is in the program. Start from `templates/v2-retail-returns/` (smallest) and read its `brokers/returns-broker.agent` next to this skill. All snippets below come from the templates.

## agent-network.yaml (v2)

```yaml
agentNetwork: 2.0.0
info: { label: Retail Returns, version: v1, description: "..." }
registry:
  agents:
    octo_rr2_refund_agent:
      info: { label: Refund Agent, description: Issues refunds to the original payment method. }
      metadata:
        platform: MuleSoft
        interfaces:
          a2a_v03:                       # use "a2a" for an A2A 1.0 agent
            card:
              name: Refund Agent
              description: Issues refunds to the original payment method.
              version: 1.0.0
              capabilities: { pushNotifications: false }
              defaultInputModes: [application/json, text/plain]
              defaultOutputModes: [application/json, text/plain]
              skills:
                - { id: issue-refund, name: Issue Refund, description: Refund a returned order., tags: [refunds], examples: [Refund ORD-1001] }
              url: <the-agent-card-url>   # a2a_v03: url + protocolVersion
              protocolVersion: 0.3.0
  mcps:
    octo_rr2_orders_mcp:
      info: { label: Orders MCP, description: "Order management: eligibility and RMAs." }
      metadata:
        protocolVersion: "2025-06-18"
        transport: { kind: streamableHttp, path: /mcp }
        tools:
          - name: check_return_eligibility
            description: Check whether an order can be returned.
            inputSchema:
              type: object
              properties: { order_id: { type: string, description: "Order id, e.g. ORD-1001" } }
              required: [order_id]
context:
  connections:
    refund_agent_connection: { kind: a2a, ref: { name: octo_rr2_refund_agent }, url: "${refundAgent.url}" }
    orders_mcp_connection:   { kind: mcp, ref: { name: octo_rr2_orders_mcp }, url: "${ordersMcp.url}" }
    openai_connection:
      kind: llm
      ref: { name: openai, namespace: 68ef9520-24e9-4cf2-b2f5-620025690913 }
      url: https://api.openai.com/v1
      authentication: { kind: apiKey, apiKey: "${openai.apiKey}" }
brokers:
  octo_rr2_returns_broker:
    kind: AgentScript
    implementation: ./brokers/returns-broker.agent
    interfaces:
      a2a:
        card:
          name: Returns Broker
          description: "The smallest deterministic flow."
          version: 1.0.0
          capabilities: { streaming: true, pushNotifications: false }
          defaultInputModes: [text/plain]
          defaultOutputModes: [text/plain]
          skills: [ { id: return-item, name: Return an Item, description: "...", tags: [retail], examples: ["Return ORD-1002 please"] } ]
```

Rules:
- An A2A 1.0 agent has `interfaces.a2a.card` with `supportedInterfaces: [{ url, protocolBinding: JSONRPC, protocolVersion: "1.0" }]`. An A2A 0.3.0 agent has `interfaces.a2a_v03.card` with `url` and `protocolVersion: 0.3.0`.
- Both card kinds need `capabilities`, `defaultInputModes` and `defaultOutputModes`. A 1.0 card has no `stateTransitionHistory`.
- Set `capabilities.streaming: true` on the broker card when the flow has progress updates.
- MCP connection `url` is the server base. The runtime appends `transport.path`. Quote `protocolVersion`.
- LLM connection: `kind: llm`, the MuleSoft OpenAI ref above, an `authentication` block. `amazonSigv4` is rejected. A non-apiKey kind needs `inputFormat` and `authentication`.
- The card `url` in the registry is the agent's own address (the templates write the A²D mock URL there). The `url` on the connection is the variable (`${refundAgent.url}`) that deploy fills in.
- Connection keys become API Manager instance ids. Make them unique per environment (prefix them).
- `exchange.json` has the same shape as for v1 (see `agent-network-v1`), with `"main": "agent-network.yaml"`, but `"classifier": "agentic-network"` (v1 uses `agent-network`). The v2 templates keep `"apiVersion": "v1"` in it. Copy the template's file and edit the variables.

## The .agent file: header and actions

```
# @dialect: AGENTFABRIC=1.0

system:
  instructions: "You are the returns desk of an online retailer. Process returns only when the order system says the order is eligible."

config:
  agent_name: "returns-broker"
  default_llm: @llm.default

llm:
  default:
    target: "llm://openai_connection"
    kind: "OpenAI"
    model: "gpt-5-mini"
    reasoning_effort: "MINIMAL"

actions:
  check_return_eligibility:
    target: "mcp://orders_mcp_connection"
    kind: "mcp:tool"
    tool_name: "check_return_eligibility"
  create_rma:
    target: "mcp://orders_mcp_connection"
    kind: "mcp:tool"
    tool_name: "create_rma"
    inputs:
      order_id: string
      reason: string
  refund_agent:
    target: "a2a://refund_agent_connection"
    kind: "a2a:send_message"
```

- `target` names a connection key from `agent-network.yaml` (`mcp://`, `a2a://`, `llm://`).
- `inputs:` is needed on an action that an executor calls with `with` bindings.

## Variables

Declare them before use. `set` fails without a `variables:` block.

```
variables:
  note: mutable string = ""
```
```
executor remember:
  description: "Stores the reason."
  do: ->
    set @variables.note = @generator.extractReturn.output.reason
```
Read it as `@variables.note`.

## Node kinds

### trigger
```
trigger returnsBrokerTrigger:
  kind: "a2a"
  target: "brokers://octo_rr2_returns_broker/a2a"
  on_message: ->
    transition to @echo.progressExtractReturn
```
The target is `brokers://<broker key>/a2a`. The user text is `@request.payload.message.parts[0].text`.

### generator (one LLM call, structured output)
```
generator extractReturn:
  description: "Extracts the order id and the return reason from the request."
  label: "Extract Return"
  system:
    instructions: |
      Extract the order id (for example ORD-1001) and a short return reason from the customer message.
      Use "UNKNOWN" when no order id is present.
  prompt: ->
    | {!@request.payload.message.parts[0].text}
  outputs:
    properties:
      order_id: { type: "string", description: "Order id, e.g. ORD-1001, or UNKNOWN" }
      reason:   { type: "string", description: "Short return reason" }
  on_exit: ->
    transition to @echo.progressEligibilityGate
```
Use `{!expr}` inside a `|` prompt line to insert a value. Read results as `@generator.extractReturn.output.order_id`.

### subagent (LLM plus actions, one job)
```
subagent eligibilityGate:
  description: "Checks return eligibility with the Orders MCP."
  label: "Eligibility Gate"
  system:
    instructions: |
      Call the eligibility tool for the order id and report whether the order can be returned.
      Set eligible to "yes" only when the tool returns eligible true.
  reasoning:
    instructions: ->
      | Order: {!@generator.extractReturn.output.order_id}. Request: {!@request.payload.message.parts[0].text}
    actions:
      check: @actions.check_return_eligibility
    max_number_of_loops: 3
    outputs:
      properties:
        eligible: { type: "string", description: "Whether the order can be returned", enum: ["yes", "no"] }
        detail:   { type: "string", description: "Eligibility detail from the tool" }
  on_exit: ->
    transition to @router.eligibilityRouter
```
Use `enum` outputs for anything a router will test. A subagent without `outputs` returns text: read it as `@subagent.refund.output`.

### orchestrator (several agents and tools, the LLM picks the order)
```
orchestrator assessClaim:
  description: "Records the FNOL, checks coverage and screens for fraud."
  label: "Assess Claim"
  system:
    instructions: |
      1. Record the first notice of loss with the FNOL agent.
      2. Check coverage for the policy and loss type.
      3. Ask the Fraud Screening agent for a risk level.
  reasoning:
    instructions: ->
      | Policy {!@generator.classifyClaim.output.policy_id}: {!@request.payload.message.parts[0].text}
    actions:
      record_fnol: @actions.fnol_agent
      coverage: @actions.check_coverage
      fraud: @actions.fraud_agent
    max_number_of_loops: 6
    outputs:
      properties:
        covered: { type: "string", description: "Coverage result", enum: ["yes", "no"] }
  on_exit: ->
    transition to @router.claimRouter
```
Template: `v2-insurance-claims`. Use a subagent when one tool or agent is enough, an orchestrator when several are needed.

### executor (no LLM, bound inputs)
```
executor createRma:
  description: "Creates the return authorisation."
  do: ->
    run @actions.create_rma
      with order_id = @generator.extractReturn.output.order_id
      with reason = @generator.extractReturn.output.reason
  on_exit: ->
    transition to @echo.progressRefund
```
Use it when the arguments are already known. It is cheap and the same every time.

### router (the branch)
```
router eligibilityRouter:
  description: "Eligible orders get an RMA and a refund; the others get advice."
  routes:
    - target: @echo.progressCreateRma
      when: @subagent.eligibilityGate.output.eligible == "yes"
      label: "Eligible"
  otherwise:
    target: @echo.progressExplainDecline
```
Conditions use `and` / `or`, never `&&`. Always give an `otherwise`.

### echo (a Reply, final)
```
echo returnAccepted:
  kind: "a2a:status_update_event"
  state: "TASK_STATE_COMPLETED"
  message: a2a.message({messageId: uuid(), parts: [a2a.textPart("Return accepted for " + @generator.extractReturn.output.order_id + ". " + @subagent.refund.output)]})
```

## Build rules

- `generator`, `subagent`, `orchestrator` and `executor` need `on_exit`. A one-line `-> transition to ...` is a syntax error: put `transition to` on its own indented line under `on_exit: ->`.
- Every path ends in an echo with a terminal state: `TASK_STATE_COMPLETED`, `TASK_STATE_FAILED`, `TASK_STATE_CANCELED` or `TASK_STATE_REJECTED`. `TASK_STATE_INPUT_REQUIRED` as a final reply fails with `terminal-requires-status-update`.
- Use FAILED for "could not process", REJECTED for "I will not do this" (a guardrail), CANCELED when the user withdrew.
- A node that only calls a tool should not reason: use an executor.
- The `.agent` file must live in the project under a normal folder. The CLI rejects paths under `/tmp` on macOS.

## Progress updates (working echoes)

An echo with state `TASK_STATE_WORKING` and an `on_exit` is a status update, not a final reply. The flow sends it, then continues. A streaming client (`SendStreamingMessage`) sees it while the broker works. It costs no LLM call.

Put one in front of every generator, subagent, orchestrator and executor. Send every transition and router target to the progress echo, and let the echo transition to the step:

```
echo progressEligibilityGate:
  kind: "a2a:status_update_event"
  state: "TASK_STATE_WORKING"
  message: a2a.message({messageId: uuid(), parts: [a2a.textPart("Checking return eligibility with the Orders MCP...")]})
  on_exit: ->
    transition to @subagent.eligibilityGate
```

- The message is one plain sentence in the present tense, ending in `...`: "Checking ...", "Creating ...". Say what happens next.
- Name it `progress<StepName>`.
- Do not redirect reads like `@subagent.x.output`, only `transition to` and `target:` lines.
- Put all progress echoes at the END of the file, after the final replies.

### Which echo is the default

The first `echo` in the file is the one Octoloom's flow editor offers as the default next step when you add a node. It must be a final reply. That is why the progress echoes go last. If your first echo is a WORKING one, new nodes will transition into it. Octoloom only uses this for editing; the CLI does not care about order.

Generator tool: `templates/tools/progress.mjs` in the same repo adds the progress echoes to a `.agent` file (`node progress.mjs file.agent`). It is safe to read as a reference for the exact rewrite.

## Patterns worth copying

- Gate then branch: generator, subagent with enum output, router, two result paths (`v2-retail-returns`).
- Fraud screen then settle: orchestrator, router with three outcomes (`v2-insurance-claims`).
- Executor straight after a gate, no LLM (`v2-event-ticketing` reserve seats).
- Retry once, human in the loop, guardrail check, echo-rejected: the Octoloom flow editor inserts them from `+ Step -> Patterns`.

## Check

```sh
anypoint-cli-v4 agent-network project build
```
Fix the error it prints, then build again. Next: `agent-network-a2d-mocks`, `agent-network-deploy-test`.
