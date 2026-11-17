# Tutorial: Insurance Claims (FNOL to Payout): governed

[All tutorials](../README.md) · [Getting started](../getting-started.md) · Deterministic network (Agent Network 2.0, AgentScript) · Technical · governed

> Classify a claim, check coverage, gate on fraud risk, then settle through adjuster and payment agents. Adds built-in policies: a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting.

| Agents | MCP servers | A2A | Policies | Template id |
|---|---|---|---|---|
| 4 | 2 | 1.0, 0.3.0 | 5 | `v2-insurance-claims-governed` |

There are two ways to use this template:

1. **[Just use it](#path-1-just-use-it)**: create the project, deploy it and chat with it in about 10 minutes.
2. **[Learn step by step](#path-2-learn-step-by-step)**: the same steps, with what each part of the network does and how Octoloom shows it.

## Before you start

- VS Code with **Octoloom for Agent Fabric** installed (Marketplace), version 0.9.25 or later.
- An Anypoint organization with Agent Fabric, a connected app (client ID and secret), an environment and a Flex gateway.
- An OpenAI API key (or an OpenAI-compatible LLM gateway).
- Nothing else: all agents and MCP servers are public A²D mocks, so the network runs without any other system.

## Path 1: Just use it

1. **Home → Start → New Deterministic Network.** In the dialog pick **Technical**, then the card **Insurance Claims (FNOL to Payout)** (the one with the policies chip). Choose a folder and click **Create**.
2. **Deploy.** In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: OpenAI API key (secret, injected at deploy time)
3. **Chat.** When the status light is green, click **Open chat** and paste:
   - `My car was hit in a parking lot, policy POL-5001`
   - `Water damage in the kitchen, policy POL-5002, about 18,000 CHF`
   - `Storm damage on my roof, policy POL-5003`
   - `My email is jane.doe@example.com and my phone is +41 79 123 45 67. My car was hit in a parking lot, policy POL-5001`
   - `Send the first prompt more than 30 times within a minute`

Done. The rest of this page explains what you just ran.

## Path 2: Learn step by step

### Step 1. Connect Octoloom

Open **Setup & Connect** (Octoloom side bar) and connect **Agent Fabric**: the connected app client ID and secret and the organization. Pick the environment. A²D isn't needed: the mock URLs are already the defaults in `exchange.json`. The Tooling list shows Node.js, Java and anypoint-cli-v4 with its agent-network plugin. Use **Install** or **Repair** on any red row.

### Step 2. Create the project from the template

On **Home**, click **New Deterministic Network**. In **2 Start from**, choose **Technical** and click **Insurance Claims (FNOL to Payout)**. The right side shows the template README: what it contains, **Deploy in 3 steps** and **Try it**. Keep the suggested name `insurance-claims-governed` or type your own, pick the folder and click **Create**.

![New Project dialog with Insurance Claims (FNOL to Payout): governed selected](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-insurance-claims-governed/img/new-project.png)

Octoloom writes `agent-network.yaml`, `exchange.json`, `README.md` and the broker flow in `brokers/`, and opens the canvas. Every id gets the template prefix `octo_ic2g_`, so several templates can be deployed into one org side by side.

### Step 3. Read the network on the canvas

![Insurance Claims (FNOL to Payout): governed on the Deterministic network canvas](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-insurance-claims-governed/img/canvas.png)

Each card is a part of `agent-network.yaml`. Click one to open it in the inspector on the right. Each change in the inspector is a change to the text, so the YAML stays the source of truth (**Code** view shows it).

- **Broker Claims Broker** (`octo_ic2g_claims_broker`): its AgentScript flow decides every step.
- **Agent FNOL Intake Agent**: Captures the first notice of loss with all required facts.
- **Agent Fraud Screening Agent**: Scores claims for fraud indicators.
- **Agent Claims Adjuster Agent**: Estimates the loss and proposes a settlement.
- **Agent Claims Payments Agent**: Pays settled claims.
- **MCP server Policy Admin MCP**: Policy administration: coverage checks. Tools: `check_coverage`.
- **MCP server Claims MCP**: Claims system of record. Tools: `create_claim`, `refer_to_siu`.

Try this on the canvas: use the zoom bar and the minimap, drag a card, or **Auto layout**. The layout is saved per file. **Minimize all** turns the cards into icon tiles. Click a connection line to see which broker uses which agent or tool.

### Step 4. Follow the broker flow (AgentScript)

Double-click the broker card (or open `brokers/claims-broker.agent`). The flow editor shows the AgentScript program that decides every step. The LLM only extracts fields and writes text, so the same input always takes the same branch.

![Insurance Claims (FNOL to Payout): governed broker flow](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-insurance-claims-governed/img/flow.png)

| Step | Kind | What it does |
|---|---|---|
| `claimsBrokerTrigger` | Trigger | Starts the flow when an A2A message arrives at the broker. |
| `classifyClaim` | Generator | Classifies the loss and extracts the policy id. |
| `assessClaim` | Orchestrator | Records the FNOL, checks coverage and screens for fraud. |
| `claimRouter` | Router | Not covered: stop. High fraud risk: refer to SIU. Otherwise settle. |
| `notCovered` | Echo | Ends the flow with the `notCovered` reply. |
| `referToSiu` | Executor | Refers the claim to the special investigations unit. |
| `referred` | Echo | Ends the flow with the `referred` reply. |
| `settleClaim` | Orchestrator | Creates the claim, gets a settlement and pays it. |
| `settled` | Echo | Ends the flow with the `settled` reply. |

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
| `fnolAgent.url` | FNOL Intake Agent (A2D mock, A2A 1.0) URL | `https://www.a2d-ai.com/api/platform/2fba0256-4819-484e-a00a-5a622f41c178/a2a` |
| `fraudAgent.url` | Fraud Screening Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/d6dbd985-7aa4-4629-be75-860b1fb9d7f0/a2a` |
| `adjusterAgent.url` | Claims Adjuster Agent (A2D mock, A2A 1.0) URL | `https://www.a2d-ai.com/api/platform/8e75ca41-b1ce-4dd8-b84c-90c80d864ce9/a2a` |
| `paymentsAgent.url` | Claims Payments Agent (A2D mock, A2A 0.3.0) URL | `https://www.a2d-ai.com/api/platform/4b5b6ba6-bbc0-48f2-a8f5-fdbe4af3f0bf/a2a` |
| `policyAdminMcp.url` | Policy Admin MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/8de15fa9-276c-459f-8243-c4b4c882fcb1/` |
| `claimsMcp.url` | Claims MCP (A2D mock) base URL | `https://www.a2d-ai.com/api/platform/587c6f66-199a-4a79-b1d4-5c77953ee271/` |

### Step 7. Deploy

Open **Projects & Deploy** and click **Deploy** on the project (or **Deploy…** on the canvas). Pick your gateway (the chips show its status and space), keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on, then enter the secrets. Nothing you type is stored:

- `openai.apiKey`: OpenAI API key (secret, injected at deploy time)

The square status light goes from blue (deploying) to green (**Deployed and running**). The deployment box lists every broker URL; click one to copy it.

### Step 8. Chat with the broker

Click **Open chat** on the deployment box. On the left is the network (the cards light up as they are called), and on the right is the conversation with its task states. Paste the prompts one at a time:

![Insurance Claims (FNOL to Payout): governed in the broker chat](https://raw.githubusercontent.com/A2D-Agentic-Asset-Designer/octoloom-assets/main/tutorials/v2-insurance-claims-governed/img/chat.png)

*The reply in the screenshot is an illustration: it shows what the broker answers. The real wording changes from run to run.*

| Prompt | You should see |
|---|---|
| `My car was hit in a parking lot, policy POL-5001` | FNOL takes the claim, Policy Admin `check_coverage` confirms motor cover, Claims `create_claim`, creates CLM-30017, Fraud: low (12), Adjuster proposes 1,980 CHF (2,480 minus 500 deductible) and Payments releases PAY-77120. |
| `Water damage in the kitchen, policy POL-5002, about 18,000 CHF` | Fraud risk high (82): new policy and amount above 10,000 CHF. Claims `refer_to_siu` opens SIU-0091 (investigator R. Meier). No payment. |
| `Storm damage on my roof, policy POL-5003` | Policy Admin: the policy lapsed. The flow ends in the not-covered branch. |
| `My email is jane.doe@example.com and my phone is +41 79 123 45 67. My car was hit in a parking lot, policy POL-5001` | Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring. |
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

- Previous: [IT Incident Response: governed](../v2-incident-response-governed/README.md)
- Next: [KYC / AML Onboarding: governed](../v2-kyc-onboarding-governed/README.md)
- Same use case, plain variant: [Insurance Claims (FNOL to Payout)](../v2-insurance-claims/README.md)
- [All tutorials](../README.md)

---
Generated from the `v2-insurance-claims-governed` template (Octoloom `media/templates/v2-insurance-claims-governed`). Screenshots use fake data.
