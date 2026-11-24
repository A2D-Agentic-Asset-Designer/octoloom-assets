# Tutorial: Utility Outage (fully mocked)

[All tutorials](../README.md) · [Getting started](../getting-started.md) · Deterministic network (Agent Network 2.0, AgentScript) · Use case · fully mocked

> A known outage gets status updates and a bill credit; an unknown one gets a ticket and a field crew. Three agents, two tool servers. Fully mocked: the LLM is an A²D LLM mock too, so no OpenAI key is needed.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 3 | 2 | 1.0, 0.3.0 | 0 | `v2-utility-outage` |

There are three ways to use this template:

1. **[Just use it](#path-1-just-use-it)**: create the project, deploy it and chat with it in about 10 minutes.
2. **[Learn step by step](#path-2-learn-step-by-step)**: the same steps, with what each part of the network does and how Octoloom shows it.
3. **[Build it from scratch](#path-3-build-it-from-scratch)**: start from a blank project and build the same network yourself, no code, one screenshot per step.

## Before you start

- VS Code with **Octoloom for Agent Fabric** installed (Marketplace), version 0.9.27 or later.
- An Anypoint organization with Agent Fabric, an environment, a [Small Managed Omni Gateway](https://octoloom.a2d-ai.com/start/gateway/) and a [connected app](https://octoloom.a2d-ai.com/start/connected-app/) (client ID and secret). New to Anypoint? **[Before you start](https://octoloom.a2d-ai.com/start/)** shows the trial account, the gateway, the connected app and connecting Octoloom, step by step with videos.
- No OpenAI key: the LLM is an A²D LLM mock as well (`a2dLlm.url`), with scripted answers for the Try it prompts.
- Nothing else: all agents, MCP servers and the LLM are public A²D mocks, so the network runs without any other system or key.

## Path 1: Just use it

1. **Home → Start → New Deterministic Network.** In the dialog pick **Use cases**, then the card **Utility Outage (fully mocked)**. Choose a folder and click **Create**.
2. **Deploy.** In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `a2dLlm.apiKey`: A2D LLM mock key (any value works)
3. **Chat.** When the status light is green, click **Open chat** and paste:
   - `No power at ADDR-31 since this morning`
   - `The lights flicker at ADDR-44`

Done. The rest of this page explains what you just ran.

## Path 2: Learn step by step

### Step 1. Connect Octoloom

Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. A²D isn't needed: the mock URLs are already the defaults in `exchange.json`. The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.

### Step 2. Create the project from the template

On **Home**, click **New Deterministic Network**. In **2 Start from**, choose **Use cases** and click **Utility Outage (fully mocked)**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `utility-outage` or type your own, pick the folder and click **Create**.

![New Project dialog with Utility Outage (fully mocked) selected](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/new-project.png)

Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md` and the broker flow in `brokers/`, and opens the canvas. Every id gets the template prefix `octo_uo2_`, so several templates can be deployed into one org side by side.

### Step 3. Read the network on the canvas

![Utility Outage (fully mocked) on the Deterministic network canvas](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/canvas.png)

Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).

- **Broker Outage Broker** (`octo_uo2_outage_broker`): its AgentScript flow decides every step.
- **Agent Customer Comms Agent**: Sends outage status updates to customers.
- **Agent Billing Credit Agent**: Applies bill credits for outages.
- **Agent Crew Dispatch Agent**: Dispatches field crews.
- **MCP server Grid MCP**: Known outages on the grid. Tools: `get_outage`.
- **MCP server Field Ticket MCP**: Field service tickets. Tools: `create_ticket`.

Try this on the canvas: use the zoom bar and the minimap, drag a card, or **Auto layout**. The layout is saved per file. **Minimize all** turns the cards into icon tiles. Click a connection line to see which broker uses which agent or tool.

### Step 4. Follow the broker flow (AgentScript)

Double-click the broker card (or open `brokers/outage-broker.agent`). The flow editor shows the AgentScript program that decides every step. The LLM only extracts fields and writes text, so the same input always takes the same branch.

![Utility Outage (fully mocked) broker flow](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/flow.png)

| Step | Kind | What it does |
|---|---|---|
| `outageBrokerTrigger` | Trigger | Starts the flow when an A2A message arrives at the broker. |
| `extractOutage` | Generator | Extracts the address id and the symptom. |
| `outageGate` | Subagent | Looks up known outages with the Grid MCP. |
| `outageRouter` | Router | Known outages get updates and a credit; new ones get a ticket and a crew. |
| `informCustomer` | Subagent | Enables status updates through the Customer Comms agent. |
| `offerCredit` | Subagent | Applies the outage bill credit through the Billing Credit agent. |
| `knownOutage` | Echo | Ends the flow with the `knownOutage` reply. |
| `createTicket` | Executor | Creates the field ticket. |
| `dispatchCrew` | Subagent | Dispatches a field crew. |
| `crewDispatched` | Echo | Ends the flow with the `crewDispatched` reply. |
| `progressExtractOutage` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressOutageGate` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressInformCustomer` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressOfferCredit` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressCreateTicket` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressDispatchCrew` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |

Click a step to edit it in the inspector. **+ Step** adds a node, and **+ Step → Patterns** inserts whole shapes such as retry, human in the loop or a guardrail check. **Code** shows the `.agent` text with completion.

### Step 5. Validate and build

In the canvas toolbar, open the CLI menu: **Validate** does a dry run of build, publish and deploy and lists problems in the Problems panel (click one to jump to the card). **Build** repairs and packages the project locally with anypoint-cli-v4.

The variables of this template (in `exchange.json`, open it for the no-code form):

| Variable | What | Default |
|---|---|---|
| `a2dLlm.url` | A2D LLM mock base URL (OpenAI-compatible) | `https://www.a2d-ai.com/api/platform/95a3d68c-3353-453d-9d4b-1d6ebec98e49/llm/v1` |
| `commsAgent.url` | Customer Comms Agent (A2D mock, A2A 1.0) URL | `https://www.a2d-ai.com/api/platform/b6db9afd-bd96-47e4-be74-3fd2d76070e8/a2a` |
| `creditAgent.url` | Billing Credit Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/aeee10e9-aca6-4cdd-b357-5565c35e42a3/a2a` |
| `crewAgent.url` | Crew Dispatch Agent (A2D mock, A2A 1.0) URL | `https://www.a2d-ai.com/api/platform/30d2929e-8970-4f62-a9c0-6ab74edd014d/a2a` |
| `gridMcp.url` | Grid MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/0162bf7a-b628-4631-974f-e2ae3737ecda/` |
| `fieldTicketMcp.url` | Field Ticket MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/6195b27b-2993-4800-98ce-c789473c1bf2/` |

### Step 6. Deploy

Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:

- `a2dLlm.apiKey`: A2D LLM mock key (any value works)

The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.

### Step 7. Chat with the broker

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. **Live progress** (the antenna button next to Send) is on by default: while the broker works, the chat lists its progress updates (*Extracting the address id and the symptom...*, *Looking up known outages with the Grid MCP...*) and keeps them above the answer. Paste the prompts one at a time:

![Utility Outage (fully mocked) in the broker chat](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/chat.png)

*The LLM is a scripted A²D LLM mock, so the broker gives the same answer every time; the ids in the table are checked by a live deploy.*

| Prompt | You should see |
|---|---|
| `No power at ADDR-31 since this morning` | Outage Gate: known outage OUT-778, back by 18:30. The Customer Comms Agent enables SMS updates and the Billing Credit Agent applies credit CR-31 (15.00 CHF). |
| `The lights flicker at ADDR-44` | Outage Gate: no known outage. Create Ticket runs `create_ticket` without the LLM, and the Crew Dispatch Agent sends crew C-12 (about 45 minutes). |



### Step 8. Trace a reply

Under each reply, the **Tracer** icon opens the task in the **Agent Network Tracer**: a waterfall of every call the broker made (gateway, broker, LLM, A2A agents, MCP tools) on one time axis, coloured like the cards. Errors are red. Click a span to see its request and response. The **Network** view shows the same reply as a sequence of calls.

### Step 9. Share it (optional)

The **Share** icon in the chat header opens the Share dialog. **A²D sessions** invites people by email to chat with this deployed broker and brings their passed / failed marks and comments back. **Local portal** generates a small web chat you can run or host anywhere.

## Path 3: Build it from scratch

Here you build the same network yourself, starting from a blank project. Every step uses a form, a menu or a button. You never import the template, and you never type YAML or AgentScript. The names below are the template's names without the `octo_uo2_` prefix. You can use your own names, but keep them consistent.

> The text fields take plain values. Where a value looks like `${group.name}`, type it as shown: it is a **variable** that `exchange.json` declares and that deploy fills in.

### Step 3.1. Create a blank project with a starter broker

Connect Octoloom first, as in [Path 2, Step 1](#step-1-connect-octoloom). Then, on **Home**, click **New Deterministic Network**. In **2 Start from**, choose **Blank** and turn on **Add a starter broker**.

- **Broker name**: `Outage Broker`
- **Name**: `utility-outage-scratch` (the Exchange asset id; a different name from the template, so both can live in one org)
- **Parent folder**: pick a folder, then click **Create blank project**.

![Blank project with a starter broker](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-new.png)

The starter broker `outage_broker` has an OpenAI LLM connection (`openai_connection`, MuleSoft's published OpenAI LLM) and a flow `brokers/outage-broker.agent` with a trigger, one subagent and the built-in `done` reply. This template doesn't use OpenAI: the next step replaces that LLM with the A²D LLM mock.

### Step 3.2. Switch the LLM to the A²D LLM mock

This template needs no OpenAI key: its LLM is an **A²D LLM mock** with scripted answers. Open the **Asset Palette** (Octoloom side bar), pick the **A²D** tab and the **LLMs** filter, then drag **Octoloom Utility Outage LLM** onto the broker card. The drop writes everything the LLM needs:

- the project LLM `a2d_octoloom_utility_outage_llm` (`registry.llms`) and its connection `a2d_octoloom_utility_outage_llm_connection` to the mock URL (no Exchange dependency);
- the variables `a2dOctoloomUtilityOutageLlm.url` (the mock URL) and `a2dOctoloomUtilityOutageLlm.apiKey` (the placeholder key `a2d-mock-key`, any value works) in `exchange.json`;
- the broker LLM: the flow's `default` model now targets `llm://a2d_octoloom_utility_outage_llm_connection` with the model `gpt-5-mini`.

Keep these names: the rest of this tutorial uses them. Then remove the starter OpenAI LLM: select its card (**openai**, below the broker) and click **Remove from network** (trash icon) in the inspector. It removes the OpenAI connection and its `exchange.json` dependency. The Problems bar then shows **Variable openai.apiKey is declared in exchange.json but not used**: click **Remove it**.

![The A²D LLM mock on the broker after the drop](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-llm.png)

### Step 3.3. Add the agents

On the canvas, click **+** (Add to the network) → **Agent** → **Empty**. The new agent opens in the inspector on the right. Fill it in, then repeat for each agent:

![The Add to the network menu with the Agent submenu](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-add.png)

- **Customer Comms Agent**
  - **Identity → Key**: `comms_agent`
  - **Info → Label**: Customer Comms Agent · **Description**: Sends outage status updates to customers.
  - **Metadata → Platform**: `AgentForce` (or click its icon under **Agent framework**)
  - **Interface**: click `a2a` (A2A 1.0). **Agent card (A2A 1.x)**: **Name** Customer Comms Agent, **Description** as above, **Supported interfaces → URL** `https://www.a2d-ai.com/api/platform/b6db9afd-bd96-47e4-be74-3fd2d76070e8/a2a`, Binding `JSONRPC`, Protocol version `1.0`
- **Billing Credit Agent**
  - **Identity → Key**: `credit_agent`
  - **Info → Label**: Billing Credit Agent · **Description**: Applies bill credits for outages.
  - **Metadata → Platform**: `MuleSoft` (or click its icon under **Agent framework**)
  - **Interface**: keep `a2a_v03` (A2A 0.3.0). **Agent card (A2A 0.3)**: **Name** Billing Credit Agent, **Description** as above, **URL** `https://www.a2d-ai.com/api/platform/aeee10e9-aca6-4cdd-b357-5565c35e42a3/a2a`
- **Crew Dispatch Agent**
  - **Identity → Key**: `crew_agent`
  - **Info → Label**: Crew Dispatch Agent · **Description**: Dispatches field crews.
  - **Metadata → Platform**: `Azure` (or click its icon under **Agent framework**)
  - **Interface**: click `a2a` (A2A 1.0). **Agent card (A2A 1.x)**: **Name** Crew Dispatch Agent, **Description** as above, **Supported interfaces → URL** `https://www.a2d-ai.com/api/platform/30d2929e-8970-4f62-a9c0-6ab74edd014d/a2a`, Binding `JSONRPC`, Protocol version `1.0`

![An agent in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-agent.png)

The card skills are optional. Once the agent has a connection (two steps on), the inspector offers **Read skills from the live agent**, which fills them from the running agent.

### Step 3.4. Add the MCP servers

Click **+** → **MCP server** → **Empty**, then fill in:

- **Grid MCP**: **Key** `grid_mcp`, **Label** Grid MCP, **Description** Known outages on the grid · **Protocol version** `2025-06-18`. The transport is already Streamable HTTP on `/mcp`.
- **Field Ticket MCP**: **Key** `field_ticket_mcp`, **Label** Field Ticket MCP, **Description** Field service tickets · **Protocol version** `2025-06-18`. The transport is already Streamable HTTP on `/mcp`.

### Step 3.5. Add the connections

A connection is the URL (and authentication) Agent Fabric uses to reach an agent or an MCP server. Click **+** → **Connection** → **Empty** once per agent and MCP server, and fill in:

| Key | Kind | Registry entry → Name | URL |
|---|---|---|---|
| `comms_agent_connection` | `a2a` | `comms_agent` | `${commsAgent.url}` |
| `credit_agent_connection` | `a2a` | `credit_agent` | `${creditAgent.url}` |
| `crew_agent_connection` | `a2a` | `crew_agent` | `${crewAgent.url}` |
| `grid_mcp_connection` | `mcp` | `grid_mcp` | `${gridMcp.url}` |
| `field_ticket_mcp_connection` | `mcp` | `field_ticket_mcp` | `${fieldTicketMcp.url}` |

![A connection in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-conn.png)

### Step 3.6. Declare the variables

The Problems bar now shows **Variable ${…} is not declared in exchange.json** for each new variable. Click **Add to exchange.json** on each one.

Then open `exchange.json` (it opens as a form) and, under **Variables**, set the defaults:

| Variable | Default |
|---|---|
| `commsAgent.url` | `https://www.a2d-ai.com/api/platform/b6db9afd-bd96-47e4-be74-3fd2d76070e8/a2a` |
| `creditAgent.url` | `https://www.a2d-ai.com/api/platform/aeee10e9-aca6-4cdd-b357-5565c35e42a3/a2a` |
| `crewAgent.url` | `https://www.a2d-ai.com/api/platform/30d2929e-8970-4f62-a9c0-6ab74edd014d/a2a` |
| `gridMcp.url` | `https://www.a2d-ai.com/api/platform/0162bf7a-b628-4631-974f-e2ae3737ecda/` |
| `fieldTicketMcp.url` | `https://www.a2d-ai.com/api/platform/6195b27b-2993-4800-98ce-c789473c1bf2/` |
| `a2dOctoloomUtilityOutageLlm.url` | `https://www.a2d-ai.com/api/platform/95a3d68c-3353-453d-9d4b-1d6ebec98e49/llm/v1` |


`a2dOctoloomUtilityOutageLlm.apiKey` keeps its default `a2d-mock-key` from the drop: the mock accepts any key, so deploy needs no real one.

![The exchange.json form with the variables](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-vars.png)

Also click **Remove it** on any **declared but not used** variable that the Problems bar shows.

### Step 3.7. Declare the MCP tools

On each MCP server card, click the **Tools** row (or its pencil). Octoloom reads the tool list from the running server: tick the tools below. You can also type a name in **Add a tool by name…**.

- **Grid MCP**: `get_outage`
- **Field Ticket MCP**: `create_ticket`

![The Tools row of an MCP server card](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-tools.png)

### Step 3.8. Link the agents and MCP servers to the broker

Every agent and MCP card now has a **Broker** row with **Link to Outage Broker**. Click it on each card. Octoloom adds the matching actions to the broker flow: one per agent and one per declared MCP tool.

![Link to the broker on the agent and MCP cards](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-link.png)

**Link to** also reads the required inputs from the tool schema. In the flow (next step), open **Connections** in the explorer and check that these actions show them under **Inputs** (one per line; type them if they are missing):
- `create_ticket`: `address_id: string`, `symptom: string`

### Step 3.9. Build the broker flow

On the broker card (or in its inspector), click **Open broker flow**. Then set up the flow:

1. **Settings → Language Settings**: on the `default` model, set **Reasoning effort (OpenAI)** to `MINIMAL` (the mock ignores it; it keeps the flow ready for a real model, like the template).
2. **Settings → System Messages**: set the instructions to: *You are the outage desk of a power utility. Send a crew only when the grid does not already know the outage.*
3. Select the `assistant` subagent and delete it (trash icon). The trigger and the built-in `done` reply stay.
4. Add the steps below in order. Select the step that comes before, click **Add node**, pick the kind and choose **Empty**, then set its **API name** in **General**. Octoloom wires each new step after the selected one, and you set the exact next step in the inspector.

![Add node in the flow editor](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-flow-add.png)

Select the trigger and, under **Go to**, pick `progressExtractOutage` once that step exists.

#### Generator `extractOutage`

- **Label** Extract Outage · **Description** Extracts the address id and the symptom.
- **System instructions**:

  > Extract the address id (for example ADDR-31) and a short symptom from the message.
  > Use "UNKNOWN" when no address id is present.

- **Prompt**:

  > {!@request.payload.message.parts[0].text}

- **Structured output** (**Add field** for each):
  - `address_id` (string): Address id, e.g. ADDR-31, or UNKNOWN
  - `symptom` (string): What the customer sees
- **Next step (on exit) → Go to**: `progressOutageGate`

#### Subagent `outageGate`

- **Label** Outage Gate · **Description** Looks up known outages with the Grid MCP.
- **System instructions**:

  > Call the outage tool for the address and report whether the outage is already known.
  > Set known to "yes" only when the tool returns known true.

- **Reasoning instructions**:

  > Address: {!@generator.extractOutage.output.address_id}. Report: {!@request.payload.message.parts[0].text}

- **Actions** (**+ Add action…**): `get_outage`
- **Limits → Max loops**: `3`
- **Structured output** (**Add field** for each):
  - `known` (string): Whether the outage is already known · **Allowed values** `yes`, `no`
  - `detail` (string): Outage detail from the tool
- **Next step (on exit) → Go to**: `outageRouter`

#### Router `outageRouter`

- **Description** Known outages get updates and a credit; new ones get a ticket and a crew.
- **Routes** (**+**): **Label** Known · **When** `@subagent.outageGate.output.known == "yes"` · **Go to** `progressInformCustomer`
- **Otherwise → Go to**: `progressCreateTicket`

#### Subagent `informCustomer`

- **Label** Inform Customer · **Description** Enables status updates through the Customer Comms agent.
- **Reasoning instructions**:

  > Enable outage updates for {!@generator.extractOutage.output.address_id}. Report: {!@request.payload.message.parts[0].text}

- **Actions** (**+ Add action…**): `comms_agent`
- **Next step (on exit) → Go to**: `progressOfferCredit`

#### Subagent `offerCredit`

- **Label** Offer Credit · **Description** Applies the outage bill credit through the Billing Credit agent.
- **Reasoning instructions**:

  > Apply the outage bill credit for {!@generator.extractOutage.output.address_id}. Report: {!@request.payload.message.parts[0].text}

- **Actions** (**+ Add action…**): `credit_agent`
- **Next step (on exit) → Go to**: `knownOutage`

#### Reply `knownOutage`

- **Use expression**, then **Message (expression)**: `"Known " + @subagent.outageGate.output.detail + ". " + @subagent.informCustomer.output + " " + @subagent.offerCredit.output`
- **Task state**: `TASK_STATE_COMPLETED`

#### Executor `createTicket`

- **Description** Creates the field ticket.
- **Steps (do)**: **Run action**
  - **Action** `create_ticket`
    - **Bind argument** `address_id` = `@generator.extractOutage.output.address_id`
    - **Bind argument** `symptom` = `@generator.extractOutage.output.symptom`
- **Next step (on exit) → Go to**: `progressDispatchCrew`

#### Subagent `dispatchCrew`

- **Label** Dispatch Crew · **Description** Dispatches a field crew.
- **Reasoning instructions**:

  > Send a field crew to {!@generator.extractOutage.output.address_id}: {!@generator.extractOutage.output.symptom}. Report: {!@request.payload.message.parts[0].text}

- **Actions** (**+ Add action…**): `crew_agent`
- **Next step (on exit) → Go to**: `crewDispatched`

#### Reply `crewDispatched`

- **Use expression**, then **Message (expression)**: `"New problem at " + @generator.extractOutage.output.address_id + ": a field ticket is open. " + @subagent.dispatchCrew.output`
- **Task state**: `TASK_STATE_COMPLETED`

#### Reply `progressExtractOutage`

- **Message text**: Extracting the address id and the symptom...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `extractOutage`

#### Reply `progressOutageGate`

- **Message text**: Looking up known outages with the Grid MCP...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `outageGate`

#### Reply `progressInformCustomer`

- **Message text**: Enabling status updates through the Customer Comms agent...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `informCustomer`

#### Reply `progressOfferCredit`

- **Message text**: Applying the outage bill credit through the Billing Credit agent...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `offerCredit`

#### Reply `progressCreateTicket`

- **Message text**: Creating the field ticket...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `createTicket`

#### Reply `progressDispatchCrew`

- **Message text**: Dispatching a field crew...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `dispatchCrew`

![The finished broker flow](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-utility-outage/img/scratch-flow.png)

When you are done, the flow matches the template's flow ([Path 2, Step 4](#step-4-follow-the-broker-flow-agentscript)). The built-in `done` reply isn't used by this use case. The Problems bar shows **echo done is not reachable from the trigger** as a warning, and you can leave it.

### Step 3.10. Validate, deploy and chat

Run **Validate** from the canvas CLI menu and fix anything in the Problems bar. Then follow Path 2 from [Validate and build](#step-5-validate-and-build) onwards: deploy (enter the secrets), wait for the green light, open the chat and send the same prompts. Your network answers like the template, because it is the same network, built by hand.

## What you learned

- How a deterministic network is built: an AgentScript flow decides every step; the LLM extracts and writes text.
- How the canvas, the inspector and the code view edit the same YAML.
- How to build the same network from a blank project with forms and menus only (Path 3).
- How to validate, build, deploy, chat and trace with Octoloom.

## Next

- Previous: [Event Ticketing (fully mocked)](../v2-event-ticketing/README.md)
- Next: [Warranty Repair (fully mocked)](../v2-warranty-repair/README.md)
- [All tutorials](../README.md)

---
Generated from the `v2-utility-outage` template (Octoloom `media/templates/v2-utility-outage`). Screenshots use fake data.
