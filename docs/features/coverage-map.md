<span class="ol-pill">Govern</span>

# Coverage map

<p class="lede"><strong>One table of every agent network on this machine: policy coverage, protected brokers, upstream authentication, governance results, real services vs mocks, deployments.</strong> Find the gaps before a review: an open broker, a connection without authentication, a network never validated.</p>

!!! info "Where to find it"
    **Home → Your statistics → Coverage map** · *Octoloom: Coverage Map*

<figure markdown>
![Coverage map: summary cards, asset origins, the Overview table and the details of a network](../assets/ui/coverage-map-annot-light.webp#only-light){ loading=lazy }
![Coverage map: summary cards, asset origins, the Overview table and the details of a network](../assets/ui/coverage-map-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>Coverage map: summary cards, asset origins, the Overview table and the details of a network</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **This workspace** | Only the agent networks of the open workspace |
| <span class="ol-n">2</span> | **All on this machine** | Every agent network Octoloom has seen on this machine |
| <span class="ol-n">3</span> | **Refresh** | Read every project again |
| <span class="ol-n">4</span> | **A²D** | A²D: hosted mocks and prototypes. Click to show only the networks that use it. |
| <span class="ol-n">5</span> | **Agent Fabric** | Agent Fabric: MuleSoft policies and rulesets, and assets published in Exchange. Click to show only the networks that use it. |
| <span class="ol-n">6</span> | **Informatica IDMC** | Informatica IDMC: Headless IDMC MCP servers. Click to show only the networks that use it. |
| <span class="ol-n">7</span> | **P4A** | P4A: the community policy and ruleset catalog. Click to show only the networks that use it. |
| <span class="ol-n">8</span> | **Your organization** | Your organization's own policies and rulesets in Exchange. Click to show only the networks that use it. |
| <span class="ol-n">9</span> | **LLM provider** | An LLM provider declared in the project and called directly. Click to show only the networks that use it. |
| <span class="ol-n">10</span> | **Local file** | A ruleset file on this machine. Click to show only the networks that use it. |
| <span class="ol-n">11</span> | **Overview** | One row per agent network |
| <span class="ol-n">12</span> | **Policies** | Policy coverage per network |
| <span class="ol-n">13</span> | **Governance** | Governance results per network |
| <span class="ol-n">14</span> | **Authentication** | Upstream authentication per connection |
| <span class="ol-n">15</span> | **Origins** | Where the assets come from |
| <span class="ol-n">16</span> | **Lifecycle** | Validated, built, published, deployed |
| <span class="ol-n">17</span> | **LLMs** | LLM providers per network |
| <span class="ol-n">18</span> | **All styles** | Show v1 and v2 networks |
| <span class="ol-n">19</span> | **Probabilistic** | v1 networks: the LLM picks the next agent |
| <span class="ol-n">20</span> | **Deterministic** | v2 networks: an AgentScript flow decides |
| <span class="ol-n">21</span> | **Any status** | Filter by status |
| <span class="ol-n">22</span> | **Deployed** | Show only deployed projects |
| <span class="ol-n">23</span> | **Not deployed** | Show only the projects that are not deployed |
| <span class="ol-n">24</span> | **Only networks with gaps 11** | Brokers without an access policy, connections without authentication, less than half covered, never validated or with violations |
| <span class="ol-n">25</span> | **Agent Fabric** | Agent Fabric: 13 |
| <span class="ol-n">26</span> | **Agent Fabric** | Agent Fabric: 9 |
| <span class="ol-n">27</span> | **Agent Fabric** | Agent Fabric: 2 |
| <span class="ol-n">28</span> | **Agent Fabric** | Agent Fabric: 1 |

## How to use it

1. Pick **This workspace** or **All on this machine**.
2. Click a summary card (for example *Policy coverage*) to switch the table to that view.
3. In **Where your assets come from**, click a source to keep only the networks that use it.
4. Turn on *Only networks with gaps*, then click a network for its details, *Open canvas* or *Governance*.

## In detail

**Home → Your statistics → Coverage map** (or **Octoloom: Coverage Map**) opens one tab with every agent network on this machine (the projects Octoloom has seen on this user profile) or only the open workspace's.

- **Summary cards:** policy coverage, protected brokers (an access policy such as JWT Validation or Client ID Enforcement), upstream authentication of agent and MCP connections, governance (validated, conform, with violations), real services vs A²D mocks, deployed. A card switches the table to its view.
- **Where your assets come from:** a flow from each source (A²D, Agent Fabric, Informatica IDMC, P4A, your organization, an LLM provider called directly, a local ruleset file) to what it supplies: agents, MCP servers, LLMs, policies and governance rulesets. Click a source to keep only the networks that use it.
- **Seven views:** Overview, Policies (Access, Traffic, Data protection, Validation, AI guardrails, Observability), Governance, Authentication, Origins, Lifecycle and LLMs. Cells show a share as a number and a colour (red 0 %, amber below 50 %, green up to 100 %). Routing, transcoding and header policies are listed but don't count.
- **Filters:** search, style, deployed or not, *Only networks with gaps* (an open broker, a connection without authentication, less than half covered, never validated or with violations) and sorting.
- **Details:** click a network for its gaps, the rulesets of its last governance run and every broker and connection with source, authentication and policies; *Open canvas*, *Governance* and *Folder*.
- **How it is read:** the project files, the last result of the Governance panel (a small summary is kept for every project, so other workspaces show it too), the deployment records and the local statistics. P4A policies count as P4A when Octoloom applied them (once deployed, they look like your organization's). Nothing is sent anywhere and the CLI never runs.

## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### Coverage map

Every agent network on this machine in one tab: how well each one is governed and where its assets come from. Six summary cards (policy coverage, protected brokers, upstream authentication, governance, real services vs A²D mocks, deployed), a chart of the sources (A²D, Agent Fabric, Informatica IDMC, P4A, your organization, LLM providers, local ruleset files) and what they supply, and a table with seven views: Overview, Policies, Governance, Authentication, Origins, Lifecycle and LLMs. Click a network for its gaps and every component with its source, authentication and policies. Read-only and local: it reads the project files, the last Governance results and the deployment records; it never runs the CLI and sends nothing anywhere.

**When to use it:** Before a demo or a go-live, to see which networks still have unprotected brokers, connections without authentication, A²D mocks or governance violations. Open it from Home → Your statistics → Coverage map, or with the Octoloom: Coverage Map command.

**Examples and details:**

- Policies view: each cell is the share of a network's brokers and connections that have a policy of that category; routing, transcoding and header policies are listed but not counted
- Click P4A in "Where your assets come from": only the networks that use a P4A policy or ruleset stay in the table
- Only networks with gaps: brokers without an access policy, connections without authentication, less than half covered, never validated or with violations
- This workspace / All on this machine: the open workspace, or every project Octoloom has seen on this user profile
- Governance shows the last run of the Governance panel; Validate a project there and the map updates

### Coverage summary

Totals over the networks in the table (the filters apply). Policy coverage: brokers and connections with at least one policy that counts. Protected brokers: brokers with an access policy (JWT validation, client ID enforcement, OAuth token enforcement). Upstream auth: agent and MCP connections with an authentication. Governance: networks validated, conform (no violations) and with violations. Real services: agents, MCP servers and LLMs that are not A²D mocks. Deployed: networks with a deployment record, running or other.

**When to use it:** Click a card to switch the table to its view.

**Examples and details:**

- Protected brokers 2 / 14: twelve brokers accept calls without an access policy
- Real services 38%: most assets are still A²D mocks

### Where your assets come from

A flow from each source (left) to what it supplies (right): agents, MCP servers, LLMs, policies and governance rulesets. A²D is mocks and prototypes; Agent Fabric is MuleSoft policies and rulesets and assets published in Exchange; Informatica IDMC is Headless IDMC MCP servers; P4A is the community policy and ruleset catalog (policies are recorded as P4A when Octoloom applies them); your organization is your own policies and rulesets in Exchange.

**When to use it:** Click a source, its band or its row in the list to show only the networks that use it; click it again to clear the filter.

**Examples and details:**

- A²D → Agents 52: 52 agent connections still call A²D mocks
- P4A → Rulesets: networks validated with a P4A ruleset

### Coverage table

One row per agent network. Cells show a share as a number and a colour: red 0%, amber 1–49%, green 50–99% and dark green 100%; a dash means not applicable or not validated. The bars in Overview and Origins split a network's assets by source.

**When to use it:** Pick a view above the table, sort by the lowest policy coverage or the most violations, and click a row for its details.

**Examples and details:**

- Authentication view: broker access (protected or open) and the authentication kinds of the agent and MCP connections
- Lifecycle view: status light, builds, publishes, deploys and the last build on this machine

### Network details

The picked network: its policy coverage, the gaps worst first, the rulesets of the last governance run with their source, and every broker and connection with its source, authentication and policies. A policy chip shows its category by colour and where it comes from (AF = Agent Fabric, P4A, Org).

**When to use it:** Open canvas to add the missing policies or authentication, Governance to validate the project (projects of the open workspace), Folder to show it in Finder or Explorer.

**Examples and details:**

- "The broker accepts calls without an access policy": add JWT Validation or Client ID Enforcement to the broker
- "2 of 5 agent and MCP connections have no authentication": set an authentication on those connections
