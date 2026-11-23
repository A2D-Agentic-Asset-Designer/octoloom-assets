# Tutorial: Fleet Maintenance (fully mocked)

[All tutorials](../README.md) · [Getting started](../getting-started.md) · Probabilistic network (Agent Network 1.0, LLM broker) · Use case · fully mocked

> A fleet broker checks telematics, orders parts, books the workshop and finds a replacement truck: two agents, four tool servers. Fully mocked: the LLM is an A²D LLM mock too, so no OpenAI key is needed.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 2 | 4 | 0.3.0 | 0 | `v1-fleet-maintenance` |

There are three ways to use this template:

1. **[Just use it](#path-1-just-use-it)**: create the project, deploy it and chat with it in about 10 minutes.
2. **[Learn step by step](#path-2-learn-step-by-step)**: the same steps, with what each part of the network does and how Octoloom shows it.
3. **[Build it from scratch](#path-3-build-it-from-scratch)**: start from a blank project and build the same network yourself, no code, one screenshot per step.

## Before you start

- VS Code with **Octoloom for Agent Fabric** installed (Marketplace), version 0.9.27 or later.
- An Anypoint organization with Agent Fabric, a connected app (client ID and secret), an environment and a Flex gateway.
- No OpenAI key: the LLM is an A²D LLM mock as well (`a2dLlm.url`), with scripted answers for the Try it prompts.
- Nothing else: all agents, MCP servers and the LLM are public A²D mocks, so the network runs without any other system or key.

## Path 1: Just use it

1. **Home → Start → New Probabilistic Network.** In the dialog pick **Use cases**, then the card **Fleet Maintenance (fully mocked)**. Choose a folder and click **Create**.
2. **Deploy.** In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `a2dLlm.apiKey`: A2D LLM mock key (any value works)
3. **Chat.** When the status light is green, click **Open chat** and paste:
   - `TRK-77 reports brake wear, get it fixed`
   - `Is TRK-77 still under warranty?`
   - `How much fuel budget is left for TRK-12?`

Done. The rest of this page explains what you just ran.

## Path 2: Learn step by step

### Step 1. Connect Octoloom

Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. A²D isn't needed: the mock URLs are already the defaults in `exchange.json`. The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.

### Step 2. Create the project from the template

On **Home**, click **New Probabilistic Network**. In **2 Start from**, choose **Use cases** and click **Fleet Maintenance (fully mocked)**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `fleet-maintenance` or type your own, pick the folder and click **Create**.

![New Project dialog with Fleet Maintenance (fully mocked) selected](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/new-project.png)

Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md`, and opens the canvas. Every id gets the template prefix `octo_fm1_`, so several templates can be deployed into one org side by side.

### Step 3. Read the network on the canvas

![Fleet Maintenance (fully mocked) on the Probabilistic network canvas](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/canvas.png)

Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).

- **Broker octo_fm1_fleet-broker** (`octo_fm1_fleet-broker`): the LLM decides which agent or tool to call from its instructions.
  - Instructions:
    - You keep a delivery fleet on the road.
    - For a repair, read the vehicle status first (for example TRK-77), check the part, book a workshop slot and ask the Dispatch agent for a replacement vehicle.
    - Use the Warranty agent for warranty questions and the fuel tools for fuel budgets.
    - Answer with the references and dates.
- **Agent Dispatch Agent**: Plans routes and replacement vehicles.
- **Agent Warranty Agent**: Knows the warranty terms of every vehicle.
- **MCP server Telematics MCP**: Live vehicle status. Tools: `get_vehicle_status`.
- **MCP server Parts MCP**: Spare parts stock. Tools: `check_part`.
- **MCP server Workshop MCP**: Workshop slots. Tools: `book_slot`.
- **MCP server Fuel MCP**: Fuel cards and budgets. Tools: `get_fuel_card`.

Try this on the canvas: use the zoom bar and the minimap, drag a card, or **Auto layout**. The layout is saved per file. **Minimize all** turns the cards into icon tiles. Click a connection line to see which broker uses which agent or tool.

### Step 4. Validate and build

In the canvas toolbar, open the CLI menu: **Validate** does a dry run of build, publish and deploy and lists problems in the Problems panel (click one to jump to the card). **Build** repairs and packages the project locally with anypoint-cli-v4.

The variables of this template (in `exchange.json`, open it for the no-code form):

| Variable | What | Default |
|---|---|---|
| `ingressgw.url` | Ingress gateway base URL (the broker is served under it) | (fill in) |
| `a2dLlm.url` | A2D LLM mock base URL (OpenAI-compatible) | `https://www.a2d-ai.com/api/platform/7044ccde-ce42-4a54-b123-db2e9bb98587/llm/v1` |
| `telematicsMcp.url` | Telematics MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/f3770ec2-ebc5-4422-9f38-765cea1af443/` |
| `partsMcp.url` | Parts MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/824ab59b-70b8-47e5-9f13-1f00e76ed915/` |
| `workshopMcp.url` | Workshop MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/894fc5b4-5682-41f5-bd2f-60e4328cb6cc/` |
| `fuelMcp.url` | Fuel MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/7049ba43-0e1f-4d5b-aa00-c6c8e8e385c1/` |
| `dispatchAgent.url` | Dispatch Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/96b57f4c-e1b8-4e17-ad3f-ce3fa13183aa/a2a` |
| `warrantyAgent.url` | Warranty Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/15aff66a-3290-40de-bda6-0aef81a72d70/a2a` |

### Step 5. Deploy

Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:

- `a2dLlm.apiKey`: A2D LLM mock key (any value works)

For a probabilistic network, also fill `ingressgw.url` in `exchange.json` (your ingress gateway base URL) before you deploy.

The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.

### Step 6. Chat with the broker

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. Paste the prompts one at a time:

![Fleet Maintenance (fully mocked) in the broker chat](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/chat.png)

*The LLM is a scripted A²D LLM mock, so the broker gives the same answer every time; the ids in the table are checked by a live deploy.*

| Prompt | You should see |
|---|---|
| `TRK-77 reports brake wear, get it fixed` | Four calls in a row: Telematics `get_vehicle_status` (brake pad wear 85%), Parts `check_part` (BP-4410 in stock), Workshop `book_slot` (WS-5521 on 2026-11-23, bay 2) and the Dispatch Agent (TRK-80 replaces TRK-77 on route R-14). |
| `Is TRK-77 still under warranty?` | The Warranty Agent: drivetrain until 2027-02-28, brake pads not covered. |
| `How much fuel budget is left for TRK-12?` | Fuel MCP `get_fuel_card`: FC-1212 used 615 of 800 CHF, 185 CHF left. |



### Step 7. Trace a reply

Under each reply, the **Tracer** icon opens the task in the **Agent Network Tracer**: a waterfall of every call the broker made (gateway, broker, LLM, A2A agents, MCP tools) on one time axis, coloured like the cards. Errors are red. Click a span to see its request and response. The **Network** view shows the same reply as a sequence of calls.

### Step 8. Share it (optional)

The **Share** icon in the chat header opens the Share dialog. **A²D sessions** invites people by email to chat with this deployed broker and brings their passed / failed marks and comments back. **Local portal** generates a small web chat you can run or host anywhere.

## Path 3: Build it from scratch

Here you build the same network yourself, starting from a blank project. Every step uses a form, a menu or a button. You never import the template, and you never type YAML. The names below are the template's names without the `octo_fm1_` prefix. You can use your own names, but keep them consistent.

> The text fields take plain values. Where a value looks like `${group.name}`, type it as shown: it is a **variable** that `exchange.json` declares and that deploy fills in.

### Step 3.1. Create a blank project with a starter broker

Connect Octoloom first, as in [Path 2, Step 1](#step-1-connect-octoloom). Then, on **Home**, click **New Probabilistic Network**. In **2 Start from**, choose **Blank** and turn on **Add a starter broker**.

- **Broker name**: `fleet-broker`
- **Name**: `fleet-maintenance-scratch` (the Exchange asset id; a different name from the template, so both can live in one org)
- **Parent folder**: pick a folder, then click **Create blank project**.

![Blank project with a starter broker](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/scratch-new.png)

The starter broker is an LLM broker with an OpenAI LLM (`openai` provider, `openai-connection`) and default instructions. This template doesn't use OpenAI: the next step replaces that LLM with the A²D LLM mock.

### Step 3.2. Switch the LLM to the A²D LLM mock

This template needs no OpenAI key: its LLM is an **A²D LLM mock** with scripted answers. Open the **Asset Palette** (Octoloom side bar), pick the **A²D** tab and the **LLMs** filter, then drag **Octoloom Fleet Maintenance LLM** onto the broker card. The drop writes everything the LLM needs:

- the project LLM `a2d-octoloom-fleet-maintenance-llm` (`llmProviders`) and its connection `a2d-octoloom-fleet-maintenance-llm-connection` to the mock URL (no Exchange dependency);
- the variables `a2dOctoloomFleetMaintenanceLlm.url` (the mock URL) and `a2dOctoloomFleetMaintenanceLlm.apiKey` (the placeholder key `a2d-mock-key`, any value works) in `exchange.json`;
- the broker LLM: the broker now uses the mock with its model `gpt-5-mini`.

Keep these names: the rest of this tutorial uses them. Then remove the starter OpenAI LLM: select its card (**OpenAI**, below the broker) and click **Remove from network** (trash icon) in the inspector. It removes the OpenAI connection. The Problems bar then shows **Variable openai.apiKey is declared in exchange.json but not used**: click **Remove it**.

![The A²D LLM mock on the broker after the drop](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/scratch-llm.png)

### Step 3.3. Add the agents

On the canvas, click **+** (Add to the network) → **Agent** → **Empty**. The new agent opens in the inspector on the right. Fill it in, then repeat for each agent:

![The Add to the network menu with the Agent submenu](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/scratch-add.png)

- **Dispatch Agent**
  - **Identity → Key**: `dispatch-agent`
  - **Label**: Dispatch Agent · **Description**: Plans routes and replacement vehicles.
  - **Metadata → Platform**: `MuleSoft` (or click its icon under **Agent framework**)
  - **Agent card**: **Name** Dispatch Agent, **Description** as above, **URL** `${dispatchAgent.url}`, **Protocol version** `0.3.0`
- **Warranty Agent**
  - **Identity → Key**: `warranty-agent`
  - **Label**: Warranty Agent · **Description**: Knows the warranty terms of every vehicle.
  - **Metadata → Platform**: `Snowflake` (or click its icon under **Agent framework**)
  - **Agent card**: **Name** Warranty Agent, **Description** as above, **URL** `${warrantyAgent.url}`, **Protocol version** `0.3.0`

![An agent in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/scratch-agent.png)

The card skills are optional. Once the agent has a connection (two steps on), the inspector offers **Read skills from the live agent**, which fills them from the running agent.

### Step 3.4. Add the MCP servers

Click **+** → **MCP server** → **Empty**, then fill in:

- **Telematics MCP**: **Key** `telematics-mcp`, **Label** Telematics MCP, **Description** Live vehicle status. The transport is already Streamable HTTP on `/mcp`.
- **Parts MCP**: **Key** `parts-mcp`, **Label** Parts MCP, **Description** Spare parts stock. The transport is already Streamable HTTP on `/mcp`.
- **Workshop MCP**: **Key** `workshop-mcp`, **Label** Workshop MCP, **Description** Workshop slots. The transport is already Streamable HTTP on `/mcp`.
- **Fuel MCP**: **Key** `fuel-mcp`, **Label** Fuel MCP, **Description** Fuel cards and budgets. The transport is already Streamable HTTP on `/mcp`.

### Step 3.5. Add the connections

A connection is the URL (and authentication) Agent Fabric uses to reach an agent or an MCP server. Click **+** → **Connection** → **Empty** once per agent and MCP server, and fill in:

| Key | Kind | Target → Name | URL |
|---|---|---|---|
| `telematics-mcp-connection` | `mcp` | `telematics-mcp` | `${telematicsMcp.url}` |
| `parts-mcp-connection` | `mcp` | `parts-mcp` | `${partsMcp.url}` |
| `workshop-mcp-connection` | `mcp` | `workshop-mcp` | `${workshopMcp.url}` |
| `fuel-mcp-connection` | `mcp` | `fuel-mcp` | `${fuelMcp.url}` |
| `dispatch-agent-connection` | `agent` | `dispatch-agent` | `${dispatchAgent.url}` |
| `warranty-agent-connection` | `agent` | `warranty-agent` | `${warrantyAgent.url}` |

![A connection in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/scratch-conn.png)

### Step 3.6. Declare the variables

The Problems bar now shows **Variable ${…} is not declared in exchange.json** for each new variable. Click **Add to exchange.json** on each one.

Then open `exchange.json` (it opens as a form) and, under **Variables**, set the defaults:

| Variable | Default |
|---|---|
| `ingressgw.url` | (your ingress gateway URL) |
| `telematicsMcp.url` | `https://www.a2d-ai.com/api/platform/f3770ec2-ebc5-4422-9f38-765cea1af443/` |
| `partsMcp.url` | `https://www.a2d-ai.com/api/platform/824ab59b-70b8-47e5-9f13-1f00e76ed915/` |
| `workshopMcp.url` | `https://www.a2d-ai.com/api/platform/894fc5b4-5682-41f5-bd2f-60e4328cb6cc/` |
| `fuelMcp.url` | `https://www.a2d-ai.com/api/platform/7049ba43-0e1f-4d5b-aa00-c6c8e8e385c1/` |
| `dispatchAgent.url` | `https://www.a2d-ai.com/api/platform/96b57f4c-e1b8-4e17-ad3f-ce3fa13183aa/a2a` |
| `warrantyAgent.url` | `https://www.a2d-ai.com/api/platform/15aff66a-3290-40de-bda6-0aef81a72d70/a2a` |
| `a2dOctoloomFleetMaintenanceLlm.url` | `https://www.a2d-ai.com/api/platform/7044ccde-ce42-4a54-b123-db2e9bb98587/llm/v1` |


`a2dOctoloomFleetMaintenanceLlm.apiKey` keeps its default `a2d-mock-key` from the drop: the mock accepts any key, so deploy needs no real one.

![The exchange.json form with the variables](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/scratch-vars.png)

### Step 3.7. Declare the MCP tools

On each MCP server card, click the **Tools** row (or its pencil). Octoloom reads the tool list from the running server: tick the tools below. You can also type a name in **Add a tool by name…**.

- **Telematics MCP**: `get_vehicle_status`
- **Parts MCP**: `check_part`
- **Workshop MCP**: `book_slot`
- **Fuel MCP**: `get_fuel_card`

![The Tools row of an MCP server card](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/scratch-tools.png)

### Step 3.8. Give the broker its agents and tools

Select the broker `fleet-broker`. In the inspector:

1. Click **Agents (0)**. In **Add existing agent…**, pick each agent and click **Add**: `dispatch-agent`, `warranty-agent`.
2. Click **MCP servers (0)**. Add each server with **Add existing MCP server…**, then tick its **Allowed tools**:
   - `telematics-mcp`: `get_vehicle_status`
   - `parts-mcp`: `check_part`
   - `workshop-mcp`: `book_slot`
   - `fuel-mcp`: `get_fuel_card`

![The MCP servers of the broker with their allowed tools](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/scratch-links.png)

### Step 3.9. Write the broker instructions

Back in the broker inspector, open **Instructions and limits**. Replace the default instruction with these entries, one per line:

- You keep a delivery fleet on the road.
- For a repair, read the vehicle status first (for example TRK-77), check the part, book a workshop slot and ask the Dispatch agent for a replacement vehicle.
- Use the Warranty agent for warranty questions and the fuel tools for fuel budgets.
- Answer with the references and dates.

Set **Max number of loops** `25`, **Max consecutive errors** `3` and **Task timeout (s)** `90`.

Optionally, fill the broker's **Agent card (A2A 0.3.0)** description: *A fleet broker checks telematics, orders parts, books the workshop and finds a replacement truck: two agents, four tool servers. Fully mocked: the LLM is an A²D LLM mock too, so no OpenAI key is needed.*

![The broker instructions and limits](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-fleet-maintenance/img/scratch-broker.png)

### Step 3.10. Validate, deploy and chat

Run **Validate** from the canvas CLI menu and fix anything in the Problems bar. Then follow Path 2 from [Validate and build](#step-4-validate-and-build) onwards: deploy (enter the secrets), wait for the green light, open the chat and send the same prompts. Your network answers like the template, because it is the same network, built by hand.

## What you learned

- How a probabilistic network is built: an LLM broker with instructions picks agents and MCP tools.
- How the canvas, the inspector and the code view edit the same YAML.
- How to build the same network from a blank project with forms and menus only (Path 3).
- How to validate, build, deploy, chat and trace with Octoloom.

## Next

- Previous: [Travel & Expense](../v1-travel-expense/README.md)
- Next: [Hotel Concierge (fully mocked)](../v1-hotel-concierge/README.md)
- [All tutorials](../README.md)

---
Generated from the `v1-fleet-maintenance` template (Octoloom `media/templates/v1-fleet-maintenance`). Screenshots use fake data.
