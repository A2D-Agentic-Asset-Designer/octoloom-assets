# Tutorial: Event Ticketing (fully mocked)

[All tutorials](../README.md) · [Getting started](../getting-started.md) · Deterministic network (Agent Network 2.0, AgentScript) · Use case · fully mocked

> Extract the event, check availability, reserve the seats and issue the tickets, or join the waitlist. Fully mocked: the LLM is an A²D LLM mock too, so no OpenAI key is needed.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 2 | 2 | 0.3.0, 1.0 | 0 | `v2-event-ticketing` |

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

1. **Home → Start → New Deterministic Network.** In the dialog pick **Use cases**, then the card **Event Ticketing (fully mocked)**. Choose a folder and click **Create**.
2. **Deploy.** In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `a2dLlm.apiKey`: A2D LLM mock key (any value works)
3. **Chat.** When the status light is green, click **Open chat** and paste:
   - `Two tickets for event EV-501 please`
   - `Four seats for EV-502`

Done. The rest of this page explains what you just ran.

## Path 2: Learn step by step

### Step 1. Connect Octoloom

Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. A²D isn't needed: the mock URLs are already the defaults in `exchange.json`. The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.

### Step 2. Create the project from the template

On **Home**, click **New Deterministic Network**. In **2 Start from**, choose **Use cases** and click **Event Ticketing (fully mocked)**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `event-ticketing` or type your own, pick the folder and click **Create**.

![New Project dialog with Event Ticketing (fully mocked) selected](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/new-project.png)

Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md` and the broker flow in `brokers/`, and opens the canvas. Every id gets the template prefix `octo_et2_`, so several templates can be deployed into one org side by side.

### Step 3. Read the network on the canvas

![Event Ticketing (fully mocked) on the Deterministic network canvas](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/canvas.png)

Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).

- **Broker Ticketing Broker** (`octo_et2_ticketing_broker`): its AgentScript flow decides every step.
- **Agent Ticketing Agent**: Issues e-tickets for reserved seats.
- **Agent Waitlist Agent**: Puts customers on the waitlist of sold-out events.
- **MCP server Events MCP**: Event calendar and availability. Tools: `check_availability`.
- **MCP server Booking MCP**: Seat reservations. Tools: `reserve_seats`.

Try this on the canvas: use the zoom bar and the minimap, drag a card, or **Auto layout**. The layout is saved per file. **Minimize all** turns the cards into icon tiles. Click a connection line to see which broker uses which agent or tool.

### Step 4. Follow the broker flow (AgentScript)

Double-click the broker card (or open `brokers/ticketing-broker.agent`). The flow editor shows the AgentScript program that decides every step. The LLM only extracts fields and writes text, so the same input always takes the same branch.

![Event Ticketing (fully mocked) broker flow](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/flow.png)

| Step | Kind | What it does |
|---|---|---|
| `ticketingBrokerTrigger` | Trigger | Starts the flow when an A2A message arrives at the broker. |
| `extractBooking` | Generator | Extracts the event id and the number of seats. |
| `availabilityGate` | Subagent | Checks the free seats with the Events MCP. |
| `availabilityRouter` | Router | Free seats are reserved and ticketed; sold-out events go to the waitlist. |
| `reserveSeats` | Executor | Reserves the seats. |
| `issueTickets` | Subagent | Issues the e-tickets through the Ticketing agent. |
| `booked` | Echo | Ends the flow with the `booked` reply. |
| `joinWaitlist` | Subagent | Puts the customer on the waitlist. |
| `waitlisted` | Echo | Ends the flow with the `waitlisted` reply. |
| `progressExtractBooking` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressAvailabilityGate` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressReserveSeats` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressIssueTickets` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressJoinWaitlist` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |

Click a step to edit it in the inspector. **+ Step** adds a node, and **+ Step → Patterns** inserts whole shapes such as retry, human in the loop or a guardrail check. **Code** shows the `.agent` text with completion.

### Step 5. Validate and build

In the canvas toolbar, open the CLI menu: **Validate** does a dry run of build, publish and deploy and lists problems in the Problems panel (click one to jump to the card). **Build** repairs and packages the project locally with anypoint-cli-v4.

The variables of this template (in `exchange.json`, open it for the no-code form):

| Variable | What | Default |
|---|---|---|
| `a2dLlm.url` | A2D LLM mock base URL (OpenAI-compatible) | `https://www.a2d-ai.com/api/platform/31e90ff0-fafc-4029-9933-c5002fa9f2ea/llm/v1` |
| `ticketingAgent.url` | Ticketing Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/7fbe7677-8b25-4d43-b51a-e3169aaa56f9/a2a` |
| `waitlistAgent.url` | Waitlist Agent (A2D mock, A2A 1.0) URL | `https://www.a2d-ai.com/api/platform/1c6d5b32-bcdd-418a-959f-2eb48a95917b/a2a` |
| `eventsMcp.url` | Events MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/7809cb1b-39b8-41cf-aaaf-e0f2ff2838ed/` |
| `bookingMcp.url` | Booking MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/155023bf-2dc9-4e61-9020-6874a24c608c/` |

### Step 6. Deploy

Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:

- `a2dLlm.apiKey`: A2D LLM mock key (any value works)

The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.

### Step 7. Chat with the broker

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. **Live progress** (the antenna button next to Send) is on by default: while the broker works, the chat lists its progress updates (*Extracting the event id and the number of seats...*, *Checking the free seats with the Events MCP...*) and keeps them above the answer. Paste the prompts one at a time:

![Event Ticketing (fully mocked) in the broker chat](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/chat.png)

*The LLM is a scripted A²D LLM mock, so the broker gives the same answer every time; the ids in the table are checked by a live deploy.*

| Prompt | You should see |
|---|---|
| `Two tickets for event EV-501 please` | Availability Gate: 38 seats left. Reserve Seats runs `reserve_seats` without the LLM, and the Ticketing Agent sends TK-501-A1 and TK-501-A2. Reply starts with "Booked 2 seats for EV-501". |
| `Four seats for EV-502` | Availability Gate: sold out. The Waitlist Agent (A2A 1.0) adds you at position 3 (WL-502-19). |



### Step 8. Trace a reply

Under each reply, the **Tracer** icon opens the task in the **Agent Network Tracer**: a waterfall of every call the broker made (gateway, broker, LLM, A2A agents, MCP tools) on one time axis, coloured like the cards. Errors are red. Click a span to see its request and response. The **Network** view shows the same reply as a sequence of calls.

### Step 9. Share it (optional)

The **Share** icon in the chat header opens the Share dialog. **A²D sessions** invites people by email to chat with this deployed broker and brings their passed / failed marks and comments back. **Local portal** generates a small web chat you can run or host anywhere.

## Path 3: Build it from scratch

Here you build the same network yourself, starting from a blank project. Every step uses a form, a menu or a button. You never import the template, and you never type YAML or AgentScript. The names below are the template's names without the `octo_et2_` prefix. You can use your own names, but keep them consistent.

> The text fields take plain values. Where a value looks like `${group.name}`, type it as shown: it is a **variable** that `exchange.json` declares and that deploy fills in.

### Step 3.1. Create a blank project with a starter broker

Connect Octoloom first, as in [Path 2, Step 1](#step-1-connect-octoloom). Then, on **Home**, click **New Deterministic Network**. In **2 Start from**, choose **Blank** and turn on **Add a starter broker**.

- **Broker name**: `Ticketing Broker`
- **Name**: `event-ticketing-scratch` (the Exchange asset id; a different name from the template, so both can live in one org)
- **Parent folder**: pick a folder, then click **Create blank project**.

![Blank project with a starter broker](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-new.png)

The starter broker `ticketing_broker` has an OpenAI LLM connection (`openai_connection`, MuleSoft's published OpenAI LLM) and a flow `brokers/ticketing-broker.agent` with a trigger, one subagent and the built-in `done` reply. This template doesn't use OpenAI: the next step replaces that LLM with the A²D LLM mock.

### Step 3.2. Switch the LLM to the A²D LLM mock

This template needs no OpenAI key: its LLM is an **A²D LLM mock** with scripted answers. Open the **Asset Palette** (Octoloom side bar), pick the **A²D** tab and the **LLMs** filter, then drag **Octoloom Event Ticketing LLM** onto the broker card. The drop writes everything the LLM needs:

- the project LLM `a2d_octoloom_event_ticketing_llm` (`registry.llms`) and its connection `a2d_octoloom_event_ticketing_llm_connection` to the mock URL (no Exchange dependency);
- the variables `a2dOctoloomEventTicketingLlm.url` (the mock URL) and `a2dOctoloomEventTicketingLlm.apiKey` (the placeholder key `a2d-mock-key`, any value works) in `exchange.json`;
- the broker LLM: the flow's `default` model now targets `llm://a2d_octoloom_event_ticketing_llm_connection` with the model `gpt-5-mini`.

Keep these names: the rest of this tutorial uses them. Then remove the starter OpenAI LLM: select its card (**openai**, below the broker) and click **Remove from network** (trash icon) in the inspector. It removes the OpenAI connection and its `exchange.json` dependency. The Problems bar then shows **Variable openai.apiKey is declared in exchange.json but not used**: click **Remove it**.

![The A²D LLM mock on the broker after the drop](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-llm.png)

### Step 3.3. Add the agents

On the canvas, click **+** (Add to the network) → **Agent** → **Empty**. The new agent opens in the inspector on the right. Fill it in, then repeat for each agent:

![The Add to the network menu with the Agent submenu](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-add.png)

- **Ticketing Agent**
  - **Identity → Key**: `ticketing_agent`
  - **Info → Label**: Ticketing Agent · **Description**: Issues e-tickets for reserved seats.
  - **Metadata → Platform**: `MuleSoft` (or click its icon under **Agent framework**)
  - **Interface**: keep `a2a_v03` (A2A 0.3.0). **Agent card (A2A 0.3)**: **Name** Ticketing Agent, **Description** as above, **URL** `https://www.a2d-ai.com/api/platform/7fbe7677-8b25-4d43-b51a-e3169aaa56f9/a2a`
- **Waitlist Agent**
  - **Identity → Key**: `waitlist_agent`
  - **Info → Label**: Waitlist Agent · **Description**: Puts customers on the waitlist of sold-out events.
  - **Metadata → Platform**: `AgentForce` (or click its icon under **Agent framework**)
  - **Interface**: click `a2a` (A2A 1.0). **Agent card (A2A 1.x)**: **Name** Waitlist Agent, **Description** as above, **Supported interfaces → URL** `https://www.a2d-ai.com/api/platform/1c6d5b32-bcdd-418a-959f-2eb48a95917b/a2a`, Binding `JSONRPC`, Protocol version `1.0`

![An agent in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-agent.png)

The card skills are optional. Once the agent has a connection (two steps on), the inspector offers **Read skills from the live agent**, which fills them from the running agent.

### Step 3.4. Add the MCP servers

Click **+** → **MCP server** → **Empty**, then fill in:

- **Events MCP**: **Key** `events_mcp`, **Label** Events MCP, **Description** Event calendar and availability · **Protocol version** `2025-06-18`. The transport is already Streamable HTTP on `/mcp`.
- **Booking MCP**: **Key** `booking_mcp`, **Label** Booking MCP, **Description** Seat reservations · **Protocol version** `2025-06-18`. The transport is already Streamable HTTP on `/mcp`.

### Step 3.5. Add the connections

A connection is the URL (and authentication) Agent Fabric uses to reach an agent or an MCP server. Click **+** → **Connection** → **Empty** once per agent and MCP server, and fill in:

| Key | Kind | Registry entry → Name | URL |
|---|---|---|---|
| `ticketing_agent_connection` | `a2a` | `ticketing_agent` | `${ticketingAgent.url}` |
| `waitlist_agent_connection` | `a2a` | `waitlist_agent` | `${waitlistAgent.url}` |
| `events_mcp_connection` | `mcp` | `events_mcp` | `${eventsMcp.url}` |
| `booking_mcp_connection` | `mcp` | `booking_mcp` | `${bookingMcp.url}` |

![A connection in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-conn.png)

### Step 3.6. Declare the variables

The Problems bar now shows **Variable ${…} is not declared in exchange.json** for each new variable. Click **Add to exchange.json** on each one.

Then open `exchange.json` (it opens as a form) and, under **Variables**, set the defaults:

| Variable | Default |
|---|---|
| `ticketingAgent.url` | `https://www.a2d-ai.com/api/platform/7fbe7677-8b25-4d43-b51a-e3169aaa56f9/a2a` |
| `waitlistAgent.url` | `https://www.a2d-ai.com/api/platform/1c6d5b32-bcdd-418a-959f-2eb48a95917b/a2a` |
| `eventsMcp.url` | `https://www.a2d-ai.com/api/platform/7809cb1b-39b8-41cf-aaaf-e0f2ff2838ed/` |
| `bookingMcp.url` | `https://www.a2d-ai.com/api/platform/155023bf-2dc9-4e61-9020-6874a24c608c/` |
| `a2dOctoloomEventTicketingLlm.url` | `https://www.a2d-ai.com/api/platform/31e90ff0-fafc-4029-9933-c5002fa9f2ea/llm/v1` |


`a2dOctoloomEventTicketingLlm.apiKey` keeps its default `a2d-mock-key` from the drop: the mock accepts any key, so deploy needs no real one.

![The exchange.json form with the variables](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-vars.png)

Also click **Remove it** on any **declared but not used** variable that the Problems bar shows.

### Step 3.7. Declare the MCP tools

On each MCP server card, click the **Tools** row (or its pencil). Octoloom reads the tool list from the running server: tick the tools below. You can also type a name in **Add a tool by name…**.

- **Events MCP**: `check_availability`
- **Booking MCP**: `reserve_seats`

![The Tools row of an MCP server card](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-tools.png)

### Step 3.8. Link the agents and MCP servers to the broker

Every agent and MCP card now has a **Broker** row with **Link to Ticketing Broker**. Click it on each card. Octoloom adds the matching actions to the broker flow: one per agent and one per declared MCP tool.

![Link to the broker on the agent and MCP cards](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-link.png)

**Link to** also reads the required inputs from the tool schema. In the flow (next step), open **Connections** in the explorer and check that these actions show them under **Inputs** (one per line; type them if they are missing):
- `reserve_seats`: `event_id: string`, `seats: string`

### Step 3.9. Build the broker flow

On the broker card (or in its inspector), click **Open broker flow**. Then set up the flow:

1. **Settings → Language Settings**: on the `default` model, set **Reasoning effort (OpenAI)** to `MINIMAL` (the mock ignores it; it keeps the flow ready for a real model, like the template).
2. **Settings → System Messages**: set the instructions to: *You are the box office of a concert hall. Reserve seats only when the event has free seats.*
3. Select the `assistant` subagent and delete it (trash icon). The trigger and the built-in `done` reply stay.
4. Add the steps below in order. Select the step that comes before, click **Add node**, pick the kind and choose **Empty**, then set its **API name** in **General**. Octoloom wires each new step after the selected one, and you set the exact next step in the inspector.

![Add node in the flow editor](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-flow-add.png)

Select the trigger and, under **Go to**, pick `progressExtractBooking` once that step exists.

#### Generator `extractBooking`

- **Label** Extract Booking · **Description** Extracts the event id and the number of seats.
- **System instructions**:

  > Extract the event id (for example EV-501) and the number of seats from the message.
  > Use "UNKNOWN" when no event id is present.

- **Prompt**:

  > {!@request.payload.message.parts[0].text}

- **Structured output** (**Add field** for each):
  - `event_id` (string): Event id, e.g. EV-501, or UNKNOWN
  - `seats` (string): Number of seats
- **Next step (on exit) → Go to**: `progressAvailabilityGate`

#### Subagent `availabilityGate`

- **Label** Availability Gate · **Description** Checks the free seats with the Events MCP.
- **System instructions**:

  > Call the availability tool for the event and report whether seats are free.
  > Set available to "yes" only when the tool returns available true.

- **Reasoning instructions**:

  > Event: {!@generator.extractBooking.output.event_id}. Request: {!@request.payload.message.parts[0].text}

- **Actions** (**+ Add action…**): `check_availability`
- **Limits → Max loops**: `3`
- **Structured output** (**Add field** for each):
  - `available` (string): Whether seats are free · **Allowed values** `yes`, `no`
  - `detail` (string): Availability detail from the tool
- **Next step (on exit) → Go to**: `availabilityRouter`

#### Router `availabilityRouter`

- **Description** Free seats are reserved and ticketed; sold-out events go to the waitlist.
- **Routes** (**+**): **Label** Available · **When** `@subagent.availabilityGate.output.available == "yes"` · **Go to** `progressReserveSeats`
- **Otherwise → Go to**: `progressJoinWaitlist`

#### Executor `reserveSeats`

- **Description** Reserves the seats.
- **Steps (do)**: **Run action**
  - **Action** `reserve_seats`
    - **Bind argument** `event_id` = `@generator.extractBooking.output.event_id`
    - **Bind argument** `seats` = `@generator.extractBooking.output.seats`
- **Next step (on exit) → Go to**: `progressIssueTickets`

#### Subagent `issueTickets`

- **Label** Issue Tickets · **Description** Issues the e-tickets through the Ticketing agent.
- **Reasoning instructions**:

  > Issue the e-tickets for event {!@generator.extractBooking.output.event_id}, {!@generator.extractBooking.output.seats} seats. Request: {!@request.payload.message.parts[0].text}

- **Actions** (**+ Add action…**): `ticketing_agent`
- **Next step (on exit) → Go to**: `booked`

#### Reply `booked`

- **Use expression**, then **Message (expression)**: `"Booked " + @generator.extractBooking.output.seats + " seats for " + @generator.extractBooking.output.event_id + ". " + @subagent.issueTickets.output`
- **Task state**: `TASK_STATE_COMPLETED`

#### Subagent `joinWaitlist`

- **Label** Join Waitlist · **Description** Puts the customer on the waitlist.
- **Reasoning instructions**:

  > Event {!@generator.extractBooking.output.event_id} has no free seats: {!@subagent.availabilityGate.output.detail}. Add the customer to the waitlist. Request: {!@request.payload.message.parts[0].text}

- **Actions** (**+ Add action…**): `waitlist_agent`
- **Next step (on exit) → Go to**: `waitlisted`

#### Reply `waitlisted`

- **Use expression**, then **Message (expression)**: `"No seats left for " + @generator.extractBooking.output.event_id + " (" + @subagent.availabilityGate.output.detail + "). " + @subagent.joinWaitlist.output`
- **Task state**: `TASK_STATE_COMPLETED`

#### Reply `progressExtractBooking`

- **Message text**: Extracting the event id and the number of seats...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `extractBooking`

#### Reply `progressAvailabilityGate`

- **Message text**: Checking the free seats with the Events MCP...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `availabilityGate`

#### Reply `progressReserveSeats`

- **Message text**: Reserving the seats...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `reserveSeats`

#### Reply `progressIssueTickets`

- **Message text**: Issuing the e-tickets through the Ticketing agent...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `issueTickets`

#### Reply `progressJoinWaitlist`

- **Message text**: Putting the customer on the waitlist...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `joinWaitlist`

![The finished broker flow](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-event-ticketing/img/scratch-flow.png)

When you are done, the flow matches the template's flow ([Path 2, Step 4](#step-4-follow-the-broker-flow-agentscript)). The built-in `done` reply isn't used by this use case. The Problems bar shows **echo done is not reachable from the trigger** as a warning, and you can leave it.

### Step 3.10. Validate, deploy and chat

Run **Validate** from the canvas CLI menu and fix anything in the Problems bar. Then follow Path 2 from [Validate and build](#step-5-validate-and-build) onwards: deploy (enter the secrets), wait for the green light, open the chat and send the same prompts. Your network answers like the template, because it is the same network, built by hand.

## What you learned

- How a deterministic network is built: an AgentScript flow decides every step; the LLM extracts and writes text.
- How the canvas, the inspector and the code view edit the same YAML.
- How to build the same network from a blank project with forms and menus only (Path 3).
- How to validate, build, deploy, chat and trace with Octoloom.

## Next

- Previous: [Supply Chain Disruption](../v2-supply-chain/README.md)
- Next: [Utility Outage (fully mocked)](../v2-utility-outage/README.md)
- [All tutorials](../README.md)

---
Generated from the `v2-event-ticketing` template (Octoloom `media/templates/v2-event-ticketing`). Screenshots use fake data.
