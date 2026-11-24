<span class="ol-pill">Start</span>

# New project

<p class="lede"><strong>A dialog that creates an agent network from a ready-to-run template (use case, governed, secured, fully mocked, Informatica IDMC) or a blank one.</strong> Every template deploys and answers as is (A²D mocks behind every agent and MCP server), so you start from something that works.</p>

!!! info "Where to find it"
    **Home → New … Network** · **Projects & Deploy → +** · *Octoloom: New Project*

<figure markdown>
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-annot-light.webp#only-light){ loading=lazy }
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>New project: style, start from, the template list and the README preview</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **Blank** | An empty network |
| <span class="ol-n">2</span> | **Use cases** | Business scenarios |
| <span class="ol-n">3</span> | **Cancel** | Close without changes |
| <span class="ol-n">4</span> | **Create from template** | Create the project |
| <span class="ol-n">5</span> | **Explain anything** | Explain anything: click, then click any object (the guided tour starts from here too). Drag to move; double-click to reset its place |

## How to use it

1. Choose the **network style**: Deterministic (2.0, AgentScript) or Probabilistic (1.0, LLM-routed).

2. Choose **Blank**, **Use cases** or **Technical** and pick a template; the README on the right shows what it does and how to try it.

    <figure markdown>
    ![The README preview of a template: Deploy in 3 steps and Try it](../assets/ui/new-project-readme-light.webp#only-light){ loading=lazy }
    ![The README preview of a template: Deploy in 3 steps and Try it](../assets/ui/new-project-readme-dark.webp#only-dark){ loading=lazy }
    <figcaption>The README preview of a template: Deploy in 3 steps and Try it</figcaption>
    </figure>

    <figure markdown>
    ![Informatica IDMC templates in the Technical tab](../assets/ui/new-project-idmc-light.webp#only-light){ loading=lazy }
    ![Informatica IDMC templates in the Technical tab](../assets/ui/new-project-idmc-dark.webp#only-dark){ loading=lazy }
    <figcaption>Informatica IDMC templates in the Technical tab</figcaption>
    </figure>

    <figure markdown>
    ![A blank network, with or without a starter broker](../assets/ui/new-project-blank-light.webp#only-light){ loading=lazy }
    ![A blank network, with or without a starter broker](../assets/ui/new-project-blank-dark.webp#only-dark){ loading=lazy }
    <figcaption>A blank network, with or without a starter broker</figcaption>
    </figure>

3. Set the project **Name** and **Parent folder**, then **Create from template**.

4. Open the canvas, then follow *Deploy in 3 steps* from the README.

## In detail

**New Project** opens a dialog with **37 ready-made examples**: 15 business use cases, each as a plain network and as a **governed** variant with built-in Agent Fabric policies (rate limiting, PII detection, schema validation, header injection, prompt decoration). Five of them also come as a **secured** variant: every agent and MCP connection authenticates (Basic or Client ID enforcement) with `exchange.json` variables (passwords and client secrets are secret variables, asked at deploy time), the LLM URL is a variable (`llmGateway.url`, your LLM gateway or api.openai.com), the broker is rate limited and v2 upstream calls are logged with the outbound Message Logging policy.

| | Use cases | Technical (governed / secured) |
|---|---|---|
| **Deterministic (v2, AgentScript)** | insurance claims, retail returns, loan origination, field service, campaign studio, supply chain disruption, KYC / AML onboarding, IT incident response | the same 8 with policies; supply chain, KYC and incident response also secured |
| **Probabilistic (v1, LLM routing)** | customer service, employee onboarding, IT helpdesk, procurement, travel & expense, HR leave, patient intake (demo data) | the same 7 with policies; HR leave and patient intake also secured |

**Informatica IDMC (technical, both styles):** *IDMC Customer Data Steward* (v1) and *IDMC Data Trust* (v2, AgentScript) call four Informatica shared MCP servers (Customer Identification, Address Verification, CDGC Metadata Search, CDGC Data Quality Score) with OAuth 2.0 client credentials. They need an IDMC org with these services and an IDMC MCP client; their README lists the IDMC setup step by step, then how to deploy.

Pick the network style, then start **Blank**, from a **Use case** or from a **Technical** example. Each card shows the number of agents and MCP servers, the A2A versions and the policies; the right side shows the example's README: **Deploy in 3 steps** (what to connect, which variables to fill in and which secrets you are asked for at deploy) and **Try it**, 3 to 6 prompts to paste into the chat (the main path, the other branches, and for governed and secured variants a prompt that shows the policies) each with **You should see**: the agents, tools and mock ids to expect in the reply and the Agent Network Tracer. All upstreams are public A²D mocks, so a new project builds and runs without other systems; set `openai.apiKey` at deploy time. The fully mocked use cases (*Hotel Concierge*, *Library Services*, *Fleet Maintenance*, *Event Ticketing*, *Warranty Repair*, *Utility Outage*) need no OpenAI key: their scripted A²D LLM mock answers the Try it prompts the same way every time.



## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### New project

Creates an agent network project: pick the style (Probabilistic or Deterministic), a template and a name, and Octoloom writes the files. An empty network has no broker and no variables; turn on Add a starter broker for one broker to start from. Initialise a Git repository runs git init and a first commit, so every later change can be reviewed and undone with Git.

**When to use it:** Starting a network from scratch or from a template.

<figure markdown>
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-light.webp#only-light){ loading=lazy }
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-dark.webp#only-dark){ loading=lazy }
<figcaption>New project: style, start from, the template list and the README preview</figcaption>
</figure>

**Examples and details:**

- An empty network, then add brokers from the palette
- Add a starter broker: the old blank project with one broker
- Filter the templates by kind: use case, technical, governed, secured
- The preview shows the network the template creates
- Each template README has Deploy in 3 steps (the variables to set and the secrets you are asked for) and Try it: prompts to paste into the chat, with what you should see
- Two technical templates need Informatica IDMC (IDMC Customer Data Steward, IDMC Data Trust): their README lists the IDMC setup step by step (pod, MCP servers, MCP client) before the deploy steps
- Six use cases are fully mocked (Hotel Concierge, Library Services, Fleet Maintenance, Event Ticketing, Warranty Repair, Utility Outage): their LLM is an A²D LLM mock too, so they deploy and answer without an OpenAI key, the same way every time
