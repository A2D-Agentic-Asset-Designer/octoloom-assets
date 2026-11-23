<span class="ol-pill">UI reference</span>

# Broker flow nodes

<p class="lede">The steps of an AgentScript flow (`brokers/*.agent`), as cards on the broker canvas.</p>

<figure markdown>
![A 2.0 broker flow: explorer, nodes and transitions](../assets/ui/agent-flow-annot-light.webp#only-light){ loading=lazy }
![A 2.0 broker flow: explorer, nodes and transitions](../assets/ui/agent-flow-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>A 2.0 broker flow: explorer, nodes and transitions</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **Hide explorer** | Hide the flow explorer |
| <span class="ol-n">2</span> | **Visual** | Visual canvas |
| <span class="ol-n">3</span> | **Code** | AgentScript source |
| <span class="ol-n">4</span> | **Network** | Open agent-network.yaml |
| <span class="ol-n">5</span> | **Preview** | Preview the result before you apply it |
| <span class="ol-n">6</span> | **New Version** | Bump the asset version |
| <span class="ol-n">7</span> | **Commit Version** | Bump the patch version in exchange.json and save all files |
| <span class="ol-n">8</span> | **Save** | Save the file (the YAML stays the source of truth) |
| <span class="ol-n">9</span> | **Add subagent** | Add a subagent step to the flow |
| <span class="ol-n">10</span> | **Subagent** | LLM loop that picks actions to complete a task |
| <span class="ol-n">11</span> | **Orchestrator** | LLM coordinating two or more agents / tools |
| <span class="ol-n">12</span> | **Generator** | Single LLM call, optional structured output |
| <span class="ol-n">13</span> | **Deterministic** | Deterministic: run actions, set variables (no LLM) |
| <span class="ol-n">14</span> | **Router** | Branch on conditions |
| <span class="ol-n">15</span> | **Reply** | Send a status message or artifact to the caller |
| <span class="ol-n">16</span> | **Collapse card** | Collapse or expand the card body |
| <span class="ol-n">17</span> | **Step** | Add next step |
| <span class="ol-n">18</span> | **Add node** | Add a step to the flow |
| <span class="ol-n">19</span> | **Auto layout** | Discard manual positions |
| <span class="ol-n">20</span> | **Minimize all** | Minimize all nodes to their icons (click an icon to open or minimize one). Auto layout packs them. |
| <span class="ol-n">21</span> | **Zoom out** | Zoom the canvas out |
| <span class="ol-n">22</span> | **43%** | Reset to 100% |
| <span class="ol-n">23</span> | **Zoom in** | Zoom the canvas in |
| <span class="ol-n">24</span> | **Fit to screen** | Fit all cards into the view |
| <span class="ol-n">25</span> | **Hide the minimap** | Show or hide the minimap |
| <span class="ol-n">26</span> | **Explain anything** | Explain anything: click, then click any object (the guided tour starts from here too). Drag to move; double-click to reset its place |

## Trigger

<div class="grid" markdown>

![card-trigger](../assets/ui/card-trigger-light.webp#only-light){ loading=lazy }
![card-trigger](../assets/ui/card-trigger-dark.webp#only-dark){ loading=lazy }

Entry point of the flow. Receives the A2A message for a broker interface and transitions to the first node.

**When to use it:** Exactly one per broker file.

</div>

**Examples and details:**

- Start with a generator that extracts ids from the message
- Go straight to a subagent for a simple assistant

??? note "In the file"

    ```text
    trigger mainTrigger:
      kind: "a2a"
      target: "brokers://my_broker/a2a"
      on_message: ->
        transition to @generator.extract
    ```

## Generator

<div class="grid" markdown>

![card-generator](../assets/ui/card-generator-light.webp#only-light){ loading=lazy }
![card-generator](../assets/ui/card-generator-dark.webp#only-dark){ loading=lazy }

One LLM call. With outputs.properties it returns typed fields (structured output); add enum to constrain values for a router.

**When to use it:** Extract ids, classify a request, summarize or rewrite text. No tools.

</div>

**Examples and details:**

- Extract order_id and reason from "Return ORD-1001, too small"
- Classify into "billing" | "shipping" | "other"
- Summarize a long complaint in two sentences

??? note "In the file"

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

<div class="grid" markdown>

![card-router](../assets/ui/card-router-light.webp#only-light){ loading=lazy }
![card-router](../assets/ui/card-router-dark.webp#only-dark){ loading=lazy }

Deterministic branch. Evaluates routes top to bottom and follows the first whose when condition is true; otherwise is the fallback.

**When to use it:** After a generator or subagent with structured outputs. Conditions use ==, != and and.

</div>

**Examples and details:**

- eligible == "yes" → create the RMA, otherwise explain
- case == "billing" → billing subagent
- risk == "high" and amount > 1000 → manual review

??? note "In the file"

    ```text
    router pick:
      routes:
        - target: @subagent.billing
          when: @generator.classify.output.case == "billing"
      otherwise:
        target: @subagent.general
    ```

## Subagent

<div class="grid" markdown>

![card-subagent](../assets/ui/card-subagent-light.webp#only-light){ loading=lazy }
![card-subagent](../assets/ui/card-subagent-dark.webp#only-dark){ loading=lazy }

An LLM loop that may call the actions you list (MCP tools or A2A agents) up to max_number_of_loops times, then returns text or structured outputs.

**When to use it:** A step needs judgment plus tools: look something up, ask a specialist agent, check a rule.

</div>

**Examples and details:**

- Tool gate: call check_eligibility, output eligible yes/no
- Delegate to a Refund agent
- Answer a question using a knowledge-base tool

## Orchestrator

Like a subagent, but meant to coordinate several agents and tools in one step, usually following numbered system instructions.

**When to use it:** Two or more agents or tools must be combined and the order can vary.

**Examples and details:**

- Record FNOL, check coverage, screen fraud, then decide
- Plan a trip with flight, hotel and policy agents

## Executor

<div class="grid" markdown>

![card-executor](../assets/ui/card-executor-light.webp#only-light){ loading=lazy }
![card-executor](../assets/ui/card-executor-dark.webp#only-dark){ loading=lazy }

Deterministic, no LLM. Runs actions with bound inputs (run @actions.x with a = expr) and sets variables.

**When to use it:** The inputs are known from earlier outputs and the call must happen exactly as written.

</div>

**Examples and details:**

- Create an RMA with order_id from the generator
- Refer a claim to SIU with a fixed reason
- Store a value in @variables

??? note "In the file"

    ```text
    executor createRma:
      do: ->
        run @actions.create_rma
          with order_id = @generator.extract.output.order_id
    ```

## Reply

<div class="grid" markdown>

![card-echo](../assets/ui/card-echo-light.webp#only-light){ loading=lazy }
![card-echo](../assets/ui/card-echo-dark.webp#only-dark){ loading=lazy }

Sends a status update or message to the caller and sets the task state (completed, failed, canceled, rejected). Every path must end in a terminal state: the CLI build rejects a branch that ends with input required.

**When to use it:** At the end of every path. To ask for missing details, reply completed with the question; the user answers in the next message.

</div>

**Examples and details:**

- Completed: "Refund RF-1001 issued"
- Completed with a question: "Which order do you mean?"
- Failed: "The order system is unavailable"
- Rejected: "I can't help with that"
