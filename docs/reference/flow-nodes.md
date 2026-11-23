# Broker flow nodes

The steps of an AgentScript flow (`brokers/*.agent`), as cards on the broker canvas.

## Trigger

Entry point of the flow. Receives the A2A message for a broker interface and transitions to the first node.

**When to use it:** Exactly one per broker file.

**Examples:**

- Start with a generator that extracts ids from the message
- Go straight to a subagent for a simple assistant

```text
trigger mainTrigger:
  kind: "a2a"
  target: "brokers://my_broker/a2a"
  on_message: ->
    transition to @generator.extract
```

## Generator

One LLM call. With outputs.properties it returns typed fields (structured output); add enum to constrain values for a router.

**When to use it:** Extract ids, classify a request, summarize or rewrite text. No tools.

**Examples:**

- Extract order_id and reason from "Return ORD-1001, too small"
- Classify into "billing" | "shipping" | "other"
- Summarize a long complaint in two sentences

```text
generator classify:
  prompt: ->
    | {!@request.payload.message.parts[0].text}
  outputs:
    properties:
      case:
        type: "string"
        enum:
          - "billing"
          - "other"
```

## Router

Deterministic branch. Evaluates routes top to bottom and follows the first whose when condition is true; otherwise is the fallback.

**When to use it:** After a generator or subagent with structured outputs. Conditions use ==, != and and.

**Examples:**

- eligible == "yes" → create the RMA, otherwise explain
- case == "billing" → billing subagent
- risk == "high" and amount > 1000 → manual review

```text
router pick:
  routes:
    - target: @subagent.billing
      when: @generator.classify.output.case == "billing"
  otherwise:
    target: @subagent.general
```

## Subagent

An LLM loop that may call the actions you list (MCP tools or A2A agents) up to max_number_of_loops times, then returns text or structured outputs.

**When to use it:** A step needs judgment plus tools: look something up, ask a specialist agent, check a rule.

**Examples:**

- Tool gate: call check_eligibility, output eligible yes/no
- Delegate to a Refund agent
- Answer a question using a knowledge-base tool

## Orchestrator

Like a subagent, but meant to coordinate several agents and tools in one step, usually following numbered system instructions.

**When to use it:** Two or more agents or tools must be combined and the order can vary.

**Examples:**

- Record FNOL, check coverage, screen fraud, then decide
- Plan a trip with flight, hotel and policy agents

## Executor

Deterministic, no LLM. Runs actions with bound inputs (run @actions.x with a = expr) and sets variables.

**When to use it:** The inputs are known from earlier outputs and the call must happen exactly as written.

**Examples:**

- Create an RMA with order_id from the generator
- Refer a claim to SIU with a fixed reason
- Store a value in @variables

```text
executor createRma:
  do: ->
    run @actions.create_rma
      with order_id = @generator.extract.output.order_id
```

## Reply

Sends a status update or message to the caller and sets the task state (completed, failed, canceled, rejected). Every path must end in a terminal state: the CLI build rejects a branch that ends with input required.

**When to use it:** At the end of every path. To ask for missing details, reply completed with the question; the user answers in the next message.

**Examples:**

- Completed: "Refund RF-1001 issued"
- Completed with a question: "Which order do you mean?"
- Failed: "The order system is unavailable"
- Rejected: "I can't help with that"
