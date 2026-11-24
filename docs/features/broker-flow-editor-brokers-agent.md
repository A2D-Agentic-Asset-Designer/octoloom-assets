<span class="ol-pill">Design</span>

# Broker flow editor

<p class="lede"><strong>The canvas of an AgentScript broker (`.agent`): trigger, generators, routers, subagents, orchestrators, executors and replies as a flow.</strong> Deterministic brokers follow a flow you can read: each step, each branch and each reply is visible and testable.</p>

!!! info "Where to find it"
    Open `brokers/*.agent` · **Flow** on a 2.0 broker card

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
| <span class="ol-n">16</span> | **Add node** | Add a step to the flow |
| <span class="ol-n">17</span> | **Auto layout** | Discard manual positions |
| <span class="ol-n">18</span> | **Minimize all** | Minimize all nodes to their icons (click an icon to open or minimize one). Auto layout packs them. |
| <span class="ol-n">19</span> | **Zoom out** | Zoom the canvas out |
| <span class="ol-n">20</span> | **27%** | Reset to 100% |
| <span class="ol-n">21</span> | **Zoom in** | Zoom the canvas in |
| <span class="ol-n">22</span> | **Fit to screen** | Fit all cards into the view |
| <span class="ol-n">23</span> | **Hide the minimap** | Show or hide the minimap |
| <span class="ol-n">24</span> | **Explain anything** | Explain anything: click, then click any object (the guided tour starts from here too). Drag to move; double-click to reset its place |

## How to use it

1. Use the **explorer** on the left for settings, variables, connections and the list of nodes; drag a node type from *Drag to canvas*.

2. Click **+ Step** on a node to add the next step, or **Patterns** for ready-made fragments.

    <figure markdown>
    ![+ Step → Patterns: ready-made flow fragments](../assets/ui/agent-patterns-light.webp#only-light){ loading=lazy }
    ![+ Step → Patterns: ready-made flow fragments](../assets/ui/agent-patterns-dark.webp#only-dark){ loading=lazy }
    <figcaption>+ Step → Patterns: ready-made flow fragments</figcaption>
    </figure>

3. Click a node to edit it in the inspector: instructions, tools, transitions, router conditions.

4. Add a **Reply** with task state *working* before a long step: with **Live** on, the chat shows it while the broker works.

5. Click **Save**; **Preview** shows the flow, **Commit Version** bumps the version.

## In detail

- Every subagent is a node, and transitions, routes and actions are edges.
- The outline lists agent settings, system messages, instructions, language settings and all subagents.
- Drag new nodes onto the canvas: Subagent, Orchestrator, Generator, Executor, Router, Reply.
- **+ Step** or right-click opens a multi-level menu: each node type has an empty entry and templates (structured extraction, classifier, yes/no branch, tool gate, run tool with bound inputs, completed/failed reply…). *Patterns* insert several wired nodes:
  - **Logical case selection**: generator with an enum output → router → one subagent per case.
  - **Check, then act** and **Extract, then run a tool**.
  - **Error handling**: a subagent with an `ok / failed` status → router → reply, or a FAILED reply with the error.
  - **Retry once, then fail**: a second attempt gets the first error as context. Flows have no loops, so the retry is bounded.
  - **Human in the loop**: a generator checks for missing details; when something is missing the reply is one question, answered in the next message.
  - **Guardrail check**: blocked requests end as REJECTED with a reason.

  Replies include Completed, Failed, Canceled and Rejected. Every path must end in a terminal state; the CLI rejects a branch that ends with input required.
- Executors and subagents / orchestrators can run both MCP tools and A2A agents (per the AgentScript reference); the action picker groups them by kind (MCP tools, A2A agents), explains each and suggests the bindings (`with message = ...` for A2A, tool inputs for MCP). Executors cannot slot-fill, so an A2A action run by an executor without `with message = ...` is flagged.
- Drag from an output port onto a card to connect it; click a connection to delete it. A node's type is fixed once created.
- A flow needs a trigger, at least one agent node (generator, subagent or orchestrator) and an echo node; Problems reports what is missing. `@kind.name` references to nodes that don't exist are reported too, as the CLI would.
- Removing a broker from the network offers to delete its `.agent` flow file (moved to the Trash, so you can restore it).
- Instruction fields (and v1 broker instructions) have an **Insert template** picker, with templates for error handling, retry, asking the user for missing details and guardrail screening.

- **Preview** (chat with the deployed broker; A2A 0.3.0 or 1.0 detected from its card, URL prefilled from the last deployment), **New Version** and **Commit Version** actions for AgentScript brokers.

## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### AgentScript flow

The canvas of one .agent file: its nodes (trigger, generator, router, sub-agent, orchestrator, executor, echo) and the paths between them. It edits the AgentScript text. A card lists the actions it calls: MCP tools under MCP actions (MCP icon) and agents (A2A) under Agent actions (agent icon); a card with no actions shows one empty Actions section. Hover an action chip to see the connection it goes through; in the inspector, click the connection name under an action to open the network canvas with that connection selected.

**When to use it:** Designing the behaviour of one agent.

<figure markdown>
![A 2.0 broker flow: explorer, nodes and transitions](../assets/ui/agent-flow-light.webp#only-light){ loading=lazy }
![A 2.0 broker flow: explorer, nodes and transitions](../assets/ui/agent-flow-dark.webp#only-dark){ loading=lazy }
<figcaption>A 2.0 broker flow: explorer, nodes and transitions</figcaption>
</figure>

**Examples and details:**

- Add a node from the palette on the left
- Select a node to edit it in the inspector
- Switch to the code view to see the AgentScript

### Trigger

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

### Generator

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

### Router

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

### Subagent

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

### Orchestrator

Like a subagent, but meant to coordinate several agents and tools in one step, usually following numbered system instructions.

**When to use it:** Two or more agents or tools must be combined and the order can vary.

<figure markdown>
![An orchestrator step on the broker flow canvas](../assets/ui/agent-flow-annot-light.webp#only-light){ loading=lazy }
![An orchestrator step on the broker flow canvas](../assets/ui/agent-flow-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>An orchestrator step on the broker flow canvas</figcaption>
</figure>

**Examples and details:**

- Record FNOL, check coverage, screen fraud, then decide
- Plan a trip with flight, hotel and policy agents

### Executor

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

### Reply

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

### Flow outline

<div class="grid" markdown>

![flow-explorer](../assets/ui/flow-explorer-light.webp#only-light){ loading=lazy }
![flow-explorer](../assets/ui/flow-explorer-dark.webp#only-dark){ loading=lazy }

The outline of the .agent file on the left: every node by kind, and the palette of nodes you can add.

**When to use it:** To find a node in a long flow or add a new one.

</div>

**Examples and details:**

- Click a node in the outline to select it on the canvas
- Drag a node kind from the palette onto the canvas

### Patterns

Patterns insert several wired nodes at once from + Step or the right-click menu: logical case selection, check then act, extract then run a tool, error handling (status output + failed reply), retry once then fail, human in the loop (ask one question when details are missing) and guardrail check (blocked requests end as rejected). Names are made unique and the last node links to the existing reply.

**When to use it:** You need a common flow shape: replace the placeholder instructions and conditions afterwards. Matching instruction templates (Error handling, Retry, Ask the user, Guardrail screen) are in the Insert template picker.

<figure markdown>
![+ Step → Patterns: ready-made flow fragments](../assets/ui/agent-patterns-light.webp#only-light){ loading=lazy }
![+ Step → Patterns: ready-made flow fragments](../assets/ui/agent-patterns-dark.webp#only-dark){ loading=lazy }
<figcaption>+ Step → Patterns: ready-made flow fragments</figcaption>
</figure>

**Examples and details:**

- Error handling: subagent status ok / failed → router → reply or FAILED with the error
- Retry once: attempt → router → second attempt with the first error → router → FAILED
- Human in the loop: generator complete yes / no → question reply or continue
- Guardrail check: generator allowed / blocked → REJECTED with reason or continue
