# Tutorial: Supply Chain Disruption: secured

[All tutorials](index.md) · [Getting started](../getting-started.md) · Deterministic network (Agent Network 2.0, AgentScript) · Technical · secured

> A late or short shipment is assessed against stock; severe delays are rerouted and customers told, other cases get a mitigation plan. Secured: authenticated connections (Basic, Client ID enforcement) with secret variables, the LLM behind a gateway URL, outbound message logging.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 4 | 3 | 1.0, 0.3.0 | 2 | `v2-supply-chain-secured` |

There are three ways to use this template:

1. **[Just use it](#path-1-just-use-it)**: create the project, deploy it and chat with it in about 10 minutes.
2. **[Learn step by step](#path-2-learn-step-by-step)**: the same steps, with what each part of the network does and how Octoloom shows it.
3. **[Build it from scratch](#path-3-build-it-from-scratch)**: start from a blank project and build the same network yourself, no code, one screenshot per step.

## Before you start

- VS Code with **Octoloom for Agent Fabric** installed (Marketplace), version 0.9.25 or later.
- An Anypoint organization with Agent Fabric, a connected app (client ID and secret), an environment and a Flex gateway.
- An OpenAI API key (or an OpenAI-compatible LLM gateway).
- Nothing else: all agents and MCP servers are public A²D mocks, so the network runs without any other system.

## Path 1: Just use it

1. **Home → Start → New Deterministic Network.** In the dialog pick **Technical**, then the card **Supply Chain Disruption: secured**. Choose a folder and click **Create**.
2. **Deploy.** In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: OpenAI API key (secret, injected at deploy time)
   - `supplierRiskAgent.password`: Password (secret, entered at deploy time)
   - `logisticsAgent.clientSecret`: Client secret (secret, entered at deploy time)
   - `buyerAgent.password`: Password (secret, entered at deploy time)
   - `customerCommsAgent.clientSecret`: Client secret (secret, entered at deploy time)
   - `shipmentsMcp.clientSecret`: Client secret (secret, entered at deploy time)
   - `inventoryMcp.password`: Password (secret, entered at deploy time)
   - `supplierMcp.clientSecret`: Client secret (secret, entered at deploy time)
3. **Chat.** When the status light is green, click **Open chat** and paste:
   - `Shipment SHP-4401 with SKU-778 is delayed 9 days at the port`
   - `Supplier reports a shortage of SKU-912 for shipment SHP-4402`
   - `Shipment SHP-4401 with SKU-778 is delayed 9 days at the port`

Done. The rest of this page explains what you just ran.

## Path 2: Learn step by step

### Step 1. Connect Octoloom

Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. A²D isn't needed: the mock URLs are already the defaults in `exchange.json`. The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.

### Step 2. Create the project from the template

On **Home**, click **New Deterministic Network**. In **2 Start from**, choose **Technical** and click **Supply Chain Disruption: secured**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `supply-chain-secured` or type your own, pick the folder and click **Create**.

![New Project dialog with Supply Chain Disruption: secured selected](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/new-project.png)

Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md` and the broker flow in `brokers/`, and opens the canvas. Every id gets the template prefix `octo_sc2s_`, so several templates can be deployed into one org side by side.

### Step 3. Read the network on the canvas

![Supply Chain Disruption: secured on the Deterministic network canvas](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/canvas.png)

Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).

- **Broker Disruption Broker** (`octo_sc2s_disruption_broker`): its AgentScript flow decides every step.
- **Agent Supplier Risk Agent**: Rates supplier reliability and alternatives.
- **Agent Logistics Agent**: Plans transport alternatives.
- **Agent Procurement Buyer Agent**: Places expedite and alternative purchase orders.
- **Agent Customer Communications Agent**: Informs affected customers about new delivery dates.
- **MCP server Shipments MCP**: Shipment tracking and rerouting. Tools: `get_shipment`, `reroute_shipment`.
- **MCP server Inventory MCP**: Stock levels per SKU. Tools: `get_stock`.
- **MCP server Supplier MCP**: Approved supplier catalogue. Tools: `find_alternative_supplier`.

Try this on the canvas: use the zoom bar and the minimap, drag a card, or **Auto layout**. The layout is saved per file. **Minimize all** turns the cards into icon tiles. Click a connection line to see which broker uses which agent or tool.

### Step 4. Follow the broker flow (AgentScript)

Double-click the broker card (or open `brokers/disruption-broker.agent`). The flow editor shows the AgentScript program that decides every step. The LLM only extracts fields and writes text, so the same input always takes the same branch.

![Supply Chain Disruption: secured broker flow](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/flow.png)

| Step | Kind | What it does |
|---|---|---|
| `disruptionBrokerTrigger` | Trigger | Starts the flow when an A2A message arrives at the broker. |
| `extractDisruption` | Generator | Extracts the shipment id and the kind of disruption. |
| `assessImpact` | Subagent | Reads the shipment and the stock cover of its SKU and rates the impact. |
| `mitigationRouter` | Router | Severe delays are rerouted, shortages get a new supplier, the rest a plan. |
| `reroute` | Executor | Switches the shipment to a faster mode (no LLM). |
| `informCustomers` | Subagent | Tells the affected customers the new date. |
| `resource` | Orchestrator | Finds an alternative supplier, checks its risk and places the order. |
| `mitigationPlan` | Subagent | Stock covers the delay: proposes a plan with the logistics agent. |
| `rerouted` | Echo | Ends the flow with the `rerouted` reply. |
| `resourced` | Echo | Ends the flow with the `resourced` reply. |
| `planned` | Echo | Ends the flow with the `planned` reply. |
| `progressExtractDisruption` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressAssessImpact` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressReroute` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressInformCustomers` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressResource` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |
| `progressMitigationPlan` | Echo | Progress update (`TASK_STATE_WORKING`): tells the caller what comes next, then goes on to that step. With **Live** on, the chat shows it while the broker works. |

Click a step to edit it in the inspector. **+ Step** adds a node, and **+ Step → Patterns** inserts whole shapes such as retry, human in the loop or a guardrail check. **Code** shows the `.agent` text with completion.

### Step 5. See the secured connections

This variant adds Agent Fabric policies. Open a broker or connection and look at its **Policies** section. Each policy folds open to show its configuration:
- `message-logging-outbound`
- `rate-limiting`

Secured: every agent and MCP connection authenticates (Basic or Client ID enforcement, alternating). User names and client ids are variables, passwords and client secrets are secret variables asked for at deploy time. The LLM URL is the variable `llmGateway.url` (api.openai.com by default, or your LLM gateway). Upstream calls are logged with the outbound Message Logging policy. Policies: message-logging-outbound, rate-limiting.

Open a connection card. Its **Authentication** section shows the kind (Basic, Client ID enforcement and so on). Names and client IDs are normal variables; passwords and secrets are **secret variables** that Octoloom asks for at deploy time and never stores.

Run **Governance** (shield icon in the canvas toolbar) to check the project against the Agent Fabric rulesets. It runs locally, and findings show on the cards with **Fix** where one exists.

### Step 6. Validate and build

In the canvas toolbar, open the CLI menu: **Validate** does a dry run of build, publish and deploy and lists problems in the Problems panel (click one to jump to the card). **Build** repairs and packages the project locally with anypoint-cli-v4.

The variables of this template (in `exchange.json`, open it for the no-code form):

| Variable | What | Default |
|---|---|---|
| `llmGateway.url` | OpenAI-compatible LLM endpoint: api.openai.com or your LLM gateway in front of it | `https://api.openai.com/v1` |
| `supplierRiskAgent.url` | Supplier Risk Agent (A2D mock, A2A 1.0) URL | `https://www.a2d-ai.com/api/platform/a0a7350b-dbd8-42de-ad71-bff62486e0f9/a2a` |
| `supplierRiskAgent.username` | User name for Basic authentication | `octoloom-demo` |
| `logisticsAgent.url` | Logistics Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/98d5b94b-db87-4ebc-9b1c-e6259e810fec/a2a` |
| `logisticsAgent.clientId` | Client ID for Client ID Enforcement | `octoloom-demo-client` |
| `buyerAgent.url` | Procurement Buyer Agent (A2D mock, A2A 1.0) URL | `https://www.a2d-ai.com/api/platform/a2cf5661-5b77-415b-a071-41c19de7c31b/a2a` |
| `buyerAgent.username` | User name for Basic authentication | `octoloom-demo` |
| `customerCommsAgent.url` | Customer Communications Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/9dcf701b-2dd0-4b19-a1d8-18435a4eac49/a2a` |
| `customerCommsAgent.clientId` | Client ID for Client ID Enforcement | `octoloom-demo-client` |
| `shipmentsMcp.url` | Shipments MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/55dce81c-8a2b-44cf-ad5f-26ed16363dfd/` |
| `shipmentsMcp.clientId` | Client ID for Client ID Enforcement | `octoloom-demo-client` |
| `inventoryMcp.url` | Inventory MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/e821f794-fba0-438e-aee1-b2391abfeb37/` |
| `inventoryMcp.username` | User name for Basic authentication | `octoloom-demo` |
| `supplierMcp.url` | Supplier MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/df692006-f8d9-46f7-8d6b-08a1cc265dd8/` |
| `supplierMcp.clientId` | Client ID for Client ID Enforcement | `octoloom-demo-client` |

### Step 7. Deploy

Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:

- `openai.apiKey`: OpenAI API key (secret, injected at deploy time)
- `supplierRiskAgent.password`: Password (secret, entered at deploy time)
- `logisticsAgent.clientSecret`: Client secret (secret, entered at deploy time)
- `buyerAgent.password`: Password (secret, entered at deploy time)
- `customerCommsAgent.clientSecret`: Client secret (secret, entered at deploy time)
- `shipmentsMcp.clientSecret`: Client secret (secret, entered at deploy time)
- `inventoryMcp.password`: Password (secret, entered at deploy time)
- `supplierMcp.clientSecret`: Client secret (secret, entered at deploy time)

The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.

### Step 8. Chat with the broker

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. **Live progress** (the antenna button next to Send) is on by default: while the broker works, the chat lists its progress updates (*Extracting the shipment id and the kind of disruption...*, *Reading the shipment and the stock cover of its SKU, rating the impact...*) and keeps them above the answer. Paste the prompts one at a time:

![Supply Chain Disruption: secured in the broker chat](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/chat.png)

*The reply in the screenshot is an illustration: it shows what the broker answers. The real wording changes from run to run.*

| Prompt | You should see |
|---|---|
| `Shipment SHP-4401 with SKU-778 is delayed 9 days at the port` | Shipments `get_shipment`, Inventory `get_stock`: 4 days of cover, shorter than the delay. Logistics `reroute_shipment` to rail, ETA 2026-11-21, +2,300 EUR. Customer Communications informs 12 customers. |
| `Supplier reports a shortage of SKU-912 for shipment SHP-4402` | Inventory: 21 days of cover. Supplier Risk: SUP-12 is high risk; `find_alternative_supplier`: SUP-31 in 5 days at +4%. Buyer places PO-66120 for 4,000 units, delivery 2026-11-18. |
| `Shipment SHP-4401 with SKU-778 is delayed 9 days at the port` | Same answer as the plain variant: the A²D mocks accept any credentials. The Tracer shows each authenticated upstream call, and the outbound Message Logging policy writes one log line per call. |

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.

### Step 9. Trace a reply

Under each reply, the **Tracer** icon opens the task in the **Agent Network Tracer**: a waterfall of every call the broker made (gateway, broker, LLM, A2A agents, MCP tools) on one time axis, coloured like the cards. Errors are red. Click a span to see its request and response. The **Network** view shows the same reply as a sequence of calls.

### Step 10. Share it (optional)

The **Share** icon in the chat header opens the Share dialog. **A²D sessions** invites people by email to chat with this deployed broker and brings their passed / failed marks and comments back. **Local portal** generates a small web chat you can run or host anywhere.

## Path 3: Build it from scratch

Here you build the same network yourself, starting from a blank project. Every step uses a form, a menu or a button. You never import the template, and you never type YAML or AgentScript. The names below are the template's names without the `octo_sc2s_` prefix. You can use your own names, but keep them consistent.

> The text fields take plain values. Where a value looks like `${group.name}`, type it as shown: it is a **variable** that `exchange.json` declares and that deploy fills in.

### Step 3.1. Create a blank project with a starter broker

Connect Octoloom first, as in [Path 2, Step 1](#step-1-connect-octoloom). Then, on **Home**, click **New Deterministic Network**. In **2 Start from**, choose **Blank** and turn on **Add a starter broker**.

- **Broker name**: `Disruption Broker`
- **Name**: `supply-chain-secured-scratch` (the Exchange asset id; a different name from the template, so both can live in one org)
- **Parent folder**: pick a folder, then click **Create blank project**.

![Blank project with a starter broker](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-new.png)

The starter broker `disruption_broker` has an OpenAI LLM connection (`openai_connection`, MuleSoft's published OpenAI LLM) and a flow `brokers/disruption-broker.agent` with a trigger, one subagent and the built-in `done` reply. The LLM is already done.

### Step 3.2. Add the agents

On the canvas, click **+** (Add to the network) → **Agent** → **Empty**. The new agent opens in the inspector on the right. Fill it in, then repeat for each agent:

![The Add to the network menu with the Agent submenu](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-add.png)

- **Supplier Risk Agent**
  - **Identity → Key**: `supplier_risk_agent`
  - **Info → Label**: Supplier Risk Agent · **Description**: Rates supplier reliability and alternatives.
  - **Metadata → Platform**: `Snowflake` (or click its icon under **Agent framework**)
  - **Interface**: click `a2a` (A2A 1.0). **Agent card (A2A 1.x)**: **Name** Supplier Risk Agent, **Description** as above, **Supported interfaces → URL** `https://www.a2d-ai.com/api/platform/a0a7350b-dbd8-42de-ad71-bff62486e0f9/a2a`, Binding `JSONRPC`, Protocol version `1.0`
- **Logistics Agent**
  - **Identity → Key**: `logistics_agent`
  - **Info → Label**: Logistics Agent · **Description**: Plans transport alternatives.
  - **Metadata → Platform**: `MuleSoft` (or click its icon under **Agent framework**)
  - **Interface**: keep `a2a_v03` (A2A 0.3.0). **Agent card (A2A 0.3)**: **Name** Logistics Agent, **Description** as above, **URL** `https://www.a2d-ai.com/api/platform/98d5b94b-db87-4ebc-9b1c-e6259e810fec/a2a`
- **Procurement Buyer Agent**
  - **Identity → Key**: `buyer_agent`
  - **Info → Label**: Procurement Buyer Agent · **Description**: Places expedite and alternative purchase orders.
  - **Metadata → Platform**: `AgentForce` (or click its icon under **Agent framework**)
  - **Interface**: click `a2a` (A2A 1.0). **Agent card (A2A 1.x)**: **Name** Procurement Buyer Agent, **Description** as above, **Supported interfaces → URL** `https://www.a2d-ai.com/api/platform/a2cf5661-5b77-415b-a071-41c19de7c31b/a2a`, Binding `JSONRPC`, Protocol version `1.0`
- **Customer Communications Agent**
  - **Identity → Key**: `customer_comms_agent`
  - **Info → Label**: Customer Communications Agent · **Description**: Informs affected customers about new delivery dates.
  - **Metadata → Platform**: `Vertex` (or click its icon under **Agent framework**)
  - **Interface**: keep `a2a_v03` (A2A 0.3.0). **Agent card (A2A 0.3)**: **Name** Customer Communications Agent, **Description** as above, **URL** `https://www.a2d-ai.com/api/platform/9dcf701b-2dd0-4b19-a1d8-18435a4eac49/a2a`

![An agent in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-agent.png)

The card skills are optional. Once the agent has a connection (two steps on), the inspector offers **Read skills from the live agent**, which fills them from the running agent.

### Step 3.3. Add the MCP servers

Click **+** → **MCP server** → **Empty**, then fill in:

- **Shipments MCP**: **Key** `shipments_mcp`, **Label** Shipments MCP, **Description** Shipment tracking and rerouting · **Protocol version** `2025-06-18`. The transport is already Streamable HTTP on `/mcp`.
- **Inventory MCP**: **Key** `inventory_mcp`, **Label** Inventory MCP, **Description** Stock levels per SKU · **Protocol version** `2025-06-18`. The transport is already Streamable HTTP on `/mcp`.
- **Supplier MCP**: **Key** `supplier_mcp`, **Label** Supplier MCP, **Description** Approved supplier catalogue · **Protocol version** `2025-06-18`. The transport is already Streamable HTTP on `/mcp`.

### Step 3.4. Add the connections

A connection is the URL (and authentication) Agent Fabric uses to reach an agent or an MCP server. Click **+** → **Connection** → **Empty** once per agent and MCP server, and fill in:

| Key | Kind | Registry entry → Name | URL |
|---|---|---|---|
| `supplier_risk_agent_connection` | `a2a` | `supplier_risk_agent` | `${supplierRiskAgent.url}` |
| `logistics_agent_connection` | `a2a` | `logistics_agent` | `${logisticsAgent.url}` |
| `buyer_agent_connection` | `a2a` | `buyer_agent` | `${buyerAgent.url}` |
| `customer_comms_agent_connection` | `a2a` | `customer_comms_agent` | `${customerCommsAgent.url}` |
| `shipments_mcp_connection` | `mcp` | `shipments_mcp` | `${shipmentsMcp.url}` |
| `inventory_mcp_connection` | `mcp` | `inventory_mcp` | `${inventoryMcp.url}` |
| `supplier_mcp_connection` | `mcp` | `supplier_mcp` | `${supplierMcp.url}` |

![A connection in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-conn.png)

These connections also authenticate. In **Authentication**, pick the kind and type the values exactly as shown. The values are variables, and the secret ones are asked for at deploy time:

- `supplier_risk_agent_connection`: **Basic (username / password)**, **username** `${supplierRiskAgent.username}`, **password** `${supplierRiskAgent.password}`
- `logistics_agent_connection`: **Client ID enforcement (client_id / client_secret headers)**, **clientId** `${logisticsAgent.clientId}` (header `client_id`), **clientSecret** `${logisticsAgent.clientSecret}` (header `client_secret`)
- `buyer_agent_connection`: **Basic (username / password)**, **username** `${buyerAgent.username}`, **password** `${buyerAgent.password}`
- `customer_comms_agent_connection`: **Client ID enforcement (client_id / client_secret headers)**, **clientId** `${customerCommsAgent.clientId}` (header `client_id`), **clientSecret** `${customerCommsAgent.clientSecret}` (header `client_secret`)
- `shipments_mcp_connection`: **Client ID enforcement (client_id / client_secret headers)**, **clientId** `${shipmentsMcp.clientId}` (header `client_id`), **clientSecret** `${shipmentsMcp.clientSecret}` (header `client_secret`)
- `inventory_mcp_connection`: **Basic (username / password)**, **username** `${inventoryMcp.username}`, **password** `${inventoryMcp.password}`
- `supplier_mcp_connection`: **Client ID enforcement (client_id / client_secret headers)**, **clientId** `${supplierMcp.clientId}` (header `client_id`), **clientSecret** `${supplierMcp.clientSecret}` (header `client_secret`)

### Step 3.5. Declare the variables

The Problems bar now shows **Variable ${…} is not declared in exchange.json** for each new variable. Click **Add to exchange.json** on each one.

Then open `exchange.json` (it opens as a form) and, under **Variables**, set the defaults:

| Variable | Default |
|---|---|
| `llmGateway.url` | `https://api.openai.com/v1` |
| `supplierRiskAgent.url` | `https://www.a2d-ai.com/api/platform/a0a7350b-dbd8-42de-ad71-bff62486e0f9/a2a` |
| `supplierRiskAgent.username` | `octoloom-demo` |
| `logisticsAgent.url` | `https://www.a2d-ai.com/api/platform/98d5b94b-db87-4ebc-9b1c-e6259e810fec/a2a` |
| `logisticsAgent.clientId` | `octoloom-demo-client` |
| `buyerAgent.url` | `https://www.a2d-ai.com/api/platform/a2cf5661-5b77-415b-a071-41c19de7c31b/a2a` |
| `buyerAgent.username` | `octoloom-demo` |
| `customerCommsAgent.url` | `https://www.a2d-ai.com/api/platform/9dcf701b-2dd0-4b19-a1d8-18435a4eac49/a2a` |
| `customerCommsAgent.clientId` | `octoloom-demo-client` |
| `shipmentsMcp.url` | `https://www.a2d-ai.com/api/platform/55dce81c-8a2b-44cf-ad5f-26ed16363dfd/` |
| `shipmentsMcp.clientId` | `octoloom-demo-client` |
| `inventoryMcp.url` | `https://www.a2d-ai.com/api/platform/e821f794-fba0-438e-aee1-b2391abfeb37/` |
| `inventoryMcp.username` | `octoloom-demo` |
| `supplierMcp.url` | `https://www.a2d-ai.com/api/platform/df692006-f8d9-46f7-8d6b-08a1cc265dd8/` |
| `supplierMcp.clientId` | `octoloom-demo-client` |

Leave the secret variables (`openai.apiKey`, `supplierRiskAgent.password`, `logisticsAgent.clientSecret`, `buyerAgent.password`, `customerCommsAgent.clientSecret`, `shipmentsMcp.clientSecret`, `inventoryMcp.password`, `supplierMcp.clientSecret`) empty: deploy asks for them and never stores them.

![The exchange.json form with the variables](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-vars.png)

Also click **Remove it** on any **declared but not used** variable that the Problems bar shows.

### Step 3.6. Declare the MCP tools

On each MCP server card, click the **Tools** row (or its pencil). Octoloom reads the tool list from the running server: tick the tools below. You can also type a name in **Add a tool by name…**.

- **Shipments MCP**: `get_shipment`, `reroute_shipment`
- **Inventory MCP**: `get_stock`
- **Supplier MCP**: `find_alternative_supplier`

![The Tools row of an MCP server card](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-tools.png)

### Step 3.7. Link the agents and MCP servers to the broker

Every agent and MCP card now has a **Broker** row with **Link to Disruption Broker**. Click it on each card. Octoloom adds the matching actions to the broker flow: one per agent and one per declared MCP tool.

![Link to the broker on the agent and MCP cards](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-link.png)

**Link to** also reads the required inputs from the tool schema. In the flow (next step), open **Connections** in the explorer and check that these actions show them under **Inputs** (one per line; type them if they are missing):
- `reroute_shipment`: `shipment_id: string`

### Step 3.8. Build the broker flow

On the broker card (or in its inspector), click **Open broker flow**. Then set up the flow:

1. **Settings → Language Settings**: on the `default` model, set **Reasoning effort (OpenAI)** to `MINIMAL`.
2. **Settings → System Messages**: set the instructions to: *You are the supply chain control tower. Decide from shipment and stock data, never from guesses.*
3. Select the `assistant` subagent and delete it (trash icon). The trigger and the built-in `done` reply stay.
4. Add the steps below in order. Select the step that comes before, click **Add node**, pick the kind and choose **Empty**, then set its **API name** in **General**. Octoloom wires each new step after the selected one, and you set the exact next step in the inspector.

![Add node in the flow editor](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-flow-add.png)

Select the trigger and, under **Go to**, pick `progressExtractDisruption` once that step exists.

#### Generator `extractDisruption`

- **Label** Extract Disruption · **Description** Extracts the shipment id and the kind of disruption.
- **System instructions**:

  > Extract the shipment id (for example SHP-4401) and classify the disruption.
  > Kind is "delay" for late shipments and "shortage" when the supplier cannot deliver the quantity.

- **Prompt**:

  > {!@request.payload.message.parts[0].text}

- **Structured output** (**Add field** for each):
  - `shipment_id` (string): Shipment id, e.g. SHP-4401
  - `kind` (string): Kind of disruption · **Allowed values** `delay`, `shortage`
- **Next step (on exit) → Go to**: `progressAssessImpact`

#### Subagent `assessImpact`

- **Label** Assess Impact · **Description** Reads the shipment and the stock cover of its SKU and rates the impact.
- **System instructions**:

  > Get the shipment, then the stock of its SKU.
  > Severity is "severe" when the delay in days is larger than the days of cover, otherwise "manageable".

- **Reasoning instructions**:

  > Shipment {!@generator.extractDisruption.output.shipment_id}, kind {!@generator.extractDisruption.output.kind}.

- **Actions** (**+ Add action…**): `get_shipment`, `get_stock`
- **Limits → Max loops**: `4`
- **Structured output** (**Add field** for each):
  - `severity` (string): Impact on stock · **Allowed values** `severe`, `manageable`
  - `detail` (string): SKU, delay and days of cover
- **Next step (on exit) → Go to**: `mitigationRouter`

#### Router `mitigationRouter`

- **Description** Severe delays are rerouted, shortages get a new supplier, the rest a plan.
- **Routes** (**+**): **Label** Severe delay · **When** `@subagent.assessImpact.output.severity == "severe" and @generator.extractDisruption.output.kind == "delay"` · **Go to** `progressReroute`
- **Routes** (**+**): **Label** Shortage · **When** `@generator.extractDisruption.output.kind == "shortage"` · **Go to** `progressResource`
- **Otherwise → Go to**: `progressMitigationPlan`

#### Executor `reroute`

- **Description** Switches the shipment to a faster mode (no LLM).
- **Steps (do)**: **Run action**
  - **Action** `reroute_shipment`
    - **Bind argument** `shipment_id` = `@generator.extractDisruption.output.shipment_id`
- **Next step (on exit) → Go to**: `progressInformCustomers`

#### Subagent `informCustomers`

- **Label** Inform Customers · **Description** Tells the affected customers the new date.
- **Reasoning instructions**:

  > Shipment {!@generator.extractDisruption.output.shipment_id} was rerouted. Impact: {!@subagent.assessImpact.output.detail}. Inform the affected customers.

- **Actions** (**+ Add action…**): `customer_comms_agent`
- **Next step (on exit) → Go to**: `rerouted`

#### Orchestrator `resource`

- **Label** Re-source · **Description** Finds an alternative supplier, checks its risk and places the order.
- **System instructions**:

  > Find approved alternative suppliers for the SKU, ask the supplier risk agent which one to use,
  > then ask the buyer agent to place the order. Summarise supplier, quantity and delivery date.

- **Reasoning instructions**:

  > Shortage on shipment {!@generator.extractDisruption.output.shipment_id}: {!@subagent.assessImpact.output.detail}

- **Actions** (**+ Add action…**): `find_alternative_supplier`, `supplier_risk_agent`, `buyer_agent`
- **Limits → Max loops**: `6`
- **Next step (on exit) → Go to**: `resourced`

#### Subagent `mitigationPlan`

- **Label** Mitigation Plan · **Description** Stock covers the delay: proposes a plan with the logistics agent.
- **Reasoning instructions**:

  > Stock covers the disruption of {!@generator.extractDisruption.output.shipment_id}: {!@subagent.assessImpact.output.detail}. Ask logistics for options and propose a plan.

- **Actions** (**+ Add action…**): `logistics_agent`
- **Next step (on exit) → Go to**: `planned`

#### Reply `rerouted`

- **Use expression**, then **Message (expression)**: `"Shipment " + @generator.extractDisruption.output.shipment_id + " rerouted. " + @subagent.informCustomers.output`
- **Task state**: `TASK_STATE_COMPLETED`

#### Reply `resourced`

- **Use expression**, then **Message (expression)**: `"Shortage handled: " + @orchestrator.resource.output`
- **Task state**: `TASK_STATE_COMPLETED`

#### Reply `planned`

- **Use expression**, then **Message (expression)**: `"No stock-out expected. " + @subagent.mitigationPlan.output`
- **Task state**: `TASK_STATE_COMPLETED`

#### Reply `progressExtractDisruption`

- **Message text**: Extracting the shipment id and the kind of disruption...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `extractDisruption`

#### Reply `progressAssessImpact`

- **Message text**: Reading the shipment and the stock cover of its SKU, rating the impact...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `assessImpact`

#### Reply `progressReroute`

- **Message text**: Switching the shipment to a faster mode...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `reroute`

#### Reply `progressInformCustomers`

- **Message text**: Telling the affected customers the new date...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `informCustomers`

#### Reply `progressResource`

- **Message text**: Finding an alternative supplier, checking its risk and placing the order...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `resource`

#### Reply `progressMitigationPlan`

- **Message text**: Stock covers the delay: planning with the logistics agent...
- **Task state**: `TASK_STATE_WORKING` (a progress update: the chat shows it while the broker works, then the flow goes on)
- **Next step (on exit) → Go to**: `mitigationPlan`

![The finished broker flow](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-flow.png)

When you are done, the flow matches the template's flow ([Path 2, Step 4](#step-4-follow-the-broker-flow-agentscript)). The built-in `done` reply isn't used by this use case. The Problems bar shows **echo done is not reachable from the trigger** as a warning, and you can leave it.

### Step 3.9. Add the policies

Select the broker or connection, scroll to **Policies** and click **Add policy**. Pick the policy (search by name), choose the **Direction** and set its **Configuration** fields. **Header Injection** has its own header list. Octoloom also adds each policy as an `exchange.json` dependency.

- Broker `disruption_broker`: **Rate Limiting** (inbound)
  - **rateLimits** (one entry each, **+**): maximumRequests `30`, timePeriodInMilliseconds `60000`
  - **exposeHeaders**: on
- Connection `supplier_risk_agent_connection`: **Message Logging (outbound)** (outbound)
  - **loggingConfiguration** (one entry each, **+**): itemName `Upstream calls`, itemData `{'message': '#[attributes.method ++ " " ++ attributes.requestPath]', 'level': 'INFO', 'firstSection': True, 'secondSection': False}`
- Connection `logistics_agent_connection`: **Message Logging (outbound)** (outbound)
  - **loggingConfiguration** (one entry each, **+**): itemName `Upstream calls`, itemData `{'message': '#[attributes.method ++ " " ++ attributes.requestPath]', 'level': 'INFO', 'firstSection': True, 'secondSection': False}`
- Connection `buyer_agent_connection`: **Message Logging (outbound)** (outbound)
  - **loggingConfiguration** (one entry each, **+**): itemName `Upstream calls`, itemData `{'message': '#[attributes.method ++ " " ++ attributes.requestPath]', 'level': 'INFO', 'firstSection': True, 'secondSection': False}`
- Connection `customer_comms_agent_connection`: **Message Logging (outbound)** (outbound)
  - **loggingConfiguration** (one entry each, **+**): itemName `Upstream calls`, itemData `{'message': '#[attributes.method ++ " " ++ attributes.requestPath]', 'level': 'INFO', 'firstSection': True, 'secondSection': False}`
- Connection `shipments_mcp_connection`: **Message Logging (outbound)** (outbound)
  - **loggingConfiguration** (one entry each, **+**): itemName `Upstream calls`, itemData `{'message': '#[attributes.method ++ " " ++ attributes.requestPath]', 'level': 'INFO', 'firstSection': True, 'secondSection': False}`
- Connection `inventory_mcp_connection`: **Message Logging (outbound)** (outbound)
  - **loggingConfiguration** (one entry each, **+**): itemName `Upstream calls`, itemData `{'message': '#[attributes.method ++ " " ++ attributes.requestPath]', 'level': 'INFO', 'firstSection': True, 'secondSection': False}`
- Connection `supplier_mcp_connection`: **Message Logging (outbound)** (outbound)
  - **loggingConfiguration** (one entry each, **+**): itemName `Upstream calls`, itemData `{'message': '#[attributes.method ++ " " ++ attributes.requestPath]', 'level': 'INFO', 'firstSection': True, 'secondSection': False}`

![Policies on the broker](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-supply-chain-secured/img/scratch-policy.png)

The template declares a policy once under `context.policies` and points to it from each connection. **Add policy** writes each policy on its connection instead. Both give the same result at runtime.

### Step 3.10. Validate, deploy and chat

Run **Validate** from the canvas CLI menu and fix anything in the Problems bar. Then follow Path 2 from [Validate and build](#step-5-validate-and-build) onwards: deploy (enter the secrets), wait for the green light, open the chat and send the same prompts. Your network answers like the template, because it is the same network, built by hand.

## What you learned

- How a deterministic network is built: an AgentScript flow decides every step; the LLM extracts and writes text.
- How the canvas, the inspector and the code view edit the same YAML.
- How to build the same network from a blank project with forms and menus only (Path 3).
- How policies are attached and checked with Governance.
- How authenticated connections use variables and secret variables.
- How to validate, build, deploy, chat and trace with Octoloom.

## Next

- Previous: [KYC / AML Onboarding: secured](v2-kyc-onboarding-secured.md)
- Next: [IDMC Data Trust (needs Informatica IDMC)](v2-idmc-data-trust.md)
- Same use case, plain variant: [Supply Chain Disruption](v2-supply-chain.md)
- Same use case, governed variant: [Supply Chain Disruption: governed](v2-supply-chain-governed.md)
- [All tutorials](index.md)

---
Generated from the `v2-supply-chain-secured` template (Octoloom `media/templates/v2-supply-chain-secured`). Screenshots use fake data.
