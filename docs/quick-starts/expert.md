<span class="ol-pill">Quick Start · Expert · ~60 min</span>

# Expert journey

<p class="lede">Connect A²D and P4A, start from a governed or secured technical template, add P4A and Agent Fabric policies, validate governance and check the Coverage map.</p>

**Needs:** Anypoint, A²D and P4A. **Steps:** 10. Open it in VS Code with **Home → Quick Start → Expert**, or *Octoloom: Quick Start* in the Command Palette.

## The journey at a glance

1. [Anypoint account](#1-anypoint-account)
2. [Small Managed Omni Gateway](#2-small-managed-omni-gateway)
3. [Connected app Octoloom-CA](#3-connected-app-octoloom-ca)
4. [Connect Octoloom to Agent Fabric](#4-connect-octoloom-to-agent-fabric)
5. [Connect to A²D](#5-connect-to-a2d)
6. [Connect to P4A](#6-connect-to-p4a)
7. [A technical network](#7-a-technical-network)
8. [Agent Fabric and P4A policies](#8-agent-fabric-and-p4a-policies)
9. [Validate the governance](#9-validate-the-governance)
10. [Deploy and check the coverage](#10-deploy-and-check-the-coverage)

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
![Expert onboarding tab, step 5 of 10: Connect to A²D](../assets/ui/qs-expert-4-light.webp#only-light){ loading=lazy }
![Expert onboarding tab, step 5 of 10: Connect to A²D](../assets/ui/qs-expert-4-dark.webp#only-dark){ loading=lazy }
<figcaption>Expert onboarding tab, step 5 of 10: Connect to A²D</figcaption>
</figure>


[A²D](https://www.a2d-ai.com) hosts **mock agents, MCP servers and LLMs**, so a network answers before the real services exist.

1. Sign up <video controls muted playsinline preload="none" poster="../assets/onboarding/videos/a2d-signup.png" src="../assets/onboarding/videos/a2d-signup.mp4" aria-label="Video: sign up for A²D" style="width:100%"></video> or sign in <video controls muted playsinline preload="none" poster="../assets/onboarding/videos/a2d-signin.png" src="../assets/onboarding/videos/a2d-signin.mp4" aria-label="Video: sign in to A²D" style="width:100%"></video> to [A²D](https://www.a2d-ai.com).
2. Open **A2D → Settings → Organization Settings → API Keys** and **create a key**. <video controls muted playsinline preload="none" poster="../assets/onboarding/videos/a2d-connect.png" src="../assets/onboarding/videos/a2d-connect.mp4" aria-label="Video: create an A²D API key and connect Octoloom" style="width:100%"></video>
3. Click **Connect A²D** (or run *Octoloom: Connect to A²D*) and paste the key.

What you get:
- the **A²D** tab of the Asset Palette: agents, MCP servers and LLM mocks of your A²D environment, ready to drop on a broker;
- **A²D sessions** in the chat's Share dialog, to let others try your deployed broker.

Self-hosted A²D: set `agentNetwork.a2dBaseUrl`.


### 6. Connect to P4A

<figure markdown>
![Expert onboarding tab, step 6 of 10: Connect to P4A](../assets/ui/qs-expert-5-light.webp#only-light){ loading=lazy }
![Expert onboarding tab, step 6 of 10: Connect to P4A](../assets/ui/qs-expert-5-dark.webp#only-dark){ loading=lazy }
<figcaption>Expert onboarding tab, step 6 of 10: Connect to P4A</figcaption>
</figure>


[P4A](https://www.p4a.ai) is a catalog of **policies and governance rulesets** for Agent Fabric, on top of the MuleSoft policies.

1. Sign up <video controls muted playsinline preload="none" poster="../assets/onboarding/videos/p4a-signup.png" src="../assets/onboarding/videos/p4a-signup.mp4" aria-label="Video: sign up for P4A" style="width:100%"></video> or sign in <video controls muted playsinline preload="none" poster="../assets/onboarding/videos/p4a-signin.png" src="../assets/onboarding/videos/p4a-signin.mp4" aria-label="Video: sign in to P4A" style="width:100%"></video> to [P4A](https://www.p4a.ai).
2. Open **Settings → Personal Access Tokens** and create a token (it starts with `p4a_`). <video controls muted playsinline preload="none" poster="../assets/onboarding/videos/p4a-connect.png" src="../assets/onboarding/videos/p4a-connect.mp4" aria-label="Video: create a P4A personal access token and connect Octoloom" style="width:100%"></video>
3. Click **Connect P4A** (or run *Octoloom: Connect to P4A*) and paste the token.
4. To **deploy** P4A policies, set up in P4A a **connection to your Anypoint organization** and a **workspace**.

What you get:
- P4A policies in the policy picker of a broker or connection, next to the Agent Fabric policies;
- your P4A rulesets in **Governance**.

Another P4A host: set `agentNetwork.p4aBaseUrl`.


### 7. A technical network

<figure markdown>
![Expert onboarding tab, step 7 of 10: A technical network](../assets/ui/qs-expert-6-light.webp#only-light){ loading=lazy }
![Expert onboarding tab, step 7 of 10: A technical network](../assets/ui/qs-expert-6-dark.webp#only-dark){ loading=lazy }
<figcaption>Expert onboarding tab, step 7 of 10: A technical network</figcaption>
</figure>


Technical templates are use cases with built-in **policies**: *governed* (rate limits, JWT validation, prompt guards, PII masking…) and *secured* (protected brokers, authenticated connections).

1. Pick a template under **Templates for this journey** in the tab (listed at the end of this page) (or click **New project**, choose a style, then **Technical**).
2. Pick a *governed* or *secured* template, for example *Supply Chain Disruption: secured*.
3. Create it and look at the policy chips on the brokers and connections.

The two IDMC templates need an Informatica IDMC org (**Setup & Connect → IDMC**).


<figure markdown>
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-light.webp#only-light){ loading=lazy }
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-dark.webp#only-dark){ loading=lazy }
<figcaption>New project: style, start from, the template list and the README preview</figcaption>
</figure>

### 8. Agent Fabric and P4A policies

<figure markdown>
![Expert onboarding tab, step 8 of 10: Agent Fabric and P4A policies](../assets/ui/qs-expert-7-light.webp#only-light){ loading=lazy }
![Expert onboarding tab, step 8 of 10: Agent Fabric and P4A policies](../assets/ui/qs-expert-7-dark.webp#only-dark){ loading=lazy }
<figcaption>Expert onboarding tab, step 8 of 10: Agent Fabric and P4A policies</figcaption>
</figure>


1. Click the **policy** button of a broker or a connection.
2. The picker lists the **Agent Fabric** (MuleSoft) policies and, with P4A connected, the **P4A** policies.
3. Add an access policy to every broker (JWT Validation, Client ID Enforcement or OAuth token enforcement) and an authentication to every agent and MCP connection.
4. Save. The policies are written to `agent-network.yaml`.

P4A policies deploy through your P4A connection to the Anypoint org; Octoloom asks before it deploys one.


<figure markdown>
![The policy picker](../assets/ui/policy-picker-light.webp#only-light){ loading=lazy }
![The policy picker](../assets/ui/policy-picker-dark.webp#only-dark){ loading=lazy }
<figcaption>The policy picker</figcaption>
</figure>

### 9. Validate the governance

<figure markdown>
![Expert onboarding tab, step 9 of 10: Validate the governance](../assets/ui/qs-expert-8-light.webp#only-light){ loading=lazy }
![Expert onboarding tab, step 9 of 10: Validate the governance](../assets/ui/qs-expert-8-dark.webp#only-dark){ loading=lazy }
<figcaption>Expert onboarding tab, step 9 of 10: Validate the governance</figcaption>
</figure>


1. Click the **Governance** shield in the project's header.
2. Pick the rulesets: **Agent Fabric**, your **organization**, **P4A**, or local ruleset files.
3. **Validate**. Conformance shows per broker, agent and MCP server; the canvas marks the components with findings.
4. Use **Fix** or **Fix all** where offered, then validate again.

Governance runs locally with the CLI; nothing is sent to your org.


<figure markdown>
![Governance: rulesets, the project canvas and findings](../assets/ui/governance-light.webp#only-light){ loading=lazy }
![Governance: rulesets, the project canvas and findings](../assets/ui/governance-dark.webp#only-dark){ loading=lazy }
<figcaption>Governance: rulesets, the project canvas and findings</figcaption>
</figure>

### 10. Deploy and check the coverage

<figure markdown>
![Expert onboarding tab, step 10 of 10: Deploy and check the coverage](../assets/ui/qs-expert-9-light.webp#only-light){ loading=lazy }
![Expert onboarding tab, step 10 of 10: Deploy and check the coverage](../assets/ui/qs-expert-9-dark.webp#only-dark){ loading=lazy }
<figcaption>Expert onboarding tab, step 10 of 10: Deploy and check the coverage</figcaption>
</figure>


1. **Deploy** to `octoloom-tutorial` and chat with the broker.
2. Open the **Coverage map** (Home → Quick Actions, or *Octoloom: Coverage Map*).
3. Check policy coverage, protected brokers, upstream authentication, governance and A²D mocks vs real services for every network on this machine.
4. Click your network for its gaps, worst first.


<figure markdown>
![Coverage map: summary cards, asset origins, the Overview table and the details of a network](../assets/ui/coverage-map-light.webp#only-light){ loading=lazy }
![Coverage map: summary cards, asset origins, the Overview table and the details of a network](../assets/ui/coverage-map-dark.webp#only-dark){ loading=lazy }
<figcaption>Coverage map: summary cards, asset origins, the Overview table and the details of a network</figcaption>
</figure>

## Templates for this journey

The Expert tab lists these templates; click one to create the project right in the tab.

| Template | Style | Agents | MCP | Tutorial |
|---|---|---|---|---|
| [Field Service Dispatch: governed](../catalog/v2-field-service-governed.md) | Deterministic | 3 | 4 | [Tutorial](../tutorials/v2-field-service-governed.md) |
| [IDMC Data Trust (needs Informatica IDMC)](../catalog/v2-idmc-data-trust.md) | Deterministic | 0 | 4 | [Tutorial](../tutorials/v2-idmc-data-trust.md) |
| [IT Incident Response: governed](../catalog/v2-incident-response-governed.md) | Deterministic | 5 | 2 | [Tutorial](../tutorials/v2-incident-response-governed.md) |
| [IT Incident Response: secured](../catalog/v2-incident-response-secured.md) | Deterministic | 5 | 2 | [Tutorial](../tutorials/v2-incident-response-secured.md) |
| [Insurance Claims (FNOL to Payout): governed](../catalog/v2-insurance-claims-governed.md) | Deterministic | 4 | 2 | [Tutorial](../tutorials/v2-insurance-claims-governed.md) |
| [KYC / AML Onboarding: governed](../catalog/v2-kyc-onboarding-governed.md) | Deterministic | 2 | 3 | [Tutorial](../tutorials/v2-kyc-onboarding-governed.md) |
| [KYC / AML Onboarding: secured](../catalog/v2-kyc-onboarding-secured.md) | Deterministic | 2 | 3 | [Tutorial](../tutorials/v2-kyc-onboarding-secured.md) |
| [Loan Origination: governed](../catalog/v2-loan-origination-governed.md) | Deterministic | 5 | 3 | [Tutorial](../tutorials/v2-loan-origination-governed.md) |
| [Marketing Campaign Studio: governed](../catalog/v2-campaign-studio-governed.md) | Deterministic | 2 | 4 | [Tutorial](../tutorials/v2-campaign-studio-governed.md) |
| [Retail Returns: governed](../catalog/v2-retail-returns-governed.md) | Deterministic | 2 | 1 | [Tutorial](../tutorials/v2-retail-returns-governed.md) |
| [Supply Chain Disruption: governed](../catalog/v2-supply-chain-governed.md) | Deterministic | 4 | 3 | [Tutorial](../tutorials/v2-supply-chain-governed.md) |
| [Supply Chain Disruption: secured](../catalog/v2-supply-chain-secured.md) | Deterministic | 4 | 3 | [Tutorial](../tutorials/v2-supply-chain-secured.md) |
| [Customer Service Broker: governed](../catalog/v1-customer-service-governed.md) | Probabilistic | 4 | 1 | [Tutorial](../tutorials/v1-customer-service-governed.md) |
| [Employee Onboarding: governed](../catalog/v1-employee-onboarding-governed.md) | Probabilistic | 3 | 2 | [Tutorial](../tutorials/v1-employee-onboarding-governed.md) |
| [HR Leave Requests: governed](../catalog/v1-hr-leave-governed.md) | Probabilistic | 2 | 2 | [Tutorial](../tutorials/v1-hr-leave-governed.md) |
| [HR Leave Requests: secured](../catalog/v1-hr-leave-secured.md) | Probabilistic | 2 | 2 | [Tutorial](../tutorials/v1-hr-leave-secured.md) |
| [IDMC Customer Data Steward (needs Informatica IDMC)](../catalog/v1-idmc-customer-steward.md) | Probabilistic | 0 | 4 | [Tutorial](../tutorials/v1-idmc-customer-steward.md) |
| [IT Helpdesk: governed](../catalog/v1-it-helpdesk-governed.md) | Probabilistic | 3 | 3 | [Tutorial](../tutorials/v1-it-helpdesk-governed.md) |
| [Patient Intake (demo data): governed](../catalog/v1-patient-intake-governed.md) | Probabilistic | 3 | 1 | [Tutorial](../tutorials/v1-patient-intake-governed.md) |
| [Patient Intake (demo data): secured](../catalog/v1-patient-intake-secured.md) | Probabilistic | 3 | 1 | [Tutorial](../tutorials/v1-patient-intake-secured.md) |
| [Procurement Assistant: governed](../catalog/v1-procurement-governed.md) | Probabilistic | 2 | 5 | [Tutorial](../tutorials/v1-procurement-governed.md) |
| [Travel & Expense: governed](../catalog/v1-travel-expense-governed.md) | Probabilistic | 5 | 4 | [Tutorial](../tutorials/v1-travel-expense-governed.md) |

---

**Next:** [pick a tutorial](../tutorials/index.md)
