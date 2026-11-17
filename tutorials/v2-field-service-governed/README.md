# Tutorial: Field Service Dispatch: governed

[All tutorials](../README.md) · [Getting started](../getting-started.md) · Deterministic network (Agent Network 2.0, AgentScript) · Technical · governed

> Diagnose an equipment fault, check parts and weather, and dispatch or resolve remotely. Adds built-in policies: a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 3 | 4 | 1.0, 0.3.0 | 5 | `v2-field-service-governed` |

There are two ways to use this template:

1. **[Just use it](#path-1-just-use-it)**: create the project, deploy it and chat with it in about 10 minutes.
2. **[Learn step by step](#path-2-learn-step-by-step)**: the same steps, with what each part of the network does and how Octoloom shows it.

## Before you start

- VS Code with **Octoloom for Agent Fabric** installed (Marketplace), version 0.9.25 or later.
- An Anypoint organization with Agent Fabric, a connected app (client ID and secret), an environment and a Flex gateway.
- An OpenAI API key (or an OpenAI-compatible LLM gateway).
- Nothing else: all agents and MCP servers are public A²D mocks, so the network runs without any other system.

## Path 1: Just use it

1. **Home → Start → New Deterministic Network.** In the dialog pick **Technical**, then the card **Field Service Dispatch** (the one with the policies chip). Choose a folder and click **Create**.
2. **Deploy.** In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: OpenAI API key (secret, injected at deploy time)
3. **Chat.** When the status light is green, click **Open chat** and paste:
   - `Heat pump HP-301 shows error E42`
   - `Solar inverter INV-77 is offline`
   - `My email is jane.doe@example.com and my phone is +41 79 123 45 67. Heat pump HP-301 shows error E42`
   - `Send the first prompt more than 30 times within a minute`

Done. The rest of this page explains what you just ran.

## Path 2: Learn step by step

### Step 1. Connect Octoloom

Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. A²D isn't needed: the mock URLs are already the defaults in `exchange.json`. The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.

### Step 2. Create the project from the template

On **Home**, click **New Deterministic Network**. In **2 Start from**, choose **Technical** and click **Field Service Dispatch**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `field-service-governed` or type your own, pick the folder and click **Create**.

![New Project dialog with Field Service Dispatch: governed selected](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-field-service-governed/img/new-project.png)

Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md` and the broker flow in `brokers/`, and opens the canvas. Every id gets the template prefix `octo_fs2g_`, so several templates can be deployed into one org side by side.

### Step 3. Read the network on the canvas

![Field Service Dispatch: governed on the Deterministic network canvas](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-field-service-governed/img/canvas.png)

Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).

- **Broker Field Service Broker** (`octo_fs2g_field_service_broker`): its AgentScript flow decides every step.
- **Agent Dispatch Agent**: Books technicians for on-site visits.
- **Agent Parts Logistics Agent**: Reserves and ships spare parts.
- **Agent Customer Communications Agent**: Keeps the customer informed.
- **MCP server Asset Registry MCP**: Installed equipment. Tools: `get_asset`.
- **MCP server Diagnostics MCP**: Remote diagnostics. Tools: `run_diagnostics`.
- **MCP server Parts Inventory MCP**: Spare parts stock. Tools: `check_stock`.
- **MCP server Weather MCP**: Weather for safe outdoor work. Tools: `get_forecast`.

Try this on the canvas: use the zoom bar and the minimap, drag a card, or **Auto layout**. The layout is saved per file. **Minimize all** turns the cards into icon tiles. Click a connection line to see which broker uses which agent or tool.

### Step 4. Follow the broker flow (AgentScript)

Double-click the broker card (or open `brokers/field-service-broker.agent`). The flow editor shows the AgentScript program that decides every step. The LLM only extracts fields and writes text, so the same input always takes the same branch.

![Field Service Dispatch: governed broker flow](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-field-service-governed/img/flow.png)

| Step | Kind | What it does |
|---|---|---|
| `fieldServiceBrokerTrigger` | Trigger | Starts the flow when an A2A message arrives at the broker. |
| `parseRequest` | Generator | Extracts the asset id and the symptom. |
| `diagnose` | Subagent | Looks up the asset and runs remote diagnostics. |
| `fixRouter` | Router | Remote fixes only need a customer update; the rest are dispatched. |
| `informCustomer` | Subagent | Tells the customer the fault was fixed remotely. |
| `resolvedRemotely` | Echo | Ends the flow with the `resolvedRemotely` reply. |
| `dispatchVisit` | Orchestrator | Checks parts and weather, reserves the part and books a technician. |
| `dispatched` | Echo | Ends the flow with the `dispatched` reply. |

Click a step to edit it in the inspector. **+ Step** adds a node, and **+ Step → Patterns** inserts whole shapes such as retry, human in the loop or a guardrail check. **Code** shows the `.agent` text with completion.

### Step 5. See the policies

This variant adds Agent Fabric policies. Open a broker or connection and look at its **Policies** section. Each policy folds open to show its configuration:
- `a2a-v1-pii-detector`
- `header-injection`
- `mcp-pii-detector`
- `mcp-schema-validation`
- `rate-limiting`

Run **Governance** (shield icon in the canvas toolbar) to check the project against the Agent Fabric rulesets. It runs locally, and findings show on the cards with **Fix** where one exists.

### Step 6. Validate and build

In the canvas toolbar, open the CLI menu: **Validate** does a dry run of build, publish and deploy and lists problems in the Problems panel (click one to jump to the card). **Build** repairs and packages the project locally with anypoint-cli-v4.

The variables of this template (in `exchange.json`, open it for the no-code form):

| Variable | What | Default |
|---|---|---|
| `dispatchAgent.url` | Dispatch Agent (A2D mock, A2A 1.0) URL | `https://www.a2d-ai.com/api/platform/69ebd12e-296f-4eed-949f-26296e3c7fe9/a2a` |
| `partsAgent.url` | Parts Logistics Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/1f49d5bd-b631-498b-b2a6-84de58a41521/a2a` |
| `customerCommsAgent.url` | Customer Communications Agent (A2D mock, A2A 1.0) URL | `https://www.a2d-ai.com/api/platform/f3d6ebd7-0b13-43c2-b2ef-f55ac045c18a/a2a` |
| `assetRegistryMcp.url` | Asset Registry MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/e63366bc-fc42-4a5f-82c6-960245f373d8/` |
| `diagnosticsMcp.url` | Diagnostics MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/9c1cb10f-5950-428c-88aa-d2b0f52f508e/` |
| `inventoryMcp.url` | Parts Inventory MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/646e87d9-595d-4194-8ffd-4eeb958fc2f5/` |
| `weatherMcp.url` | Weather MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/1839bfc8-fb85-4256-9195-26c193243b7d/` |

### Step 7. Deploy

Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:

- `openai.apiKey`: OpenAI API key (secret, injected at deploy time)

The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.

### Step 8. Chat with the broker

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. Paste the prompts one at a time:

![Field Service Dispatch: governed in the broker chat](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-field-service-governed/img/chat.png)

*The reply in the screenshot is an illustration: it shows what the broker answers. The real wording changes from run to run.*

| Prompt | You should see |
|---|---|
| `Heat pump HP-301 shows error E42` | Asset Registry `get_asset`, Diagnostics `run_diagnostics` needs a visit. Parts Inventory `check_stock`: CMP-42 from Bern. Weather `get_forecast`: Vevey OK. Parts Logistics reserves it, Dispatch books technician T-14 (Marco) tomorrow 08:00-10:00, Customer Communications confirms. |
| `Solar inverter INV-77 is offline` | Diagnostics `run_diagnostics`: lost connectivity, fixed with a remote reboot. Customer Communications informs the customer; no visit. |
| `My email is jane.doe@example.com and my phone is +41 79 123 45 67. Heat pump HP-301 shows error E42` | Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring. |
| `Send the first prompt more than 30 times within a minute` | The broker answers HTTP 429 (Too Many Requests) once the rate limit of 30 requests per minute is reached. |

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.

### Step 9. Trace a reply

Under each reply, the **Tracer** icon opens the task in the **Agent Network Tracer**: a waterfall of every call the broker made (gateway, broker, LLM, A2A agents, MCP tools) on one time axis, coloured like the cards. Errors are red. Click a span to see its request and response. The **Network** view shows the same reply as a sequence of calls.

### Step 10. Share it (optional)

The **Share** icon in the chat header opens the Share dialog. **A²D sessions** invites people by email to chat with this deployed broker and brings their passed / failed marks and comments back. **Local portal** generates a small web chat you can run or host anywhere.

## What you learned

- How a deterministic network is built: an AgentScript flow decides every step; the LLM extracts and writes text.
- How the canvas, the inspector and the code view edit the same YAML.
- How policies are attached and checked with Governance.
- How to validate, build, deploy, chat and trace with Octoloom.

## Next

- Previous: [Supply Chain Disruption](../v2-supply-chain/README.md)
- Next: [IT Incident Response: governed](../v2-incident-response-governed/README.md)
- Same use case, plain variant: [Field Service Dispatch](../v2-field-service/README.md)
- [All tutorials](../README.md)

---
Generated from the `v2-field-service-governed` template (Octoloom `media/templates/v2-field-service-governed`). Screenshots use fake data.
