# Tutorial: Supply Chain Disruption: secured

[All tutorials](../README.md) · [Getting started](../getting-started.md) · Deterministic network (Agent Network 2.0, AgentScript) · Technical · secured

> A late or short shipment is assessed against stock; severe delays are rerouted and customers told, other cases get a mitigation plan. Secured: authenticated connections (Basic, Client ID enforcement) with secret variables, the LLM behind a gateway URL, outbound message logging.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 4 | 3 | 1.0, 0.3.0 | 2 | `v2-supply-chain-secured` |

There are two ways to use this template:

1. **[Just use it](#path-1-just-use-it)**: create the project, deploy it and chat with it in about 10 minutes.
2. **[Learn step by step](#path-2-learn-step-by-step)**: the same steps, with what each part of the network does and how Octoloom shows it.

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

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. Paste the prompts one at a time:

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

## What you learned

- How a deterministic network is built: an AgentScript flow decides every step; the LLM extracts and writes text.
- How the canvas, the inspector and the code view edit the same YAML.
- How policies are attached and checked with Governance.
- How authenticated connections use variables and secret variables.
- How to validate, build, deploy, chat and trace with Octoloom.

## Next

- Previous: [KYC / AML Onboarding: secured](../v2-kyc-onboarding-secured/README.md)
- Next: [IDMC Data Trust (needs Informatica IDMC)](../v2-idmc-data-trust/README.md)
- Same use case, plain variant: [Supply Chain Disruption](../v2-supply-chain/README.md)
- Same use case, governed variant: [Supply Chain Disruption: governed](../v2-supply-chain-governed/README.md)
- [All tutorials](../README.md)

---
Generated from the `v2-supply-chain-secured` template (Octoloom `media/templates/v2-supply-chain-secured`). Screenshots use fake data.
