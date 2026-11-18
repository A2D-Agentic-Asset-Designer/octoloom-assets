# Tutorial: Travel & Expense: governed

[All tutorials](../README.md) · [Getting started](../getting-started.md) · Probabilistic network (Agent Network 1.0, LLM broker) · Technical · governed

> Five specialist agents and four travel and finance tool servers plan trips and settle expenses. Adds built-in policies: rate-limiting, mcp-pii-detector, mcp-schema-validation, header-injection, a-two-a-pii-detector, a-two-a-prompt-decorator.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 5 | 4 | 0.3.0 | 6 | `v1-travel-expense-governed` |

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

1. **Home → Start → New Probabilistic Network.** In the dialog pick **Technical**, then the card **Travel & Expense** (the one with the policies chip). Choose a folder and click **Create**.
2. **Deploy.** In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: OpenAI API key (secret, injected at deploy time)
3. **Chat.** When the status light is green, click **Open chat** and paste:
   - `Book a trip from Zurich to London for 2026-12-02 to 2026-12-04`
   - `Can I fly business class to London?`
   - `Do I need a visa for India? And for the UK?`
   - `Submit my hotel bill of 420 GBP for reimbursement`
   - `My email is jane.doe@example.com and my phone is +41 79 123 45 67. Book a trip from Zurich to London for 2026-12-02 to 2026-12-04`
   - `Send the first prompt more than 30 times within a minute`

Done. The rest of this page explains what you just ran.

## Path 2: Learn step by step

### Step 1. Connect Octoloom

Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. A²D isn't needed: the mock URLs are already the defaults in `exchange.json`. The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.

### Step 2. Create the project from the template

On **Home**, click **New Probabilistic Network**. In **2 Start from**, choose **Technical** and click **Travel & Expense**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `travel-expense-governed` or type your own, pick the folder and click **Create**.

![New Project dialog with Travel & Expense: governed selected](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/new-project.png)

Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md`, and opens the canvas. Every id gets the template prefix `octo_te1g_`, so several templates can be deployed into one org side by side.

### Step 3. Read the network on the canvas

![Travel & Expense: governed on the Probabilistic network canvas](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/canvas.png)

Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).

- **Broker octo_te1g_travel-expense-broker** (`octo_te1g_travel-expense-broker`): the LLM decides which agent or tool to call from its instructions.
  - Instructions:
    - You plan business trips and settle travel expenses.
    - Check the travel policy with the Policy Advisor agent before booking anything.
    - Search flights and hotels with the tools, then book through the Travel Booking agent.
    - For trips abroad ask the Visa agent whether a visa is needed.
    - Expenses: convert amounts with convert_currency, audit them with the Expense Audit agent and pay out through the Reimbursement agent.
- **Agent Travel Booking Agent**: Books flights, hotels and rail.
- **Agent Policy Advisor Agent**: Explains the corporate travel policy.
- **Agent Visa Agent**: Visa and entry requirements.
- **Agent Expense Audit Agent**: Audits expenses against policy.
- **Agent Reimbursement Agent**: Pays out approved expenses.
- **MCP server Flights MCP**: Flight search. Tools: `search_flights`.
- **MCP server Hotels MCP**: Hotel search. Tools: `search_hotels`.
- **MCP server Expense MCP**: Expense reports. Tools: `create_expense_report`.
- **MCP server Currency MCP**: Currency conversion. Tools: `convert_currency`.

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
| `flightsMcp.url` | Flights MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/1f6d63f2-3c3d-4268-9471-40e6d18955d3/` |
| `hotelsMcp.url` | Hotels MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/6875794f-e1ea-479e-a2f8-4d9ed4b29dfc/` |
| `expenseMcp.url` | Expense MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/75a62546-5ff3-4c98-ac92-d1bf91a1265c/` |
| `currencyMcp.url` | Currency MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/54c12af9-4b43-4be6-a861-fe9ad82c0944/` |
| `travelBookingAgent.url` | Travel Booking Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/e106ec8c-02ee-4ce5-b015-2cd536b26b77/a2a` |
| `policyAdvisorAgent.url` | Policy Advisor Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/cdf8b42e-2666-42f6-a5ae-09b40aee71bc/a2a` |
| `visaAgent.url` | Visa Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/7256173e-0e33-484b-b11b-1f07610c1f75/a2a` |
| `expenseAuditAgent.url` | Expense Audit Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/bcc0eab9-61c0-48e5-9092-6d4ce1a6c0d9/a2a` |
| `reimbursementAgent.url` | Reimbursement Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/c0ffe718-d2aa-4298-b713-96c807aa2551/a2a` |

### Step 6. Deploy

Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:

- `openai.apiKey`: OpenAI API key (secret, injected at deploy time)

For a probabilistic network, also fill `ingressgw.url` in `exchange.json` (your ingress gateway base URL) before you deploy.

The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.

### Step 7. Chat with the broker

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. Paste the prompts one at a time:

![Travel & Expense: governed in the broker chat](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/chat.png)

*The reply in the screenshot is an illustration: it shows what the broker answers. The real wording changes from run to run.*

| Prompt | You should see |
|---|---|
| `Book a trip from Zurich to London for 2026-12-02 to 2026-12-04` | Flights `search_flights`: LX318, 212 CHF. Hotels `search_hotels`: Thames Bridge, 210 GBP. Policy Advisor checks the hotel limit (220 GBP per night). Travel Booking books LX318 (PNR K7Q2ZP) and the hotel (H-55120). |
| `Can I fly business class to London?` | Policy Advisor: business class only for flights over 6 hours, so economy. |
| `Do I need a visa for India? And for the UK?` | Visa Agent: India needs an e-Business visa (apply 4 days ahead); the UK needs no visa but an ETA. |
| `Submit my hotel bill of 420 GBP for reimbursement` | Expense Audit approves the hotel (2 nights at 210 GBP, within the limit). Currency `convert_currency`: 1.1483, 482.30 CHF. Expense `create_expense_report` creates ER-6610; Reimbursement schedules RB-8812 for 2026-11-25. |
| `My email is jane.doe@example.com and my phone is +41 79 123 45 67. Book a trip from Zurich to London for 2026-12-02 to 2026-12-04` | Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring. |
| `Send the first prompt more than 30 times within a minute` | The broker answers HTTP 429 (Too Many Requests) once the rate limit of 60 requests per minute is reached. |

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.

### Step 8. Trace a reply

Under each reply, the **Tracer** icon opens the task in the **Agent Network Tracer**: a waterfall of every call the broker made (gateway, broker, LLM, A2A agents, MCP tools) on one time axis, coloured like the cards. Errors are red. Click a span to see its request and response. The **Network** view shows the same reply as a sequence of calls.

### Step 9. Share it (optional)

The **Share** icon in the chat header opens the Share dialog. **A²D sessions** invites people by email to chat with this deployed broker and brings their passed / failed marks and comments back. **Local portal** generates a small web chat you can run or host anywhere.

## Path 3: Build it from scratch

Here you build the same network yourself, starting from a blank project. Every step uses a form, a menu or a button. You never import the template, and you never type YAML. The names below are the template's names without the `octo_te1g_` prefix. You can use your own names, but keep them consistent.

> The text fields take plain values. Where a value looks like `${group.name}`, type it as shown: it is a **variable** that `exchange.json` declares and that deploy fills in.

### Step 3.1. Create a blank project with a starter broker

Connect Octoloom first, as in [Path 2, Step 1](#step-1-connect-octoloom). Then, on **Home**, click **New Probabilistic Network**. In **2 Start from**, choose **Blank** and turn on **Add a starter broker**.

- **Broker name**: `travel-expense-broker`
- **Name**: `travel-expense-governed-scratch` (the Exchange asset id; a different name from the template, so both can live in one org)
- **Parent folder**: pick a folder, then click **Create blank project**.

![Blank project with a starter broker](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/scratch-new.png)

The starter broker is an LLM broker with an OpenAI LLM (`openai` provider, `openai-connection`) and default instructions. The LLM is already done.

### Step 3.2. Add the agents

On the canvas, click **+** (Add to the network) → **Agent** → **Empty**. The new agent opens in the inspector on the right. Fill it in, then repeat for each agent:

![The Add to the network menu with the Agent submenu](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/scratch-add.png)

- **Travel Booking Agent**
  - **Identity → Key**: `travel-booking-agent`
  - **Label**: Travel Booking Agent · **Description**: Books flights, hotels and rail.
  - **Metadata → Platform**: `MuleSoft` (or click its icon under **Agent framework**)
  - **Agent card**: **Name** Travel Booking Agent, **Description** as above, **URL** `${travelBookingAgent.url}`, **Protocol version** `0.3.0`
- **Policy Advisor Agent**
  - **Identity → Key**: `policy-advisor-agent`
  - **Label**: Policy Advisor Agent · **Description**: Explains the corporate travel policy.
  - **Metadata → Platform**: `AgentForce` (or click its icon under **Agent framework**)
  - **Agent card**: **Name** Policy Advisor Agent, **Description** as above, **URL** `${policyAdvisorAgent.url}`, **Protocol version** `0.3.0`
- **Visa Agent**
  - **Identity → Key**: `visa-agent`
  - **Label**: Visa Agent · **Description**: Visa and entry requirements.
  - **Metadata → Platform**: `Bedrock` (or click its icon under **Agent framework**)
  - **Agent card**: **Name** Visa Agent, **Description** as above, **URL** `${visaAgent.url}`, **Protocol version** `0.3.0`
- **Expense Audit Agent**
  - **Identity → Key**: `expense-audit-agent`
  - **Label**: Expense Audit Agent · **Description**: Audits expenses against policy.
  - **Metadata → Platform**: `OpenAI` (or click its icon under **Agent framework**)
  - **Agent card**: **Name** Expense Audit Agent, **Description** as above, **URL** `${expenseAuditAgent.url}`, **Protocol version** `0.3.0`
- **Reimbursement Agent**
  - **Identity → Key**: `reimbursement-agent`
  - **Label**: Reimbursement Agent · **Description**: Pays out approved expenses.
  - **Metadata → Platform**: `Snowflake` (or click its icon under **Agent framework**)
  - **Agent card**: **Name** Reimbursement Agent, **Description** as above, **URL** `${reimbursementAgent.url}`, **Protocol version** `0.3.0`

![An agent in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/scratch-agent.png)

The card skills are optional. Once the agent has a connection (two steps on), the inspector offers **Read skills from the live agent**, which fills them from the running agent.

### Step 3.3. Add the MCP servers

Click **+** → **MCP server** → **Empty**, then fill in:

- **Flights MCP**: **Key** `flights-mcp`, **Label** Flights MCP, **Description** Flight search. The transport is already Streamable HTTP on `/mcp`.
- **Hotels MCP**: **Key** `hotels-mcp`, **Label** Hotels MCP, **Description** Hotel search. The transport is already Streamable HTTP on `/mcp`.
- **Expense MCP**: **Key** `expense-mcp`, **Label** Expense MCP, **Description** Expense reports. The transport is already Streamable HTTP on `/mcp`.
- **Currency MCP**: **Key** `currency-mcp`, **Label** Currency MCP, **Description** Currency conversion. The transport is already Streamable HTTP on `/mcp`.

### Step 3.4. Add the connections

A connection is the URL (and authentication) Agent Fabric uses to reach an agent or an MCP server. Click **+** → **Connection** → **Empty** once per agent and MCP server, and fill in:

| Key | Kind | Target → Name | URL |
|---|---|---|---|
| `flights-mcp-connection` | `mcp` | `flights-mcp` | `${flightsMcp.url}` |
| `hotels-mcp-connection` | `mcp` | `hotels-mcp` | `${hotelsMcp.url}` |
| `expense-mcp-connection` | `mcp` | `expense-mcp` | `${expenseMcp.url}` |
| `currency-mcp-connection` | `mcp` | `currency-mcp` | `${currencyMcp.url}` |
| `travel-booking-agent-connection` | `agent` | `travel-booking-agent` | `${travelBookingAgent.url}` |
| `policy-advisor-agent-connection` | `agent` | `policy-advisor-agent` | `${policyAdvisorAgent.url}` |
| `visa-agent-connection` | `agent` | `visa-agent` | `${visaAgent.url}` |
| `expense-audit-agent-connection` | `agent` | `expense-audit-agent` | `${expenseAuditAgent.url}` |
| `reimbursement-agent-connection` | `agent` | `reimbursement-agent` | `${reimbursementAgent.url}` |

![A connection in the inspector](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/scratch-conn.png)

### Step 3.5. Declare the variables

The Problems bar now shows **Variable ${…} is not declared in exchange.json** for each new variable. Click **Add to exchange.json** on each one.

Then open `exchange.json` (it opens as a form) and, under **Variables**, set the defaults:

| Variable | Default |
|---|---|
| `ingressgw.url` | (your ingress gateway URL) |
| `flightsMcp.url` | `https://www.a2d-ai.com/api/platform/1f6d63f2-3c3d-4268-9471-40e6d18955d3/` |
| `hotelsMcp.url` | `https://www.a2d-ai.com/api/platform/6875794f-e1ea-479e-a2f8-4d9ed4b29dfc/` |
| `expenseMcp.url` | `https://www.a2d-ai.com/api/platform/75a62546-5ff3-4c98-ac92-d1bf91a1265c/` |
| `currencyMcp.url` | `https://www.a2d-ai.com/api/platform/54c12af9-4b43-4be6-a861-fe9ad82c0944/` |
| `travelBookingAgent.url` | `https://www.a2d-ai.com/api/platform/e106ec8c-02ee-4ce5-b015-2cd536b26b77/a2a` |
| `policyAdvisorAgent.url` | `https://www.a2d-ai.com/api/platform/cdf8b42e-2666-42f6-a5ae-09b40aee71bc/a2a` |
| `visaAgent.url` | `https://www.a2d-ai.com/api/platform/7256173e-0e33-484b-b11b-1f07610c1f75/a2a` |
| `expenseAuditAgent.url` | `https://www.a2d-ai.com/api/platform/bcc0eab9-61c0-48e5-9092-6d4ce1a6c0d9/a2a` |
| `reimbursementAgent.url` | `https://www.a2d-ai.com/api/platform/c0ffe718-d2aa-4298-b713-96c807aa2551/a2a` |

Leave the secret variables (`openai.apiKey`) empty: deploy asks for them and never stores them.

![The exchange.json form with the variables](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/scratch-vars.png)

### Step 3.6. Declare the MCP tools

On each MCP server card, click the **Tools** row (or its pencil). Octoloom reads the tool list from the running server: tick the tools below. You can also type a name in **Add a tool by name…**.

- **Flights MCP**: `search_flights`
- **Hotels MCP**: `search_hotels`
- **Expense MCP**: `create_expense_report`
- **Currency MCP**: `convert_currency`

![The Tools row of an MCP server card](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/scratch-tools.png)

### Step 3.7. Give the broker its agents and tools

Select the broker `travel-expense-broker`. In the inspector:

1. Click **Agents (0)**. In **Add existing agent…**, pick each agent and click **Add**: `travel-booking-agent`, `policy-advisor-agent`, `visa-agent`, `expense-audit-agent`, `reimbursement-agent`.
2. Click **MCP servers**. Add each server with **Add existing MCP server…**, then tick its **Allowed tools**:
   - `flights-mcp`: `search_flights`
   - `hotels-mcp`: `search_hotels`
   - `expense-mcp`: `create_expense_report`
   - `currency-mcp`: `convert_currency`

![The MCP servers of the broker with their allowed tools](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/scratch-links.png)

### Step 3.8. Write the broker instructions

Back in the broker inspector, open **Instructions and limits**. Replace the default instruction with these entries, one per line:

- You plan business trips and settle travel expenses.
- Check the travel policy with the Policy Advisor agent before booking anything.
- Search flights and hotels with the tools, then book through the Travel Booking agent.
- For trips abroad ask the Visa agent whether a visa is needed.
- Expenses: convert amounts with convert_currency, audit them with the Expense Audit agent and pay out through the Reimbursement agent.

Set **Max number of loops** `25`, **Max consecutive errors** `3` and **Task timeout (s)** `90`.
Under **Model parameters → OpenAI**, set **Reasoning effort** to `MINIMAL`. The broker then answers within the gateway timeout.

Optionally, fill the broker's **Agent card (A2A 0.3.0)** description: *Five specialist agents and four travel and finance tool servers plan trips and settle expenses.*

![The broker instructions and limits](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/scratch-broker.png)

### Step 3.9. Add the policies

Select the broker or connection, scroll to **Policies** and click **Add policy**. Pick the policy (search by name) and set its **Configuration** fields. **Header Injection** has its own header list. Octoloom also adds each policy as an `exchange.json` dependency.

- Broker `travel-expense-broker`: **Rate Limiting**
  - **rateLimits** (one entry each, **+**): maximumRequests `60`, timePeriodInMilliseconds `60000`
  - **exposeHeaders**: on
- Connection `flights-mcp-connection`: **MCP PII Detector**
  - **entities**: `Email`, `US SSN`, `Credit Card`, `Phone Number`
  - **action**: `Log and mask`
- Connection `hotels-mcp-connection`: **MCP Schema Validation**
  - **validateToolSchema**: on
- Connection `hotels-mcp-connection`: **Header Injection**
  - **inboundHeaders** (one entry each, **+**): `x-octoloom-source` = `travel-expense-governed-v1`
- Connection `expense-mcp-connection`: **MCP PII Detector**
  - **entities**: `Email`, `US SSN`, `Credit Card`, `Phone Number`
  - **action**: `Log and mask`
- Connection `currency-mcp-connection`: **MCP Schema Validation**
  - **validateToolSchema**: on
- Connection `currency-mcp-connection`: **Header Injection**
  - **inboundHeaders** (one entry each, **+**): `x-octoloom-source` = `travel-expense-governed-v1`
- Connection `travel-booking-agent-connection`: **A2A PII Detector**
  - **entities**: `Email`, `US SSN`, `Credit Card`
  - **action**: `Log`
- Connection `policy-advisor-agent-connection`: **Header Injection**
  - **inboundHeaders** (one entry each, **+**): `x-correlation-source` = `travel-expense-broker`
- Connection `policy-advisor-agent-connection`: **A2A Prompt Decorator**
  - **textDecorators** (one entry each, **+**): text `#['Answer concisely and never include personal data.']`
- Connection `visa-agent-connection`: **A2A PII Detector**
  - **entities**: `Email`, `US SSN`, `Credit Card`
  - **action**: `Log`
- Connection `expense-audit-agent-connection`: **Header Injection**
  - **inboundHeaders** (one entry each, **+**): `x-correlation-source` = `travel-expense-broker`
- Connection `expense-audit-agent-connection`: **A2A Prompt Decorator**
  - **textDecorators** (one entry each, **+**): text `#['Answer concisely and never include personal data.']`
- Connection `reimbursement-agent-connection`: **A2A PII Detector**
  - **entities**: `Email`, `US SSN`, `Credit Card`
  - **action**: `Log`

![Policies on the broker](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-travel-expense-governed/img/scratch-policy.png)

### Step 3.10. Validate, deploy and chat

Run **Validate** from the canvas CLI menu and fix anything in the Problems bar. Then follow Path 2 from [Validate and build](#step-4-validate-and-build) onwards: deploy (enter the secrets), wait for the green light, open the chat and send the same prompts. Your network answers like the template, because it is the same network, built by hand.

## What you learned

- How a probabilistic network is built: an LLM broker with instructions picks agents and MCP tools.
- How the canvas, the inspector and the code view edit the same YAML.
- How to build the same network from a blank project with forms and menus only (Path 3).
- How policies are attached and checked with Governance.
- How to validate, build, deploy, chat and trace with Octoloom.

## Next

- Previous: [Procurement Assistant: governed](../v1-procurement-governed/README.md)
- Next: [HR Leave Requests: secured](../v1-hr-leave-secured/README.md)
- Same use case, plain variant: [Travel & Expense](../v1-travel-expense/README.md)
- [All tutorials](../README.md)

---
Generated from the `v1-travel-expense-governed` template (Octoloom `media/templates/v1-travel-expense-governed`). Screenshots use fake data.
