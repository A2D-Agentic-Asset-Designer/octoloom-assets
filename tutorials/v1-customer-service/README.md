# Tutorial: Customer Service Broker

[All tutorials](../README.md) · [Getting started](../getting-started.md) · Probabilistic network (Agent Network 1.0, LLM broker) · Use case

> One front door for orders, returns, billing and loyalty questions, backed by a CRM tool server.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 4 | 1 | 0.3.0 | 0 | `v1-customer-service` |

There are two ways to use this template:

1. **[Just use it](#path-1-just-use-it)**: create the project, deploy it and chat with it in about 10 minutes.
2. **[Learn step by step](#path-2-learn-step-by-step)**: the same steps, with what each part of the network does and how Octoloom shows it.

## Before you start

- VS Code with **Octoloom for Agent Fabric** installed (Marketplace), version 0.9.25 or later.
- An Anypoint organization with Agent Fabric, a connected app (client ID and secret), an environment and a Flex gateway.
- An OpenAI API key (or an OpenAI-compatible LLM gateway).
- Nothing else: all agents and MCP servers are public A²D mocks, so the network runs without any other system.

## Path 1: Just use it

1. **Home → Start → New Probabilistic Network.** In the dialog pick **Use cases**, then the card **Customer Service Broker**. Choose a folder and click **Create**.
2. **Deploy.** In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: OpenAI API key (secret, injected at deploy time)
3. **Chat.** When the status light is green, click **Open chat** and paste:
   - `Where is order SO-9001 for customer C-2001?`
   - `I want to return the shoes from order SO-9002`
   - `Why was I charged twice on invoice INV-7781? I am C-2001`
   - `How many points do I have? I am C-2001. Redeem them for a voucher`
   - `Exchange the shoes from SO-9002 for a bigger size`

Done. The rest of this page explains what you just ran.

## Path 2: Learn step by step

### Step 1. Connect Octoloom

Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. A²D isn't needed: the mock URLs are already the defaults in `exchange.json`. The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.

### Step 2. Create the project from the template

On **Home**, click **New Probabilistic Network**. In **2 Start from**, choose **Use cases** and click **Customer Service Broker**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `customer-service` or type your own, pick the folder and click **Create**.

![New Project dialog with Customer Service Broker selected](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-customer-service/img/new-project.png)

Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md`, and opens the canvas. Every id gets the template prefix `octo_cs1_`, so several templates can be deployed into one org side by side.

### Step 3. Read the network on the canvas

![Customer Service Broker on the Probabilistic network canvas](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-customer-service/img/canvas.png)

Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).

- **Broker octo_cs1_customer-service-broker** (`octo_cs1_customer-service-broker`): the LLM decides which agent or tool to call from its instructions.
  - Instructions:
    - You are the single front door for customer questions.
    - Identify the customer first with the CRM tool get_customer (customer ids look like C-2001).
    - Route order tracking to the Order Status agent, returns and exchanges to the Returns agent, invoices and payments to the Billing agent, and points or rewards to the Loyalty agent.
    - Open a CRM case when the request cannot be solved in this conversation.
    - Answer in a friendly tone and never invent order or invoice numbers.
- **Agent Order Status Agent**: Tracks orders and shipments.
- **Agent Returns Agent**: Handles returns, exchanges and return labels.
- **Agent Billing Agent**: Explains invoices, payments and refunds.
- **Agent Loyalty Agent**: Manages loyalty points, tiers and rewards.
- **MCP server CRM MCP**: Customer records and support cases. Tools: `get_customer`, `create_case`, `list_cases`.

Try this on the canvas: use the zoom bar and the minimap, drag a card, or **Auto layout**. The layout is saved per file. **Minimize all** turns the cards into icon tiles. Click a connection line to see which broker uses which agent or tool.

### Step 4. Validate and build

In the canvas toolbar, open the CLI menu: **Validate** does a dry run of build, publish and deploy and lists problems in the Problems panel (click one to jump to the card). **Build** repairs and packages the project locally with anypoint-cli-v4.

The variables of this template (in `exchange.json`, open it for the no-code form):

| Variable | What | Default |
|---|---|---|
| `ingressgw.url` | Ingress gateway base URL (the broker is served under it) | (fill in) |
| `crmMcp.url` | CRM MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/31f7ded2-aede-4897-8c52-19b294630e28/` |
| `orderStatusAgent.url` | Order Status Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/9d3edc31-a603-4aa6-aee9-990cb856467b/a2a` |
| `returnsAgent.url` | Returns Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/1950885c-191f-4e08-a1b5-1aa2654100a7/a2a` |
| `billingAgent.url` | Billing Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/7798938a-e34c-40db-bea2-f95f58830928/a2a` |
| `loyaltyAgent.url` | Loyalty Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/bc04526d-59b6-4e1c-816f-f93f8a1f01bd/a2a` |

### Step 5. Deploy

Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:

- `openai.apiKey`: OpenAI API key (secret, injected at deploy time)

For a probabilistic network, also fill `ingressgw.url` in `exchange.json` (your ingress gateway base URL) before you deploy.

The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.

### Step 6. Chat with the broker

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. Paste the prompts one at a time:

![Customer Service Broker in the broker chat](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v1-customer-service/img/chat.png)

*The reply in the screenshot is an illustration: it shows what the broker answers. The real wording changes from run to run.*

| Prompt | You should see |
|---|---|
| `Where is order SO-9001 for customer C-2001?` | CRM `get_customer` finds Lena Fischer (Gold). Order Status Agent: SO-9001 shipped with DHL, ETA 2026-11-12. |
| `I want to return the shoes from order SO-9002` | Order Status Agent: SO-9002 is delivered. Returns Agent opens return RMA-4410. |
| `Why was I charged twice on invoice INV-7781? I am C-2001` | Billing Agent: invoice INV-7781 has one charge and one pre-authorisation, released within 3 days. The broker may log CRM case CS-30551 with `create_case`. |
| `How many points do I have? I am C-2001. Redeem them for a voucher` | Loyalty Agent: 1,840 points, Gold tier until 2027-03-31. Redeeming 500 points gives voucher VC-5050 (10 EUR), 1,340 points left. |
| `Exchange the shoes from SO-9002 for a bigger size` | Returns Agent: exchange EX-118, size 42 replaces size 41. |

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.

### Step 7. Trace a reply

Under each reply, the **Tracer** icon opens the task in the **Agent Network Tracer**: a waterfall of every call the broker made (gateway, broker, LLM, A2A agents, MCP tools) on one time axis, coloured like the cards. Errors are red. Click a span to see its request and response. The **Network** view shows the same reply as a sequence of calls.

### Step 8. Share it (optional)

The **Share** icon in the chat header opens the Share dialog. **A²D sessions** invites people by email to chat with this deployed broker and brings their passed / failed marks and comments back. **Local portal** generates a small web chat you can run or host anywhere.

## What you learned

- How a probabilistic network is built: an LLM broker with instructions picks agents and MCP tools.
- How the canvas, the inspector and the code view edit the same YAML.
- How to validate, build, deploy, chat and trace with Octoloom.

## Next

- Next: [Employee Onboarding](../v1-employee-onboarding/README.md)
- Same use case, governed variant: [Customer Service Broker: governed](../v1-customer-service-governed/README.md)
- [All tutorials](../README.md)

---
Generated from the `v1-customer-service` template (Octoloom `media/templates/v1-customer-service`). Screenshots use fake data.
