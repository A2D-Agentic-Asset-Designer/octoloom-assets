<span class="ol-pill">Quick Start · Advanced · ~45 min</span>

# Advanced journey

<p class="lede">Connect A²D, build a use-case network from A²D mock agents and MCP servers, deploy it, then chat, trace and share it in an A²D session.</p>

**Needs:** Anypoint and A²D. **Steps:** 9. Open it in VS Code with **Home → Quick Start → Advanced**, or *Octoloom: Quick Start* in the Command Palette.

## The journey at a glance

1. [Anypoint account](#1-anypoint-account)
2. [Small Managed Omni Gateway](#2-small-managed-omni-gateway)
3. [Connected app Octoloom-CA](#3-connected-app-octoloom-ca)
4. [Connect Octoloom to Agent Fabric](#4-connect-octoloom-to-agent-fabric)
5. [Connect to A²D](#5-connect-to-a2d)
6. [A use-case network](#6-a-use-case-network)
7. [Build with A²D mocks](#7-build-with-a2d-mocks)
8. [Deploy to your Omni Gateway](#8-deploy-to-your-omni-gateway)
9. [Chat, trace and share](#9-chat-trace-and-share)

## Steps 1–4: the prerequisites

Every journey starts with the same four steps. Each is explained step by step, with videos, under **Before you start**:

### 1. Anypoint account

See [Anypoint account](../start/account.md).

### 2. Small Managed Omni Gateway

See [Small Managed Omni Gateway](../start/gateway.md).

### 3. Connected app Octoloom-CA

See [Connected app Octoloom-CA](../start/connected-app.md).

### 4. Connect Octoloom to Agent Fabric

See [Connect Octoloom to Agent Fabric](../start/connect-anypoint.md).

### 5. Connect to A²D

<figure markdown>
![Advanced onboarding tab, step 5 of 9: Connect to A²D](../assets/ui/qs-advanced-4-light.webp#only-light){ loading=lazy }
![Advanced onboarding tab, step 5 of 9: Connect to A²D](../assets/ui/qs-advanced-4-dark.webp#only-dark){ loading=lazy }
<figcaption>Advanced onboarding tab, step 5 of 9: Connect to A²D</figcaption>
</figure>


[A²D](https://www.a2d-ai.com) hosts **mock agents, MCP servers and LLMs**, so a network answers before the real services exist.

1. Sign up <video controls muted playsinline preload="none" poster="../assets/onboarding/videos/a2d-signup.png" src="../assets/onboarding/videos/a2d-signup.mp4" aria-label="Video: sign up for A²D" style="width:100%"></video> or sign in <video controls muted playsinline preload="none" poster="../assets/onboarding/videos/a2d-signin.png" src="../assets/onboarding/videos/a2d-signin.mp4" aria-label="Video: sign in to A²D" style="width:100%"></video> to [A²D](https://www.a2d-ai.com).
2. Open **A2D → Settings → Organization Settings → API Keys** and **create a key**. <video controls muted playsinline preload="none" poster="../assets/onboarding/videos/a2d-connect.png" src="../assets/onboarding/videos/a2d-connect.mp4" aria-label="Video: create an A²D API key and connect Octoloom" style="width:100%"></video>
3. Click **Connect A²D** (or run *Octoloom: Connect to A²D*) and paste the key.

What you get:
- the **A²D** tab of the Asset Palette: agents, MCP servers and LLM mocks of your A²D environment, ready to drop on a broker;
- **A²D sessions** in the chat's Share dialog, to let others try your deployed broker.

Self-hosted A²D: set `agentNetwork.a2dBaseUrl`.


### 6. A use-case network

<figure markdown>
![Advanced onboarding tab, step 6 of 9: A use-case network](../assets/ui/qs-advanced-5-light.webp#only-light){ loading=lazy }
![Advanced onboarding tab, step 6 of 9: A use-case network](../assets/ui/qs-advanced-5-dark.webp#only-dark){ loading=lazy }
<figcaption>Advanced onboarding tab, step 6 of 9: A use-case network</figcaption>
</figure>


Use cases are complete business networks: HR leave, IT helpdesk, retail returns, insurance claims, supply chain and more, Probabilistic and Deterministic.

1. Pick a template under **Templates for this journey** in the tab (listed at the end of this page) (or click **New project**, choose a style, then **Use cases**).
2. Name the project and create it. Its README.md lists the agents, MCP servers, LLM and policies, and prompts to try.
3. The asset names get your project name as prefix, so several projects can live in one org.

Fully mocked use cases need nothing else. The others call an LLM: set its key when you deploy, or replace the LLM with an **A²D LLM mock** in the next step.


<figure markdown>
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-light.webp#only-light){ loading=lazy }
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-dark.webp#only-dark){ loading=lazy }
<figcaption>New project: style, start from, the template list and the README preview</figcaption>
</figure>

### 7. Build with A²D mocks

<figure markdown>
![Advanced onboarding tab, step 7 of 9: Build with A²D mocks](../assets/ui/qs-advanced-6-light.webp#only-light){ loading=lazy }
![Advanced onboarding tab, step 7 of 9: Build with A²D mocks](../assets/ui/qs-advanced-6-dark.webp#only-dark){ loading=lazy }
<figcaption>Advanced onboarding tab, step 7 of 9: Build with A²D mocks</figcaption>
</figure>


1. Open the **A²D** tab of the Asset Palette.
2. Drag an **agent** or an **MCP server** onto the canvas and connect it to the broker.
3. Use the **LLMs** filter and drop an **A²D LLM mock** on a broker: it switches to the mock's model, no OpenAI key needed.
4. Check **Problems**, then **Save**.

The origin tag on each card shows which parts are still A²D mocks. Typical workflow: validate the conversation with mocks, then replace each mock with its published Agent Fabric asset.


<figure markdown>
![A²D tab: LLM mocks](../assets/ui/assets-a2d-llm-light.webp#only-light){ loading=lazy }
![A²D tab: LLM mocks](../assets/ui/assets-a2d-llm-dark.webp#only-dark){ loading=lazy }
<figcaption>A²D tab: LLM mocks</figcaption>
</figure>

### 8. Deploy to your Omni Gateway

<figure markdown>
![Advanced onboarding tab, step 8 of 9: Deploy to your Omni Gateway](../assets/ui/qs-advanced-7-light.webp#only-light){ loading=lazy }
![Advanced onboarding tab, step 8 of 9: Deploy to your Omni Gateway](../assets/ui/qs-advanced-7-dark.webp#only-dark){ loading=lazy }
<figcaption>Advanced onboarding tab, step 8 of 9: Deploy to your Omni Gateway</figcaption>
</figure>


1. In **Projects & Deploy**, click **Deploy** on the project.
2. Pick the gateway **octoloom-tutorial** from the gateway chips (green dot = running).
3. Keep **Tracing**, **Wait until the network is ready** and **Publish before deploy** on.
4. Click **Deploy**. The output goes to the **Octoloom CLI** channel; the status light turns green when the brokers answer.

A **403** means the connected app misses a scope: add the one the message names. Octoloom never undeploys or deletes what is already deployed.


<figure markdown>
![The Deploy form: gateways, target space and switches](../assets/ui/deploy-form-light.webp#only-light){ loading=lazy }
![The Deploy form: gateways, target space and switches](../assets/ui/deploy-form-dark.webp#only-dark){ loading=lazy }
<figcaption>The Deploy form: gateways, target space and switches</figcaption>
</figure>

### 9. Chat, trace and share

<figure markdown>
![Advanced onboarding tab, step 9 of 9: Chat, trace and share](../assets/ui/qs-advanced-8-light.webp#only-light){ loading=lazy }
![Advanced onboarding tab, step 9 of 9: Chat, trace and share](../assets/ui/qs-advanced-8-dark.webp#only-dark){ loading=lazy }
<figcaption>Advanced onboarding tab, step 9 of 9: Chat, trace and share</figcaption>
</figure>


1. **Deploy** to `octoloom-tutorial` and wait for the green light.
2. **Open chat**, send a sample prompt and follow the calls in **Network** and **Traces**.
3. Click **Share** in the chat header → **A²D sessions**: create a session so others can try the broker in A²D, and read their feedback with **Continue in chat**.


<figure markdown>
![Chat with live progress updates](../assets/ui/chat-progress-light.webp#only-light){ loading=lazy }
![Chat with live progress updates](../assets/ui/chat-progress-dark.webp#only-dark){ loading=lazy }
<figcaption>Chat with live progress updates</figcaption>
</figure>

<figure markdown>
![Share: A²D sessions with results](../assets/ui/chat-share-a2d-light.webp#only-light){ loading=lazy }
![Share: A²D sessions with results](../assets/ui/chat-share-a2d-dark.webp#only-dark){ loading=lazy }
<figcaption>Share: A²D sessions with results</figcaption>
</figure>

## Templates for this journey

The Advanced tab lists these templates; click one to create the project right in the tab.

| Template | Style | Agents | MCP | Tutorial |
|---|---|---|---|---|
| [Event Ticketing (fully mocked)](../catalog/v2-event-ticketing.md) | Deterministic | 2 | 2 | [Tutorial](../tutorials/v2-event-ticketing.md) |
| [Field Service Dispatch](../catalog/v2-field-service.md) | Deterministic | 3 | 4 | [Tutorial](../tutorials/v2-field-service.md) |
| [IT Incident Response](../catalog/v2-incident-response.md) | Deterministic | 5 | 2 | [Tutorial](../tutorials/v2-incident-response.md) |
| [Insurance Claims (FNOL to Payout)](../catalog/v2-insurance-claims.md) | Deterministic | 4 | 2 | [Tutorial](../tutorials/v2-insurance-claims.md) |
| [KYC / AML Onboarding](../catalog/v2-kyc-onboarding.md) | Deterministic | 2 | 3 | [Tutorial](../tutorials/v2-kyc-onboarding.md) |
| [Loan Origination](../catalog/v2-loan-origination.md) | Deterministic | 5 | 3 | [Tutorial](../tutorials/v2-loan-origination.md) |
| [Marketing Campaign Studio](../catalog/v2-campaign-studio.md) | Deterministic | 2 | 4 | [Tutorial](../tutorials/v2-campaign-studio.md) |
| [Retail Returns](../catalog/v2-retail-returns.md) | Deterministic | 2 | 1 | [Tutorial](../tutorials/v2-retail-returns.md) |
| [Supply Chain Disruption](../catalog/v2-supply-chain.md) | Deterministic | 4 | 3 | [Tutorial](../tutorials/v2-supply-chain.md) |
| [Utility Outage (fully mocked)](../catalog/v2-utility-outage.md) | Deterministic | 3 | 2 | [Tutorial](../tutorials/v2-utility-outage.md) |
| [Warranty Repair (fully mocked)](../catalog/v2-warranty-repair.md) | Deterministic | 3 | 1 | [Tutorial](../tutorials/v2-warranty-repair.md) |
| [Customer Service Broker](../catalog/v1-customer-service.md) | Probabilistic | 4 | 1 | [Tutorial](../tutorials/v1-customer-service.md) |
| [Employee Onboarding](../catalog/v1-employee-onboarding.md) | Probabilistic | 3 | 2 | [Tutorial](../tutorials/v1-employee-onboarding.md) |
| [Fleet Maintenance (fully mocked)](../catalog/v1-fleet-maintenance.md) | Probabilistic | 2 | 4 | [Tutorial](../tutorials/v1-fleet-maintenance.md) |
| [HR Leave Requests](../catalog/v1-hr-leave.md) | Probabilistic | 2 | 2 | [Tutorial](../tutorials/v1-hr-leave.md) |
| [Hotel Concierge (fully mocked)](../catalog/v1-hotel-concierge.md) | Probabilistic | 2 | 1 | [Tutorial](../tutorials/v1-hotel-concierge.md) |
| [IT Helpdesk](../catalog/v1-it-helpdesk.md) | Probabilistic | 3 | 3 | [Tutorial](../tutorials/v1-it-helpdesk.md) |
| [Library Services (fully mocked)](../catalog/v1-library-services.md) | Probabilistic | 2 | 3 | [Tutorial](../tutorials/v1-library-services.md) |
| [Patient Intake (demo data)](../catalog/v1-patient-intake.md) | Probabilistic | 3 | 1 | [Tutorial](../tutorials/v1-patient-intake.md) |
| [Procurement Assistant](../catalog/v1-procurement.md) | Probabilistic | 2 | 5 | [Tutorial](../tutorials/v1-procurement.md) |
| [Travel & Expense](../catalog/v1-travel-expense.md) | Probabilistic | 5 | 4 | [Tutorial](../tutorials/v1-travel-expense.md) |

---

**Next:** [the Expert journey](expert.md)
