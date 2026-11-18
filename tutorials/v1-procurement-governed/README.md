# Tutorial: Procurement Assistant: governed

[All tutorials](../README.md) · [Getting started](../getting-started.md) · Probabilistic network (Agent Network 1.0, LLM broker) · Technical · governed

> A tool-heavy broker: two agents and five procurement tool servers turn requests into purchase orders. Adds built-in policies: rate-limiting, mcp-pii-detector, mcp-schema-validation, header-injection, a-two-a-pii-detector, a-two-a-prompt-decorator.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 2 | 5 | 0.3.0 | 6 | `v1-procurement-governed` |

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

1. **Home → Start → New Probabilistic Network.** In the dialog pick **Technical**, then the card **Procurement Assistant** (the one with the policies chip). Choose a folder and click **Create**.
2. **Deploy.** In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: OpenAI API key (secret, injected at deploy time)
3. **Chat.** When the status light is green, click **Open chat** and paste:
   - `Order 5 monitors for cost centre CC-410`
   - `Is supplier SUP-88 approved? And SUP-91?`
   - `Order 5 monitors for cost centre CC-999`
   - `Find an alternative to MON-27A`
   - `My email is jane.doe@example.com and my phone is +41 79 123 45 67. Order 5 monitors for cost centre CC-410`
   - `Send the first prompt more than 30 times within a minute`

Done. The rest of this page explains what you just ran.

## Path 2: Learn step by step

### Step 1. Connect Octoloom

Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. A²D isn't needed: the mock URLs are already the defaults in `exchange.json`. The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.

### Step 2. Create the project from the template

On **Home**, click **New Probabilistic Network**. In **2 Start from**, choose **Technical** and click **Procurement Assistant**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `procurement-governed` or type your own, pick the folder and click **Create**.

![New Project dialog with Procurement Assistant: governed selected](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/new-project.png)

Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md`, and opens the canvas. Every id gets the template prefix `octo_p1g_`, so several templates can be deployed into one org side by side.

### Step 3. Read the network on the canvas

![Procurement Assistant: governed on the Probabilistic network canvas](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/canvas.png)

Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).

- **Broker octo_p1g_procurement-broker** (`octo_p1g_procurement-broker`): the LLM decides which agent or tool to call from its instructions.
  - Instructions:
    - You turn purchase requests into compliant purchase orders.
    - Find the item in the catalog, check the cost-centre budget and look up the supplier.
    - Ask the Supplier Risk agent to assess any supplier that is not yet approved.
    - Use an existing framework contract when one exists; create the purchase order only when the budget is sufficient.
    - Ask the Sourcing agent for alternatives when an item is unavailable or over budget.
- **Agent Supplier Risk Agent**: Assesses supplier financial, ESG and sanctions risk.
- **Agent Sourcing Agent**: Finds alternative items and suppliers.
- **MCP server Catalog MCP**: Product catalog. Tools: `search_catalog`.
- **MCP server Budget MCP**: Cost-centre budgets. Tools: `check_budget`.
- **MCP server Supplier Registry MCP**: Approved suppliers. Tools: `get_supplier`.
- **MCP server Contracts MCP**: Framework contracts. Tools: `find_contract`.
- **MCP server Purchase Orders MCP**: Purchase orders. Tools: `create_purchase_order`.

Try this on the canvas: use the zoom bar and the minimap, drag a card, or **Auto layout**. The layout is saved per file. **Minimize all** turns the cards into icon tiles. Click a connection line to see which broker uses which agent or tool.

### Step 4. See the policies

This variant adds Agent Fabric policies. Open a broker or connection and look at its **Policies** section. Each policy folds open to show its configuration:
- `rate-limiting`
- `mcp-pii-detector`
- `mcp-schema-validation`
- `header-injection`
- `a-two-a-pii-detector`
- `a-two-a-prompt-decorator`

Run **Governance** (shield icon in the canvas toolbar) to check the project against the Agent Fabric rulesets. It runs locally, and findings show on the cards with **Fix** where one exists.

### Step 5. Validate and build

In the canvas toolbar, open the CLI menu: **Validate** does a dry run of build, publish and deploy and lists problems in the Problems panel (click one to jump to the card). **Build** repairs and packages the project locally with anypoint-cli-v4.

The variables of this template (in `exchange.json`, open it for the no-code form):

| Variable | What | Default |
|---|---|---|
| `ingressgw.url` | Ingress gateway base URL (the broker is served under it) | (fill in) |
| `catalogMcp.url` | Catalog MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/fc34bc2e-353d-47e5-bd83-92e6bf54fc62/` |
| `budgetMcp.url` | Budget MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/f4b4d8b6-3665-461b-bdc7-ddad0844cd4a/` |
| `supplierRegistryMcp.url` | Supplier Registry MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/4ce2b160-071c-4dc2-92c6-8b25b6d6bbd4/` |
| `contractsMcp.url` | Contracts MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/622d4561-4016-44f6-b158-2f642bbb3fe8/` |
| `purchaseOrdersMcp.url` | Purchase Orders MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/701ff77b-9e79-4dda-84bb-867e3aa7ad1b/` |
| `supplierRiskAgent.url` | Supplier Risk Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/61c4b202-4364-402c-bc08-6a6c0c5c719c/a2a` |
| `sourcingAgent.url` | Sourcing Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/6c82f3d9-b7fe-460e-82b8-768e047ba83d/a2a` |

### Step 6. Deploy

Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:

- `openai.apiKey`: OpenAI API key (secret, injected at deploy time)

For a probabilistic network, also fill `ingressgw.url` in `exchange.json` (your ingress gateway base URL) before you deploy.

The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.

### Step 7. Chat with the broker

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. Paste the prompts one at a time:

![Procurement Assistant: governed in the broker chat](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/chat.png)

*The reply in the screenshot is an illustration: it shows what the broker answers. The real wording changes from run to run.*

| Prompt | You should see |
|---|---|
| `Order 5 monitors for cost centre CC-410` | Catalog `search_catalog`: MON-27A, 349 CHF from SUP-88. Budget `check_budget`: CC-410 has 5,200 left. Supplier Risk: SUP-88 approved (risk 23). Contracts `find_contract`: FC-2026-04 (12% off). Purchase Orders `create_purchase_order`: PO-450021, 1,535.60. |
| `Is supplier SUP-88 approved? And SUP-91?` | Supplier Registry `get_supplier` and Supplier Risk: SUP-88 approved (risk 23), SUP-91 not approved (risk 71). |
| `Order 5 monitors for cost centre CC-999` | Budget `check_budget`: CC-999 has only 120 left, so no purchase order is created. |
| `Find an alternative to MON-27A` | Sourcing Agent: 27" QHD monitor MON-27B from SUP-88 at 219 CHF (contract FC-2026-04). |
| `My email is jane.doe@example.com and my phone is +41 79 123 45 67. Order 5 monitors for cost centre CC-410` | Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring. |
| `Send the first prompt more than 30 times within a minute` | The broker answers HTTP 429 (Too Many Requests) once the rate limit of 60 requests per minute is reached. |

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.

### Step 8. Trace a reply

Under each reply, the **Tracer** icon opens the task in the **Agent Network Tracer**: a waterfall of every call the broker made (gateway, broker, LLM, A2A agents, MCP tools) on one time axis, coloured like the cards. Errors are red. Click a span to see its request and response. The **Network** view shows the same reply as a sequence of calls.

### Step 9. Share it (optional)

The **Share** icon in the chat header opens the Share dialog. **A²D sessions** invites people by email to chat with this deployed broker and brings their passed / failed marks and comments back. **Local portal** generates a small web chat you can run or host anywhere.

## Path 3: Build it from scratch

Here you build the same network yourself, starting from a blank project. Every step uses a form, a menu or a button. You never import the template, and you never type YAML. The names below are the template's names without the `octo_p1g_` prefix. You can use your own names, but keep them consistent.

> The text fields take plain values. Where a value looks like `${group.name}`, type it as shown: it is a **variable** that `exchange.json` declares and that deploy fills in.

### Step 3.1. Create a blank project with a starter broker

Connect Octoloom first, as in [Path 2, Step 1](#step-1-connect-octoloom). Then, on **Home**, click **New Probabilistic Network**. In **2 Start from**, choose **Blank** and turn on **Add a starter broker**.

- **Broker name**: `procurement-broker`
- **Name**: `procurement-governed-scratch` (the Exchange asset id; a different name from the template, so both can live in one org)
- **Parent folder**: pick a folder, then click **Create blank project**.

![Blank project with a starter broker](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/scratch-new.png)

The starter broker is an LLM broker with an OpenAI LLM (`openai` provider, `openai-connection`) and default instructions. The LLM is already done.

### Step 3.2. Add the agents

On the canvas, click **+** (Add to the network) → **Agent** → **Empty**. The new agent opens in the inspector on the right. Fill it in, then repeat for each agent:

![The Add to the network menu with the Agent submenu](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/scratch-add.png)

- **Supplier Risk Agent**
  - **Identity → Key**: `supplier-risk-agent`
  - **Label**: Supplier Risk Agent · **Description**: Assesses supplier financial, ESG and sanctions risk.
  - **Metadata → Platform**: `Databricks` (or click its icon under **Agent framework**)
  - **Agent card**: **Name** Supplier Risk Agent, **Description** as above, **URL** `${supplierRiskAgent.url}`, **Protocol version** `0.3.0`
- **Sourcing Agent**
  - **Identity → Key**: `sourcing-agent`
  - **Label**: Sourcing Agent · **Description**: Finds alternative items and suppliers.
  - **Metadata → Platform**: `LangChain` (or click its icon under **Agent framework**)
  - **Agent card**: **Name** Sourcing Agent, **Description** as above, **URL** `${sourcingAgent.url}`, **Protocol version** `0.3.0`

![An agent in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/scratch-agent.png)

The card skills are optional. Once the agent has a connection (two steps on), the inspector offers **Read skills from the live agent**, which fills them from the running agent.

### Step 3.3. Add the MCP servers

Click **+** → **MCP server** → **Empty**, then fill in:

- **Catalog MCP**: **Key** `catalog-mcp`, **Label** Catalog MCP, **Description** Product catalog. The transport is already Streamable HTTP on `/mcp`.
- **Budget MCP**: **Key** `budget-mcp`, **Label** Budget MCP, **Description** Cost-centre budgets. The transport is already Streamable HTTP on `/mcp`.
- **Supplier Registry MCP**: **Key** `supplier-registry-mcp`, **Label** Supplier Registry MCP, **Description** Approved suppliers. The transport is already Streamable HTTP on `/mcp`.
- **Contracts MCP**: **Key** `contracts-mcp`, **Label** Contracts MCP, **Description** Framework contracts. The transport is already Streamable HTTP on `/mcp`.
- **Purchase Orders MCP**: **Key** `purchase-orders-mcp`, **Label** Purchase Orders MCP, **Description** Purchase orders. The transport is already Streamable HTTP on `/mcp`.

### Step 3.4. Add the connections

A connection is the URL (and authentication) Agent Fabric uses to reach an agent or an MCP server. Click **+** → **Connection** → **Empty** once per agent and MCP server, and fill in:

| Key | Kind | Target → Name | URL |
|---|---|---|---|
| `catalog-mcp-connection` | `mcp` | `catalog-mcp` | `${catalogMcp.url}` |
| `budget-mcp-connection` | `mcp` | `budget-mcp` | `${budgetMcp.url}` |
| `supplier-registry-mcp-connection` | `mcp` | `supplier-registry-mcp` | `${supplierRegistryMcp.url}` |
| `contracts-mcp-connection` | `mcp` | `contracts-mcp` | `${contractsMcp.url}` |
| `purchase-orders-mcp-connection` | `mcp` | `purchase-orders-mcp` | `${purchaseOrdersMcp.url}` |
| `supplier-risk-agent-connection` | `agent` | `supplier-risk-agent` | `${supplierRiskAgent.url}` |
| `sourcing-agent-connection` | `agent` | `sourcing-agent` | `${sourcingAgent.url}` |

![A connection in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/scratch-conn.png)

### Step 3.5. Declare the variables

The Problems bar now shows **Variable ${…} is not declared in exchange.json** for each new variable. Click **Add to exchange.json** on each one.

Then open `exchange.json` (it opens as a form) and, under **Variables**, set the defaults:

| Variable | Default |
|---|---|
| `ingressgw.url` | (your ingress gateway URL) |
| `catalogMcp.url` | `https://www.a2d-ai.com/api/platform/fc34bc2e-353d-47e5-bd83-92e6bf54fc62/` |
| `budgetMcp.url` | `https://www.a2d-ai.com/api/platform/f4b4d8b6-3665-461b-bdc7-ddad0844cd4a/` |
| `supplierRegistryMcp.url` | `https://www.a2d-ai.com/api/platform/4ce2b160-071c-4dc2-92c6-8b25b6d6bbd4/` |
| `contractsMcp.url` | `https://www.a2d-ai.com/api/platform/622d4561-4016-44f6-b158-2f642bbb3fe8/` |
| `purchaseOrdersMcp.url` | `https://www.a2d-ai.com/api/platform/701ff77b-9e79-4dda-84bb-867e3aa7ad1b/` |
| `supplierRiskAgent.url` | `https://www.a2d-ai.com/api/platform/61c4b202-4364-402c-bc08-6a6c0c5c719c/a2a` |
| `sourcingAgent.url` | `https://www.a2d-ai.com/api/platform/6c82f3d9-b7fe-460e-82b8-768e047ba83d/a2a` |

Leave the secret variables (`openai.apiKey`) empty: deploy asks for them and never stores them.

![The exchange.json form with the variables](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/scratch-vars.png)

### Step 3.6. Declare the MCP tools

On each MCP server card, click the **Tools** row (or its pencil). Octoloom reads the tool list from the running server: tick the tools below. You can also type a name in **Add a tool by name…**.

- **Catalog MCP**: `search_catalog`
- **Budget MCP**: `check_budget`
- **Supplier Registry MCP**: `get_supplier`
- **Contracts MCP**: `find_contract`
- **Purchase Orders MCP**: `create_purchase_order`

![The Tools row of an MCP server card](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/scratch-tools.png)

### Step 3.7. Give the broker its agents and tools

Select the broker `procurement-broker`. In the inspector:

1. Click **Agents (0)**. In **Add existing agent…**, pick each agent and click **Add**: `supplier-risk-agent`, `sourcing-agent`.
2. Click **MCP servers**. Add each server with **Add existing MCP server…**, then tick its **Allowed tools**:
   - `catalog-mcp`: `search_catalog`
   - `budget-mcp`: `check_budget`
   - `supplier-registry-mcp`: `get_supplier`
   - `contracts-mcp`: `find_contract`
   - `purchase-orders-mcp`: `create_purchase_order`

![The MCP servers of the broker with their allowed tools](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/scratch-links.png)

### Step 3.8. Write the broker instructions

Back in the broker inspector, open **Instructions and limits**. Replace the default instruction with these entries, one per line:

- You turn purchase requests into compliant purchase orders.
- Find the item in the catalog, check the cost-centre budget and look up the supplier.
- Ask the Supplier Risk agent to assess any supplier that is not yet approved.
- Use an existing framework contract when one exists; create the purchase order only when the budget is sufficient.
- Ask the Sourcing agent for alternatives when an item is unavailable or over budget.

Set **Max number of loops** `25`, **Max consecutive errors** `3` and **Task timeout (s)** `90`.
Under **Model parameters → OpenAI**, set **Reasoning effort** to `MINIMAL`. The broker then answers within the gateway timeout.

Optionally, fill the broker's **Agent card (A2A 0.3.0)** description: *A tool-heavy broker: two agents and five procurement tool servers turn requests into purchase orders.*

![The broker instructions and limits](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/scratch-broker.png)

### Step 3.9. Add the policies

Select the broker or connection, scroll to **Policies** and click **Add policy**. Pick the policy (search by name) and set its **Configuration** fields. **Header Injection** has its own header list. Octoloom also adds each policy as an `exchange.json` dependency.

- Broker `procurement-broker`: **Rate Limiting**
  - **rateLimits** (one entry each, **+**): maximumRequests `60`, timePeriodInMilliseconds `60000`
  - **exposeHeaders**: on
- Connection `catalog-mcp-connection`: **MCP PII Detector**
  - **entities**: `Email`, `US SSN`, `Credit Card`, `Phone Number`
  - **action**: `Log and mask`
- Connection `budget-mcp-connection`: **MCP Schema Validation**
  - **validateToolSchema**: on
- Connection `budget-mcp-connection`: **Header Injection**
  - **inboundHeaders** (one entry each, **+**): `x-octoloom-source` = `procurement-governed-v1`
- Connection `supplier-registry-mcp-connection`: **MCP PII Detector**
  - **entities**: `Email`, `US SSN`, `Credit Card`, `Phone Number`
  - **action**: `Log and mask`
- Connection `contracts-mcp-connection`: **MCP Schema Validation**
  - **validateToolSchema**: on
- Connection `contracts-mcp-connection`: **Header Injection**
  - **inboundHeaders** (one entry each, **+**): `x-octoloom-source` = `procurement-governed-v1`
- Connection `purchase-orders-mcp-connection`: **MCP PII Detector**
  - **entities**: `Email`, `US SSN`, `Credit Card`, `Phone Number`
  - **action**: `Log and mask`
- Connection `supplier-risk-agent-connection`: **A2A PII Detector**
  - **entities**: `Email`, `US SSN`, `Credit Card`
  - **action**: `Log`
- Connection `sourcing-agent-connection`: **Header Injection**
  - **inboundHeaders** (one entry each, **+**): `x-correlation-source` = `procurement-broker`
- Connection `sourcing-agent-connection`: **A2A Prompt Decorator**
  - **textDecorators** (one entry each, **+**): text `#['Answer concisely and never include personal data.']`

![Policies on the broker](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-procurement-governed/img/scratch-policy.png)

### Step 3.10. Validate, deploy and chat

Run **Validate** from the canvas CLI menu and fix anything in the Problems bar. Then follow Path 2 from [Validate and build](#step-4-validate-and-build) onwards: deploy (enter the secrets), wait for the green light, open the chat and send the same prompts. Your network answers like the template, because it is the same network, built by hand.

## What you learned

- How a probabilistic network is built: an LLM broker with instructions picks agents and MCP tools.
- How the canvas, the inspector and the code view edit the same YAML.
- How to build the same network from a blank project with forms and menus only (Path 3).
- How policies are attached and checked with Governance.
- How to validate, build, deploy, chat and trace with Octoloom.

## Next

- Previous: [Patient Intake (demo data): governed](../v1-patient-intake-governed/README.md)
- Next: [Travel & Expense: governed](../v1-travel-expense-governed/README.md)
- Same use case, plain variant: [Procurement Assistant](../v1-procurement/README.md)
- [All tutorials](../README.md)

---
Generated from the `v1-procurement-governed` template (Octoloom `media/templates/v1-procurement-governed`). Screenshots use fake data.
