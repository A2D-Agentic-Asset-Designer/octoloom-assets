<span class="ol-pill">UI reference</span>

# Side bar, Home and New project

<p class="lede">Setup & Connect, the Asset Palette, Home, the Coverage map and the New Project dialog.</p>

<figure markdown>
![The Home page: start cards, tutorials, recently built projects and your statistics](../assets/ui/welcome-annot-light.webp#only-light){ loading=lazy }
![The Home page: start cards, tutorials, recently built projects and your statistics](../assets/ui/welcome-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>The Home page: start cards, tutorials, recently built projects and your statistics</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **Quick Actions** | Collapse Quick Actions |
| <span class="ol-n">2</span> | **Open folder…** | Open the project folder |
| <span class="ol-n">3</span> | **Projects & Deploy** | The projects list with status lights |
| <span class="ol-n">4</span> | **Setup & Connect** | Connect Anypoint, A²D and IDMC |
| <span class="ol-n">5</span> | **Open the coverage map** | Open the coverage map: policies, governance, authentication and where the assets of every agent network come from |
| <span class="ol-n">6</span> | **Quick Start** | Collapse Quick Start |
| <span class="ol-n">7</span> | **Open the Beginner onboarding** | Open the Beginner onboarding: 9 steps |
| <span class="ol-n">8</span> | **Agent Fabric** | Agent Fabric is connected |
| <span class="ol-n">9</span> | **Open the Advanced onboarding** | Open the Advanced onboarding: 9 steps |
| <span class="ol-n">10</span> | **A²D** | A²D is connected |
| <span class="ol-n">11</span> | **Open the Expert onboarding** | Open the Expert onboarding: 10 steps |
| <span class="ol-n">12</span> | **Needs P4A** | Needs P4A: the onboarding shows how to connect it |
| <span class="ol-n">13</span> | **Tutorials** | Collapse Tutorials |
| <span class="ol-n">14</span> | **Getting started** | Open the Getting started tutorial on GitHub |
| <span class="ol-n">15</span> | **All template tutorials** | Open the list of template tutorials on GitHub |
| <span class="ol-n">16</span> | **Open the Octoloom documentation site** | Open the Octoloom documentation site (octoloom.a2d-ai.com): every view, button and component with screenshots |
| <span class="ol-n">17</span> | **Recently built** | Collapse Recently built |
| <span class="ol-n">18</span> | **Open folder** | Open the folder in this window |
| <span class="ol-n">19</span> | **Your statistics** | Collapse Your statistics |
| <span class="ol-n">20</span> | **Explain anything** | Explain anything: click, then click any object (the guided tour starts from here too). Drag to move; double-click to reset its place |

## Setup & Connect

One-time setup in the Octoloom side bar, most important first: Connections to Agent Fabric (business group and environment), A²D, P4A and Headless IDMC (Informatica), Tooling (Node.js, Java, anypoint-cli-v4, the agent-network plugin and Octoloom itself with a new-version notice, with install or repair), and Appearance (auto, light or dark). The line on top says how many connections are set up and whether the tools are ready. Projects & Deploy below it is for daily project work.

**When to use it:** The first time you use Octoloom, when a connection expires, or when a build says a tool is missing. It is collapsed by default and opens by itself when the workspace has no folder or no agent network project yet.

**Examples and details:**

- Appearance: Auto follows the VS Code theme; Light or Dark forces Octoloom's own palette. When the forced mode doesn't match VS Code, a hint says so with Follow VS Code
- Connect Agent Fabric with the plug button on its card, then pick the environment with the globe button
- Publish and deploy into a sub business group: pick it with the branch button next to the globe (the connected app needs scopes in that group, otherwise only the root organization is listed)
- Connect A²D with an API key to drag designed agents and MCP servers from the Asset Palette
- Connect Headless IDMC: pick the pod of your org (for example North America, dm-us), then log in with your IDMC user. The IDMC tab of the Asset Palette lists the shared and composite Informatica MCP servers. Headless IDMC needs the AI Engineering license in your Informatica org and a pod that runs it (the hdm.<pod> host); without them the IDMC tab says so
- Install missing tools after a fresh machine setup; the refresh button checks again
- Switch all Octoloom views to light or dark, independent of the VS Code theme

<figure markdown>
![Setup & Connect: connections, tooling and appearance](../assets/ui/setup-connect-light.webp#only-light){ loading=lazy }
![Setup & Connect: connections, tooling and appearance](../assets/ui/setup-connect-dark.webp#only-dark){ loading=lazy }
<figcaption>Setup & Connect: connections, tooling and appearance</figcaption>
</figure>

## Assets

The assets you can add to a network: agents and MCP servers from Exchange, A²D, Headless IDMC and your project, and LLMs from Exchange and A²D. Each card is one asset. The Agent Fabric and A²D tabs have the LLMs filter; IDMC has MCP servers and agents only. A²D LLMs are LLM mocks: fake OpenAI, Azure OpenAI or Gemini LLMs hosted by A²D that answer from scenarios (broker answers, tool calls, errors, delays), so a network runs without a real model key. Dropping one adds a project LLM (registry.llms in v2, llmProviders in v1) and an LLM connection to the mock URL, with no Exchange dependency; a mock that accepts any key gets the placeholder key a2d-mock-key, and dropped on a broker it becomes the broker LLM with the first model of the mock. The IDMC tab lists the shared Informatica MCP servers of your pod and the composite MCP servers of your org (it needs the AI Engineering license in your Informatica org and a pod that runs Headless IDMC); adding one sets its IDS-SESSION-ID authentication from the secret variable idmc.sessionId in exchange.json. LLMs (the LLMs filter) are published LLM assets: dropping one on a broker adds an exchange.json dependency (llm-metadata), an LLM connection with a URL variable and a secret apiKey variable, and makes it the broker LLM. The LLM is referenced, never copied, so publish creates no new LLM asset. LLMs with an input format (such as MuleSoft openai) work in Deterministic (v2) networks only; the Probabilistic (v1) build rejects them (error 3061).

**When to use it:** While building a network, to find what to drag onto the canvas.

**Examples and details:**

- Drag an asset card onto the network canvas to add it
- Filter the list, or search Exchange
- The hue of a card tells its kind: agent, MCP server or LLM
- IDMC tab: pick Shared or Composite, then drag a server such as Search Customer onto the canvas
- LLMs: drop your LLM proxy (an LLM asset in Exchange) on a broker; set its URL and API key variables in exchange.json or at deploy time
- A²D tab, LLMs: drop an LLM mock on a broker to deploy and chat without an OpenAI key; the reply is the mock scenario answer

<figure markdown>
![Agent Fabric tab, LLMs filter](../assets/ui/assets-llm-light.webp#only-light){ loading=lazy }
![Agent Fabric tab, LLMs filter](../assets/ui/assets-llm-dark.webp#only-dark){ loading=lazy }
<figcaption>Agent Fabric tab, LLMs filter</figcaption>
</figure>

## LLMs from Exchange

A network can declare its own LLM (registry.llms in v2, llmProviders in v1): every publish then creates a new LLM asset in Exchange for that project. Referencing a published LLM instead (an exchange.json dependency with classifier llm-metadata and a connection ref with its name and namespace) reuses one asset. New Deterministic (v2) projects and v2 templates reference MuleSoft openai. A Problem (info) points at a v2 project-declared LLM; for an OpenAI LLM its Fix switches the connections to MuleSoft openai and adds the dependency in one undoable edit.

**When to use it:** When your Exchange fills up with one LLM asset per project, or to share one LLM proxy across networks.

**Examples and details:**

- v2: connection ref { name: openai, namespace: <MuleSoft org> } plus the llm-metadata dependency: build has no "Building LLM" step
- v1: spec.llm.ref of the broker names an LLM asset without an input format, plus the dependency; MuleSoft openai is rejected (3061)
- Problems: "LLM … is declared in registry.llms" → Fix: Use MuleSoft's openai from Exchange
- Broker inspector, LLM provider: referenced LLMs are listed as "Exchange asset · v1.0.0"; pick another to replace it, or Remove LLM from broker
- On the canvas a referenced LLM has a dashed icon tile, like every asset from Exchange

<figure markdown>
![A 1.0 broker with an LLM from Exchange](../assets/ui/network-v1-exchange-llm-light.webp#only-light){ loading=lazy }
![A 1.0 broker with an LLM from Exchange](../assets/ui/network-v1-exchange-llm-dark.webp#only-dark){ loading=lazy }
<figcaption>A 1.0 broker with an LLM from Exchange</figcaption>
</figure>

## Octoloom Welcome

The start page of Octoloom, in five sections that are open by default; click a heading to fold it, and Octoloom remembers it. Quick Actions: create a Probabilistic or Deterministic network, open a folder, Projects & Deploy, Setup & Connect and the Coverage map. Quick Start: the Beginner, Advanced and Expert onboarding tabs. Tutorials: Getting started and one per template, on GitHub, and the documentation site. Recently built: the five agent network projects built last on this machine. Your statistics: your totals. The totals count workspaces, network projects (and the Probabilistic / Deterministic ratio), brokers, agents, MCP servers, Exchange, A²D and IDMC assets, governed assets (brokers, agents and MCP servers with at least one policy), policies in networks, deployments, publishes and the top 3 LLM providers. Everything is counted locally on this user profile from the projects Octoloom has seen; nothing is sent anywhere. Under the title you see the installed Octoloom version, and a link when the Marketplace has a newer one. The Tutorials section also links the Octoloom documentation site.

**When to use it:** It opens when VS Code starts (turn it off with the checkbox or the agentNetwork.showWelcome setting), not when you click the Octoloom icon. Open it any time with the home button in Projects & Deploy or the Octoloom: Welcome command.

**Examples and details:**

- Start a new Deterministic network from its card in Quick Actions: the New Project dialog opens with that style
- Fold Tutorials with its heading: it stays folded the next time Home opens
- Click a recently built project to open its canvas; Open folder opens it in this window
- Statistics count projects from every workspace you opened with Octoloom; builds, deploys and publishes are counted when they succeed
- Exchange vs A²D assets use the origin recorded when an asset was added, else the endpoint URL
- IDMC assets are MCP servers whose connection sends the IDS-SESSION-ID header or points at informaticacloud.com
- Governed assets count each broker, agent or MCP server once, however many policies it has

## Tutorials

Links to the Octoloom tutorials on GitHub (octoloom-assets/tutorials): Getting started, a tour of Octoloom from Setup & Connect to chat, trace and share, and one tutorial per template project. Each template tutorial has three paths: Just use it (create, deploy, chat in 3 steps), Learn step by step (the canvas, the broker flow, policies, validate, build, deploy, chat and trace, explained with screenshots) and Build it from scratch (start from an empty project and add every broker, agent, MCP server, LLM, connection and policy yourself, with screenshots). The Documentation link opens the Octoloom documentation site (octoloom.a2d-ai.com): every view, button and component explained with screenshots, all templates and tutorials, and the version history.

**When to use it:** You are new to Octoloom, or want to see what a template does before you create it. The links open in your browser.

**Examples and details:**

- Getting started: the 10-step tour
- All template tutorials: the list of every template, Probabilistic and Deterministic, with its agents, MCP servers and policies
- Retail Returns is the smallest deterministic template to start with
- Build it from scratch: the same network as the template, built card by card from New Project → Empty

## Octoloom version

The Octoloom version installed in this VS Code. Once per session Octoloom reads the latest version from the public Visual Studio Marketplace (a read-only request that sends no project or usage data). When a newer version exists, Octoloom Welcome and Setup & Connect → Tooling say "<version> available"; click it to open Octoloom in the Extensions view and update.

**When to use it:** Check which version you run before you report a problem, or update when a new version is available. Offline or behind a proxy, only the installed version is shown.

**Examples and details:**

- Octoloom Welcome: "Version 0.9.25" under the title
- Tooling: the Octoloom row shows the installed version, with a warning and "0.9.26 available" when there is an update
- Click "available" to open the extension page in the Extensions view, where Update installs it

<figure markdown>
![The installed version, with a link when the Marketplace has a newer one](../assets/ui/welcome-update-light.webp#only-light){ loading=lazy }
![The installed version, with a link when the Marketplace has a newer one](../assets/ui/welcome-update-dark.webp#only-dark){ loading=lazy }
<figcaption>The installed version, with a link when the Marketplace has a newer one</figcaption>
</figure>

## Coverage map

Every agent network on this machine in one tab: how well each one is governed and where its assets come from. Six summary cards (policy coverage, protected brokers, upstream authentication, governance, real services vs A²D mocks, deployed), a chart of the sources (A²D, Agent Fabric, Informatica IDMC, P4A, your organization, LLM providers, local ruleset files) and what they supply, and a table with seven views: Overview, Policies, Governance, Authentication, Origins, Lifecycle and LLMs. Click a network for its gaps and every component with its source, authentication and policies. Read-only and local: it reads the project files, the last Governance results and the deployment records; it never runs the CLI and sends nothing anywhere.

**When to use it:** Before a demo or a go-live, to see which networks still have unprotected brokers, connections without authentication, A²D mocks or governance violations. Open it from Home → Quick Actions or Your statistics → Coverage map, or with the Octoloom: Coverage Map command.

**Examples and details:**

- Policies view: each cell is the share of a network's brokers and connections that have a policy of that category; routing, transcoding and header policies are listed but not counted
- Click P4A in "Where your assets come from": only the networks that use a P4A policy or ruleset stay in the table
- Only networks with gaps: brokers without an access policy, connections without authentication, less than half covered, never validated or with violations
- This workspace / All on this machine: the open workspace, or every project Octoloom has seen on this user profile
- Governance shows the last run of the Governance panel; Validate a project there and the map updates

<figure markdown>
![Coverage map: summary cards, asset origins, the Overview table and the details of a network](../assets/ui/coverage-map-light.webp#only-light){ loading=lazy }
![Coverage map: summary cards, asset origins, the Overview table and the details of a network](../assets/ui/coverage-map-dark.webp#only-dark){ loading=lazy }
<figcaption>Coverage map: summary cards, asset origins, the Overview table and the details of a network</figcaption>
</figure>

## Coverage summary

Totals over the networks in the table (the filters apply). Policy coverage: brokers and connections with at least one policy that counts. Protected brokers: brokers with an access policy (JWT validation, client ID enforcement, OAuth token enforcement). Upstream auth: agent and MCP connections with an authentication. Governance: networks validated, conform (no violations) and with violations. Real services: agents, MCP servers and LLMs that are not A²D mocks. Deployed: networks with a deployment record, running or other.

**When to use it:** Click a card to switch the table to its view.

**Examples and details:**

- Protected brokers 2 / 14: twelve brokers accept calls without an access policy
- Real services 38%: most assets are still A²D mocks

## Where your assets come from

A flow from each source (left) to what it supplies (right): agents, MCP servers, LLMs, policies and governance rulesets. A²D is mocks and prototypes; Agent Fabric is MuleSoft policies and rulesets and assets published in Exchange; Informatica IDMC is Headless IDMC MCP servers; P4A is the community policy and ruleset catalog (policies are recorded as P4A when Octoloom applies them); your organization is your own policies and rulesets in Exchange.

**When to use it:** Click a source, its band or its row in the list to show only the networks that use it; click it again to clear the filter.

**Examples and details:**

- A²D → Agents 52: 52 agent connections still call A²D mocks
- P4A → Rulesets: networks validated with a P4A ruleset

## Coverage table

One row per agent network. Cells show a share as a number and a colour: red 0%, amber 1–49%, green 50–99% and dark green 100%; a dash means not applicable or not validated. The bars in Overview and Origins split a network's assets by source.

**When to use it:** Pick a view above the table, sort by the lowest policy coverage or the most violations, and click a row for its details.

**Examples and details:**

- Authentication view: broker access (protected or open) and the authentication kinds of the agent and MCP connections
- Lifecycle view: status light, builds, publishes, deploys and the last build on this machine

## Network details

The picked network: its policy coverage, the gaps worst first, the rulesets of the last governance run with their source, and every broker and connection with its source, authentication and policies. A policy chip shows its category by colour and where it comes from (AF = Agent Fabric, P4A, Org).

**When to use it:** Open canvas to add the missing policies or authentication, Governance to validate the project (projects of the open workspace), Folder to show it in Finder or Explorer.

**Examples and details:**

- "The broker accepts calls without an access policy": add JWT Validation or Client ID Enforcement to the broker
- "2 of 5 agent and MCP connections have no authentication": set an authentication on those connections

## New project

Creates an agent network project: pick the style (Probabilistic or Deterministic), a template and a name, and Octoloom writes the files. An empty network has no broker and no variables; turn on Add a starter broker for one broker to start from. Above the templates, filter chips narrow the list: Level (Beginner: fully mocked use cases, no LLM key; Advanced: the other use cases; Expert: governed, secured and IDMC networks), Industry, Needs (nothing else, an LLM key, Informatica IDMC) and Time; each chip shows how many templates it leaves, and Clear filters resets them. A Quick Start journey opens New Project with its level already set; click the chip to remove it. Initialise a Git repository runs git init and a first commit, so every later change can be reviewed and undone with Git.

**When to use it:** Starting a network from scratch or from a template.

**Examples and details:**

- An empty network, then add brokers from the palette
- Add a starter broker: the old blank project with one broker
- Filter the templates by kind: use case, technical, governed, secured
- Level Beginner + Industry Travel & hospitality: the fully mocked Hotel Concierge or Event Ticketing
- Needs: Nothing else lists the templates that run with only an Anypoint org
- The preview shows the network the template creates
- Each template README has Deploy in 3 steps (the variables to set and the secrets you are asked for) and Try it: prompts to paste into the chat, with what you should see
- Two technical templates need Informatica IDMC (IDMC Customer Data Steward, IDMC Data Trust): their README lists the IDMC setup step by step (pod, MCP servers, MCP client) before the deploy steps
- Six use cases are fully mocked (Hotel Concierge, Library Services, Fleet Maintenance, Event Ticketing, Warranty Repair, Utility Outage): their LLM is an A²D LLM mock too, so they deploy and answer without an OpenAI key, the same way every time

<figure markdown>
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-light.webp#only-light){ loading=lazy }
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-dark.webp#only-dark){ loading=lazy }
<figcaption>New project: style, start from, the template list and the README preview</figcaption>
</figure>

## Agent network from Exchange

Downloads an agent network that is published in Exchange (by you or a colleague) and opens it as an Octoloom project. The dialog lists only Agent Network assets, Deterministic and Probabilistic. The chosen version is saved in a new folder of your workspace, which is never overwritten.

**When to use it:** To reuse, review, govern or redeploy a network that lives in Exchange, or to continue work on another machine.

**Examples and details:**

- Click the Exchange icon next to + in Projects & Deploy, or choose From Exchange in the + menu
- Search by name, switch between your organization and everything you can see, and pick a version
- Secrets are not in Exchange: set them again when you deploy
- If the exchange.json version is already published, bump it before the next Publish

<figure markdown>
![Agent network from Exchange: networks of the org, version picker and Save to](../assets/ui/exchange-import-light.webp#only-light){ loading=lazy }
![Agent network from Exchange: networks of the org, version picker and Save to](../assets/ui/exchange-import-dark.webp#only-dark){ loading=lazy }
<figcaption>Agent network from Exchange: networks of the org, version picker and Save to</figcaption>
</figure>
