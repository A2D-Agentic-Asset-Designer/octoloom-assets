<span class="ol-pill">Version</span>

# Version history

<p class="lede">Every Octoloom release from the very first, newest first: what changed, in plain words, and who made it happen. <b>60 versions</b>, <b>216 changes</b>.</p>

## Contributors

Everyone who suggested or built a change. A change counts for the person who filed the request and for the person who implemented it; a change without a request is credited to its implementer.

[Amir Khan](https://github.com/amirkhan-ak-sf) · [Gabriel Bustos Sölch](https://github.com/gabrielmule) · [George Jeffcock](https://github.com/jeffcock) · [Tommaso Bolis](https://github.com/tommasobolis) · [Burak Tas](https://github.com/burak-tas)

## 0.9.29

<span class="ol-ver-meta">in development</span>

- **Setup gateways asks for the space**. Setup gateways ran the CLI without a target space, so it picked one the user never chose and never said which. It now asks for the space type (Shared Space or Private Space), the space (from the spaces of the connected organization, or typed when they cannot be read) and the gateway name (agent-network-shared-gw for a shared space, agent-network-gw for a private space), runs agent-network:setup:gateways with -g and -t, and the message at the end names the space.

    <span class="ol-by">:material-account-heart-outline: [Tommaso Bolis](https://github.com/tommasobolis), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Broker canvas: agent actions get their own section**. A card on the AgentScript flow canvas showed every action under one Actions section with the MCP icon, also the actions that send an A2A message to an agent. Now MCP tools are listed under **MCP actions** (MCP icon and colour, as before) and agents under **Agent actions** (agent icon and colour), each only when the card has such actions; a card without actions keeps the single empty Actions section. Folded sections stay folded. Actions that are not defined stay with the MCP actions and keep their error mark. The Tracer graph is unchanged.

    <span class="ol-by">:material-account-heart-outline: [Tommaso Bolis](https://github.com/tommasobolis), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Templates deploy on every control plane**. MuleSoft publishes its policies and the `openai` LLM under a different organization in each control plane (US, EU, Canada, Japan); templates and new projects named the US one, so on an EU org the pre-deploy check said *openai 1.0.0 can't be read by the connected organization*. New projects, the policy picker and the *Use the Exchange LLM* fix now use the organization of the control plane you are connected to; the Coverage map counts MuleSoft policies of every control plane as Agent Fabric. Credits: reported, built and committed by [Amir Khan](https://github.com/amirkhan-ak-sf).

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Quick Start: recorded videos and create from the tab**. The onboarding pages show 11 short videos instead of the Anypoint pictures: Anypoint sign-up and log-in, the Small Managed Omni Gateway, the connected app Octoloom-CA, connecting Agent Fabric, and now also signing up, signing in and connecting **A²D** and **P4A**. Names, e-mail addresses, organization names and ids, keys and tokens are blurred. Each video is a small thumbnail next to the instruction it shows; a click opens it in a dialog (Escape closes it). H.264 MP4, about 5 MB in all. A template card under *Templates for this journey* no longer opens New agent network: it opens the **Project** step of New Project right in the tab (name, parent folder, after creating, Git), creates the project with the same code, adds it to Projects & Deploy and runs the After-creating action; errors such as a taken name show in the form.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf), [Tommaso Bolis](https://github.com/tommasobolis), [George Jeffcock](https://github.com/jeffcock)</span>

- **Setup & Connect: connection cards follow the side bar width**. The Agent Fabric, A²D, P4A and Headless IDMC cards now shrink with the side bar: the description shortens with an ellipsis and the button always stays in view. **Connect** is a plug button (tooltip *Connect to <name>*).

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Anonymous usage counts (telemetry)**. Octoloom now counts how it is used, so we can see which features help: start-ups, a daily ping with which connections are set up (yes or no), Build / Validate / Publish / Deploy / Governance runs with their result, New Project with the style and template id, the commands used (once per command per day) and the class of an error (never its message). No names, paths, URLs, hosts, org data, prompts, chat text or keys are ever sent; the only id is VS Code's random machine id, and no person profiles are created. Events go to PostHog Cloud EU (country only, the IP is discarded). VS Code's `telemetry.telemetryLevel` always wins; the new setting **`agentNetwork.telemetry.enabled`** turns it off for Octoloom only, and a one-time notice offers **Turn off**. Every event and property is listed in `telemetry.json`; the README *Privacy and security* section explains what is sent, how long it is kept and how to ask for deletion.

    <span class="ol-by">:material-account-heart-outline: [Tommaso Bolis](https://github.com/tommasobolis), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Home: Quick Start journeys and foldable sections**. Home now has five sections that are open by default and fold with their heading, remembered per user: **Quick Actions** (was *Start*, now with a Coverage map link), **Quick Start**, Tutorials, Recently built and Your statistics. Quick Start has **Beginner**, **Advanced** and **Expert** cards with walking, running and climbing icons. Each opens its own **onboarding tab**: the steps on the left, the page of the step on the right with pictures of the Anypoint screens (organization names blurred), buttons that open the right Octoloom view or site, Previous / Next and Mark as done. Each journey lists only its own templates (Beginner: fully mocked; Advanced: the other use cases; Expert: technical). Reopen a journey with *Octoloom: Quick Start*. Every journey starts with the same prerequisites: an Anypoint account, a Small Managed Omni Gateway (Edge 1.15.0 or later, 60 s upstream and idle timeouts, Distributed Tracing), a connected app with least-privilege scopes, and the connection to Agent Fabric. Advanced adds the A²D connection and Expert adds A²D and P4A. The Connect steps tick themselves off, and **Check my gateway** (*Octoloom: Check Omni Gateway*) lists the gateways of the connected environment.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf), [Tommaso Bolis](https://github.com/tommasobolis), [George Jeffcock](https://github.com/jeffcock)</span>


## 0.9.28

<span class="ol-ver-meta">2026-11-23 · released</span>

- **Documentation site from Home and Explain**. Home → Tutorials has a **Documentation** link to [octoloom.a2d-ai.com](https://octoloom.a2d-ai.com/), and every Explain card has a **Docs** link that opens the site with a search for that object.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Headless IDMC: clear message instead of "fetch failed"**. When the pod has no Headless IDMC host (for example `dmp-em`), the IDMC tab says so and names what Headless IDMC needs: the **AI Engineering** license in your Informatica org and a pod that runs it. 401/403 answers from the IDMC MCP services carry the same hint, and connecting warns when the pod has no Headless IDMC. Explain, README and Requirements name the license.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Templates: live progress in the chat**. Every deterministic (v2) template now tells the caller what it does next: before each step its flow sends a *working* status update with a plain sentence (*Checking the free seats with the Events MCP...*, *Issuing the e-tickets through the Ticketing agent...*), then goes on. With **Live** on, the chat lists them while the broker works. The updates are ordinary Reply nodes in `brokers/*.agent` (no LLM call) that you can edit or remove in the flow editor. Brokers already deployed keep their flow until you redeploy them from a new project. The template READMEs (*Try it*) and the tutorials mention the **Live progress** toggle (antenna next to Send, on by default).

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Docs: meet Loomi**. The Octoloom octopus has a name: **Loomi** (he/him). The README introduces him and the logo alt texts name him.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf), [George Jeffcock](https://github.com/jeffcock)</span>


## 0.9.27

<span class="ol-ver-meta">2026-11-20 · released</span>

- **Chat: working, not stuck**. While a broker works on a message, its bubble says so in plain words (*Sending your message…*, *Got your request. Getting started…*, *Working on it…*) with the seconds so far, and after 10 s *Still working, not stuck* (a broker that sends no step messages is said to answer in one go). v2 brokers (A2A 1.0) stream their status updates (`SendStreamingMessage`), and each one is listed with its time, the state in plain words and the broker's own message. A **Live** button left of Send turns the stream on or off (kept per machine); a broker that doesn't stream falls back to the normal send. v1 brokers (A2A 0.3) can't stream or be asked for their task, so they get the time-based progress.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **A²D LLM mocks in the Asset Palette**. The A²D tab has an **LLMs** filter with the LLM mocks of your A²D environment (OpenAI, Azure OpenAI, Bedrock OpenAI, Gemini). Dropping one on a broker adds a project LLM (v2 `registry.llms`, v1 `llmProviders`) and a connection to the mock URL with a placeholder key, and switches the broker to the first model of the mock. No Exchange dependency is added, and Problems doesn't ask for one.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Six fully mocked templates and their tutorials**. New Project has six use cases whose LLM is an A²D LLM mock too, so they deploy and answer without an OpenAI key: *Hotel Concierge*, *Library Services* and *Fleet Maintenance* (probabilistic), *Event Ticketing*, *Warranty Repair* and *Utility Outage* (deterministic). Each has its own scripted LLM mock (`a2dLlm.url`, placeholder key `a2d-mock-key`) next to new A²D agent and MCP mocks, so the same prompt gives the same reply every time. Every Try it prompt was deployed and checked in the chat against its *You should see*. Each template has a tutorial; *Build it from scratch* drops the LLM mock from the palette's A²D LLMs filter.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Credits in the CHANGELOG, release notes, issues and PRs**. Every entry names the issue's reporter, the code owner (PR author) and the committers equally, as profile links, so nobody gets a notification. `node .github/credits.mjs <issue> [pr | git-range]` prints the line, a test checks the newest section, and the skills and the PR template ask for it.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Octoloom standards check on every issue**. CI posts an *Octoloom standards check* comment on every new or edited issue. It lists where the request touches a frozen UI surface, several UI modules, the UI framework or theme, hidden or locked project files, LLM cost, credentials or org changes, and asks the agent to rate it in 8 categories in the issue (skill `octoloom-standards-review`, labels `standards/*`). The skill also says what *great project files* are: true to the reference, maintainable, cheap for customers, repeatable and explained.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Coverage map**. A **Coverage map** link in Home → *Your statistics* (and **Octoloom: Coverage Map**) opens one tab with every agent network on this machine: summary cards (policy coverage, protected brokers, upstream auth, governance, real services vs A²D mocks, deployed), a flow chart of where agents, MCP servers, LLMs, policies and rulesets come from (A²D, Agent Fabric, Informatica IDMC, P4A, your organization), a table with seven views and the details of each network with its gaps. Governance runs now also keep a small summary per project, and P4A policies are recorded when applied, so the map can show them. Read-only and local.

    <span class="ol-by">:material-account-heart-outline: [Burak Tas](https://github.com/burak-tas), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.26

<span class="ol-ver-meta">2026-11-19 · released</span>

- **Docs: tutorials linked from the Marketplace page**. The top navigation, Highlights and *Getting started* link the [tutorials](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/blob/main/tutorials/README.md).

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: connection keys over 51 characters**. The CLI names the gateway context `<key>-api-context` (63 characters at most); the local gateway of Run locally rejects a longer name. Run locally now stops before the CLI and offers **Rename and run** (key and references). Deploys to a managed gateway accept the key (a 52-character key deploys and runs), so Build, Publish and Deploy only write a warning and go on. New Project caps the id prefix.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: CLI login clash**. When the connected app is passed, `ANYPOINT_USERNAME` / `ANYPOINT_PASSWORD` from the environment are dropped for the CLI run, and the error explains the clash.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: stale local run**. A leftover `build-status.json` without a running terminal no longer shows *Starting locally*.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: dangling `@kind.name` references**. References in a broker flow to nodes that don't exist are reported in Problems, before the CLI fails with *undefined reference*.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **One CLI run per project**. While a build, publish, deploy, local run or gateway setup is running, its icon shows a spinner and the project's other action icons are disabled; a second run is refused with a message.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Error details**. Failed calls keep the HTTP status, the server's answer, the network cause and the URL; the asset palette error has an info button with them.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Broker flow file on delete, flow minimum**. Removing a broker offers to move its `.agent` file to the Trash. A flow needs a trigger, an agent node (generator, subagent or orchestrator) and an echo node; Problems reports what is missing.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Run locally: variables, internal hosts**. The local form has inputs for the non-secret `exchange.json` variables, preloaded with their `exchange.json` values; changed values are passed as `--property` for this machine only (`exchange.json` is not changed). A default URL with an internal host name is marked, and Run locally asks before it starts.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **No more Forget deployment**. It hid running deployments; the status refresh shows the real state.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Remove from workspace**. A project action that takes the project off the list or closes its workspace folder. Files stay on disk and in Git; *Show Removed Projects* brings it back, and so does a download from Exchange, a new project in the same folder or *Add Folder to Workspace*. Governance lists the same projects as Projects & Deploy. Remove closes the project's open tabs without a save prompt (unsaved changes are discarded).

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Canvas tool stack tooltips**. Hovering + Add, Asset Palette, Auto layout or Minimize all on the network canvas shows its name next to the button (VS Code shows no native tooltip there).

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Docs: dashed icon tile**. The README and Explain (LLM provider, canvas, LLMs from Exchange) say what the dashed tile means: an asset referenced from Exchange, not declared in the project.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **v2 Context card connected**. The Context card (policies and connections without an owner) sits left of the brokers and connects to each broker's new orange **Context** row instead of floating unconnected.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Protected broker settings**. A v2 broker's Kind and Implementation are behind the same lock as the protected part of `exchange.json`.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Theme hint**. Setup & Connect → Appearance says when the forced color mode doesn't match VS Code, with **Follow VS Code**.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Explain per button**. Every toolbar and project button has its own Explain card; the Publish card explains versioning (the `exchange.json` version is used as it is, a published version can't be published again). An **(i)** in the *Projects & Deploy* title bar, after **+** and Home, turns on Explain mode for the side bar.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Governance in the project header.** The shield moved from the action row to the project card's header, right after the version, so the row has one icon less.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Tutorials: Build it from scratch**. Home and the README mention the third path of every tutorial.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.25

<span class="ol-ver-meta">2026-11-17 · released</span>

- **Pre-deploy: duplicated connection names.** a v1 connection key that another project in the environment already uses for the same Exchange asset (typically a shared Exchange LLM, `demo-llm-connection`) is reported before publishing, instead of the late "Duplicated connection name" deploy error. Fix and deploy renames it to `<project>-<key>` with the broker refs.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Tutorials.** A new **Tutorials** section on Home links to *Getting started* and to one tutorial for each of the 37 templates in [octoloom-assets/tutorials](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/blob/main/tutorials/README.md). Each tutorial has two paths: **Just use it** (create from the template, deploy, chat) and **Learn step by step** (the canvas, the AgentScript flow, policies and secured connections, validate and build, deploy with its secrets, chat with every Try it prompt and what you should see, and the Tracer), with screenshots.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **UI conformance checks, pack 2**. New findings on the Problems bar and in VS Code Problems, each with a Fix where one is safe:
    - **AgentScript:** sections, blocks, transitions, actions and variables are checked against the reference; LLM settings (temperature, top_p, provider-only options, thinking budget, key names) are checked per provider.
    - **Network:** agent cards, connection authentication, TLS and the TTL limit.
    - **Builder:** a click on a problem jumps to the exact field; the flow coach wires open paths to the final reply; a delete also removes its flow actions and unused variables, with one Undo and one summary toast.
    - **Chat:** the card's per-transport endpoint is used when the base URL has none, and `${ingressgw.url}` in a published card is replaced before sending.
    - **Versions:** the next version suggested is above the latest one in Exchange.
    - **Explain:** deploy and publish errors (403, 2007, 3025, hard delete, hanging deploys, policies, a broker's services must be deployed) explain what to do.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Headless IDMC**. Connect to Informatica IDMC in Setup & Connect and browse its shared and composite MCP servers in the new **IDMC** tab of the asset palette (tabs: A²D, Agent Fabric, IDMC). An added server gets its connection with `IDS-SESSION-ID` authentication from a secret variable. Canvas cards show an Informatica badge, and the Welcome page counts IDMC MCP servers and governed assets.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: Informatica MCP servers answered 405**. Connections use the full server URL with `/mcp`; a host-only URL is a warning. An MCP `metadata.platform` must be lower case, as Exchange requires.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **IDMC templates**. **IDMC Customer Data Steward** (v1) and **IDMC Data Trust** (v2), each with a README on what IDMC must provide, setup and deploy. Bundled templates stay in New Project when the remote catalog loads.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Validate Project**. A dry run of build, publish and deploy on a copy, from the canvas menu, the project card, the Explorer and the command palette. Nothing in the project or the organization changes.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **exchange.json checks**. A `${organizationId}` group is an error with Fix and is filled at build; a missing `groupId`, `assetId` or `version` is an error in Problems.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: Fix and deploy used the old names**. The deploy now uses the renamed keys.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: New Project's canvas didn't open in an empty window**. It opens after the extension host restart.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: template brokers timed out in the chat**. With gpt-5-mini's default reasoning effort, a broker step took about 26 seconds, longer than a gateway with a short upstream timeout allows. All templates now set the reasoning effort to `MINIMAL`. Campaign Studio calls each tool once and allows 12 loops. KYC Onboarding opens the account once the checks pass or the analyst approves. The v1 IDMC Customer Data Steward README explains that the v1 runtime can't send `verify_address` its nested request, and points to the v2 IDMC Data Trust template.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Side bar hover tips; one *None* in the v2 authentication kinds; the AgentScript `variables` section is known**.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Contributor rules: no UI change without the maintainer's go**. The skills, `AGENTS.md` and the gate tests now also freeze the broker and network canvases, the asset palette, the exchange.json form, Validate / Build / Publish / Deploy and the chat module. Regression checks compare against the tested 0.9.25 build only.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **LLMs from Exchange as dependencies**. The Agent Fabric tab of the asset palette has an **LLMs** filter. Dropping a published LLM on a broker adds an `llm-metadata` dependency in exchange.json, an LLM connection with a URL variable and a secret `apiKey` variable, and makes it the broker's LLM. The LLM is referenced, never copied, so a publish creates no new LLM asset. New Deterministic (v2) projects and the v2 templates reference MuleSoft `openai`. A v2 project-declared LLM is reported in Problems, and for OpenAI its Fix switches to MuleSoft `openai`. The broker inspector lists referenced LLMs ("Exchange asset · v1.0.0") to replace them, and **Remove LLM from broker** or the LLM card's trash removes one in one undoable edit. LLMs with an input format work in v2 only; the v1 build rejects them (error 3061).

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Installed version and update notice**. Welcome shows the installed Octoloom version under the title, and Setup & Connect → Tooling has an Octoloom row. When the Marketplace has a newer version, both say so and open the extension in the Extensions view.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Asset palette: LLMs only on the Agent Fabric tab.** A²D and IDMC have MCP servers and agents only, so their tabs show the All / MCP / Agents filter without LLMs.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Share a broker from the chat.** One Share icon in the broker chat header, after New conversation, opens the Share dialog on its A²D sessions tab; sharing is no longer in Projects & Deploy and the labelled header buttons are gone. **Local portal** generates a standalone web chat for a broker, so colleagues can chat with it without VS Code, Octoloom or a Slack or Teams app: a Node server with no dependencies, the chat page, a Dockerfile and a README with deploy steps for Docker, Render, Fly.io, Cloud Run and Azure App Service. Visitors sign in with a shared passcode that Octoloom shows once; only its hash is stored. The server calls the broker over A2A with the credentials method saved in the chat and keeps the secret out of the browser. Several portals per project, each with its own folder, passcode and port; self-checks (`node server.mjs --check`, a Status panel), a version stamp with Update, Delete to the Trash and port checks. **A²D sessions** share a deployed broker as an A²D exploratory session of the new **Octoloom chat** type: invited people verify themselves on an Octoloom-styled page and chat in the Octoloom chat window hosted by A²D. The session always expires (1 to 90 days); its row opens, copies, invites, extends, ends or removes it. Opened, it shows the results stored in A²D (invites, passed / failed / in-progress marks with comments, submits and conversations, refreshed every minute; new marks are flagged), and **Continue in the chat** loads a visitor's conversation into the Octoloom chat with the same context. An older A²D falls back to its tester and the invite status. With an A²D that takes Octoloom chat sessions, the broker's Client ID is sent as its client_id / client_secret headers, and custom API key headers and OAuth2 client credentials work too (A²D gets and refreshes the token). Create, End and Remove are confirmed inside the Share dialog (a review step and an inline strip with icon buttons), not in a system message box.

    <span class="ol-by">:material-account-heart-outline: [Burak Tas](https://github.com/burak-tas), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.24

<span class="ol-ver-meta">2026-11-15 · released</span>

- **Meet the Octoloomies: Shad Iman, Executive Loomie**, and refreshed Marketplace screenshots.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Contributor rules: the UI is frozen**. This is a docs and tests change only: nothing in the extension changes. The new skill `octoloom-ui-frozen-surfaces` and the new `AGENTS.md` cover the chat module (Network/Traces, Chat Window, Agent Network Tracer), every canvas, publish/deploy and the Explain button. On these surfaces, every coding agent must keep the framework, functionality, user experience, components, positioning, styles, movements, stickiness and flexibility as they are. Only invisible work such as background processes, caching and data retrieval is open to change. The new gate test `test/frozenSurfaces.test.ts` fails if a frozen persistence key or control is removed.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Agent Network View in the chat**. The chat's **Network** tab now draws the whole network read-only, like the network canvas: every broker, agent, MCP server, LLM, connection and policy. You can drag, minimize and collapse cards, and the layout is kept per project. Click a broker to chat with it. After you pick a reply, the tab shows it as a **sequence diagram**: You, the broker, and each agent, MCP server and LLM it called, with a request arrow and a response arrow per call, numbered (1), (2), … in time order. Click an arrow for its span facts and the log lines with the request and the response. The network and the sequence fit their section, refit when it is resized, and have a zoom bar. A **full screen** button in the left header gives the whole panel to the network, the sequence or the trace. It uses the same trace lookup as the Trace waterfall, so nothing new is called in the organization. The sequence and the waterfall share the loaded trace while the chat is open, so switching between Network and Trace is instant. The refresh button loads it again, and a trace with no spans yet is always loaded again. The Trace waterfall, the Agent Network Tracer and the Governance canvas are unchanged.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: v1 brokers showed no trace spans**. Mule broker logs carry no trace id, so the chat Trace view and the Agent Network Tracer said there were no spans. Octoloom now finds the trace by time: the `[BROKER] <broker>` span in Observability that covers the task's log lines. It is marked *matched by time*. v2 brokers still match by trace id.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: long deploys were cut in the terminal, and v1 deploys stopped to ask for `ingressgw.url`**. On macOS and Linux the deploy command is now written to a private script and only `sh '<script>'` is typed, so a deploy with many properties is no longer cut at the terminal's 1,024-byte buffer. For v1 networks Octoloom fills `ingressgw.url` with the base URL of the gateway picked in the Deploy form, so the CLI no longer stops to ask. New gate tests (`deployProps`, `deployRoutes`) cover every bundled v1 and v2 template and the sidebar and canvas routes, and the deploy skill makes them mandatory.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: cards could not be dragged by the icon tile or chevron, and clicks on them did nothing**. On every canvas a card now drags from anywhere (header, icon tile, chevron, body) whether it is open, collapsed or minimized, and in a canvas that mixes all three. A click on the icon tile minimizes or opens only that card, and a click on the chevron collapses or expands only that card. New gate test `test/canvasStates.test.ts`, and the canvas skills now make these behaviours mandatory.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix: a new project didn't show in Projects & Deploy**. After **New Project** created a project inside the workspace, or with *Add to this workspace and open the canvas*, the Projects & Deploy list only showed it after a save, Refresh or reload. The list now updates straight away, and also whenever a folder is added to or removed from the workspace. *Only open the canvas* outside the workspace still doesn't list it.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock)</span>

- **Code view: YAML values have colour**. In `agent-network.yaml` the values after a key (`label: Retail Returns`, list items such as `- text/plain`) were shown in the plain text colour; only quoted strings, keys and comments had colour. Plain values now get the string colour, and `:` and list `-` the operator colour, as in the AgentScript view. Key colours are unchanged.

    <span class="ol-by">:material-account-heart-outline: [Tommaso Bolis](https://github.com/tommasobolis), [George Jeffcock](https://github.com/jeffcock), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.23

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Fix: Deploy from the canvas asked for a gateway that doesn't exist**. *Deploy…* on the canvas, the command palette, the editor title and the Explorer used a chain of prompts with `agent-network-gw` (the CLI's example name) filled in, so pressing Enter failed with *Gateway with name 'agent-network-gw' not found* (4006). They now open the project's **Deploy form** in Projects & Deploy, the same form as the rocket on the project card: gateway chips from the connected environment, secrets, the Tracing / Wait / Publish switches and deployment properties, with the same saved values.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Deploy into a private space**. *Target space* lists the organization's private spaces (marked *private*) and the CloudHub shared spaces as chips (read-only, Runtime Manager). Each gateway chip says which space it runs in; with a single gateway the brokers deploy to that space. In *Ingress / egress* mode picking the ingress gateway fills in its space, so the CLI no longer falls back to `agent-network-space`.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Trace legend with your own colours**. The chat trace now has a legend above the waterfall that says what each colour is: Broker, Agent, LLM, MCP, Router, Other and Error, only for the kinds in that trace. Click a name to choose your own colour for it, and **Reset colours** goes back to the defaults. The default colours are unchanged. Your colours are saved on this machine only (not synced, not in the project).

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.22

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Fix: the broker chat disappeared in a narrow chat tab**. Below 760px the chat stacks the network on top of the conversation, but the conversation landed in a 0px row and the space under the network stayed empty, also with the Agent Network Tracer open. The chat now shows under the network again, and *Chat full height* / *Trace full height* use the whole height at that width.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.21

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Fix: Publish, Deploy and Build fail with "No authentication mechanism was provided"**. Every one of them builds the project first, and anypoint-cli-v4's build logs in to Anypoint too, but Octoloom ran it without credentials. It only worked when the CLI had its own `anypoint-cli-v4 conf client_id / client_secret`. The build now gets the connected app from Setup & Connect, like publish and deploy (through the process environment, never on the command line). When the CLI still gets no credentials, the error says so and offers **Connect**.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.20

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Fix: Setup & Connect shows what to do first**. In a short side bar Projects & Deploy took the height, so only *Appearance* showed and users missed Connections and Tooling. The sections are now Connections, Tooling, Appearance. The line on top says what is left, for example *2 of 3 connected · tools ready*. The view also asks VS Code for more height when it opens.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.19

<span class="ol-ver-meta">released</span>

- **Publish and deploy into a sub business group**. Octoloom always used the connected app's own organization (usually the root), so a sub business group such as *Arnado Air Group* couldn't be targeted. When the connected app can see more than one business group, Connect now asks which one to use, root first and sub groups indented. Change it later with the new branch button next to the environment globe on the Agent Fabric card, or with **Octoloom: Select Agent Fabric Business Group**. Switching the group picks the environment again, because environments belong to a group. The chosen group drives environments, gateways, Exchange search, `--organization` on publish and deploy, and the `groupId` of new projects. A new pre-deploy warning tells you when a project's `exchange.json` `groupId` is not the selected group. The connected app needs scopes in the sub group, otherwise Anypoint lists only the root organization.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.18

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Fix: Agent network from Exchange can scroll**. An org with many agent networks filled the dialog, and the page couldn't scroll, so *Save to* was out of reach. The view now scrolls like New Project. The network list has its own scroll area, so step 2 and the footer stay in view, and long asset ids and footer text no longer overflow.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.17

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Find / replace in the code view looks like VS Code's**. It was CodeMirror's default bar at the bottom: white inputs, grey text buttons and native checkboxes. Now a find box floats at the top right, like VS Code's: a chevron shows the replace row, and the find input has **Aa** (match case), **ab** (whole word) and **.\*** (regex) toggles inside. Next to it are the **N of M** count (red *No results*), previous / next, select all and close, and the replace row has Replace and Replace All. Keys: <kbd>Ctrl/Cmd</kbd>+<kbd>F</kbd> find, <kbd>Ctrl/Cmd</kbd>+<kbd>H</kbd> replace, <kbd>Enter</kbd> / <kbd>Shift</kbd>+<kbd>Enter</kbd> next / previous, <kbd>Alt</kbd>+<kbd>C</kbd>/<kbd>W</kbd>/<kbd>R</kbd> toggles, <kbd>Esc</kbd> close. The colours are VS Code's (find widget, input, input option, match highlights). The UI framework is unchanged: CodeMirror's own panel hook, no new library.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.16

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Download an agent network from Exchange**. The Projects side bar has an Exchange icon after **+**, and the new-project menu has a **From Exchange** card. Both open a dialog that lists only the *Agent Network* assets of your organization (or all you can see), with search and a version picker (newest first). Octoloom downloads the version's project zip (v2 `agentic-network`, v1 `agent-network` or legacy `broker-group`), unpacks it with size limits and path checks into a new folder of your workspace (never overwritten: `-2`, `-3`, …) and opens it on the canvas. Nothing changes in Exchange. When Exchange stripped `exchange.json` (variables, `descriptorVersion`, seen on v1 networks), Octoloom puts them back, so the project builds and governance checks it like the original. A note tells you when the version is already published and needs a bump before the next Publish.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock)</span>


## 0.9.15

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Open the broker in Exchange to request access**. Each deployed broker row, and the chat's *Authentication* header, has an Exchange icon (key) that opens the broker's asset page in Exchange. There, **Request access** gives you the client ID and secret for brokers behind Client ID Enforcement. No more searching for the broker in Exchange.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.14

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Blue light for brokers behind authentication**. A deployed broker whose gateway asks for credentials (HTTP 401/403, e.g. Client ID Enforcement) was shown red as *Deployed, not answering (stopped)*. It now shows blue: **Deployed, needs credentials**. Each protected broker row gets a shield chip: **saved** (green, with the method) when the credentials saved in the chat work, otherwise **needed**, **refused** or **sign in**; click it to open the chat. Saving, clearing or signing in in the chat checks the deployment again at once, so the light turns green. The status check still never signs in by itself.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.13

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Collapse and expand policies**. In the *Policies* section of the inspector each policy has a chevron that collapses it to its title row (binding name, direction, policy asset, number of settings). With two or more policies they start collapsed; **Collapse all** / **Expand all** sits in the section header. Your choice is remembered per policy. The YAML is not changed.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.12

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Deploy form with on/off switches and a gateway picker**. The checkboxes in the Deploy and Run locally forms are now switches in Octoloom's colours, one per row: **Tracing**, **Wait until the network is ready**, **Publish before deploy** (on by default, off passes `--disable-tracing`, `--dont-wait-for-agent-network`, `--disable-autopublish`) and **Watch files**. Your saved choices carry over. Under each gateway field, the gateways of the connected environment are listed as chips with a status dot; click one to fill it in, or type a name as before.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.11

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Template READMEs you can deploy and try right away**. Every one of the 35 templates now has **Deploy in 3 steps** (connect, the variables to fill in such as `ingressgw.url`, and each secret you are asked for at deploy, such as `openai.apiKey` and the passwords and client secrets of secured variants) and **Try it**: 3 to 6 prompts per template covering the main path and the other branches, plus PII and rate-limit prompts for governed variants, each with **You should see** (the agents, tools and mock ids in the reply and the Agent Network Tracer). The New Project preview shows bold text and nested items. The networks, flows and mocks did not change.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.10

<span class="ol-ver-meta">2026-11-13 · released</span>

- **All MuleSoft gateway policies in the policy picker**. The Agent Fabric tab now lists every MuleSoft-provided policy that Anypoint offers on an Agent Fabric instance (about 120, up from 12), including *Basic Authentication - Simple* and *LDAP*, *Client ID Enforcement*, *IP Allowlist / Blocklist*, *CORS*, *Spike Control* and *Credential Injection*, with their schema defaults. The list is bundled (works offline); when connected, newer MuleSoft policies from Exchange are added. Mule 4-only templates, GraphQL / WebSocket / WSDL-only policies and the ones the CLI adds itself are left out.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.9

<span class="ol-ver-meta">2026-11-13 · released</span>

- **The policy picker lists every policy for every component**. On a broker, agent, MCP server or LLM the picker no longer hides policies such as *Basic Authentication*. A new **All components / Only for <component type>** toggle lets you narrow the list yourself. The "Show N more for other component types" link and the dimmed entries are gone.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.8

<span class="ol-ver-meta">2026-11-13 · released</span>

- **The floating Explain button keeps one place across tabs**. Drag it in one editor or panel and every other open Octoloom tab moves its button there too, so switching tabs feels like one button. The place is kept after a restart; double-click resets it everywhere. (In a split view each editor group still shows its own copy, at the same place.)

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.7

<span class="ol-ver-meta">2026-11-13 · released</span>

- **One floating Explain button per window**. The side bar views (Setup & Connect, Projects & Deploy, Asset Palette) no longer draw their own, so only the editor's button is shown.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.6

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Only the floating Explain button**. The fixed Explain buttons and panels are removed from the network canvas and broker flow toolbars, Governance, chat authentication and the Agent Network Tracer; the floating info button explains all of them.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **The floating button starts the guide.** On the network canvas and the broker flow, Explain mode offers **Start the guide** (and a button to show the guides again automatically); the toolbar Guide menu is gone. Each tour now ends on the floating button.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Larger, dark blue floating button** (48 px, white icon) in both themes.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Agent Network Tracer:** Full height is icon-only (a toggle, `aria-pressed`) and its Explain button is gone.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Tests:** the Tracer UI smoke test (`test/ui/tracer-smoke.mjs`) checks the chat's Trace view opened by a task instead of the network box, and drops the removed Explain case: all 12 cases pass again.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.5

<span class="ol-ver-meta">2026-11-13 · released</span>

- **Explain anything**. A floating, movable info button on every Octoloom view (bottom right, above the minimap). Turn it on, then click any card, panel, tool or canvas: the click does not act, and a card beside the object explains what it is, when to use it and examples, with the object's name. Hover outlines what will be explained; Esc closes the card, then the mode. Drag the button to move it (kept per view); double-click to reset. New explanations for the chat, chat network, projects, assets, canvases, the `exchange.json` editor, New project, code view, problems, inspector, canvas tools, flow outline and toolbar.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.4

<span class="ol-ver-meta">in development</span>

- **Collapse every part of the chat**. The left side (network or trace) and the chat window fold to a thin rail with their icon and name: the chevron at the left of the network bar, or at the end of the chat header. Click the rail to expand. The Agent Network Tracer already collapses to its header. The choice is kept; full height still wins, and opening a trace expands a folded left side.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.3

<span class="ol-ver-meta">in development</span>

- **Traces tab removed** from the Tracer's detail column: the same spans, as a waterfall with span details, are in the chat's Trace view, which opening a task now drives.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.2

<span class="ol-ver-meta">released</span>

- **The Tracer's task list drives the chat's Trace view**. Opening a task in the Agent Network Tracer's **Tasks** list also shows its span waterfall on the left of the chat (Network | Trace switches to Trace), as the trace icon under a reply does. Error-only rows are not traced.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Tracer header:** **Full height** and **Explain** moved to the right end of the header, after the environment and the access pill.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.1

<span class="ol-ver-meta">released</span>

- **Agent Network Tracer graph: icon-only Minimize all / Open all**. The button keeps no text and uses workflow icons: one node branching to two (Minimize all), two linked cards (Open all, pressed). Its tooltip names the action; it is still a toggle (`aria-pressed`).

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.9.0

<span class="ol-ver-meta">released</span>

Versioning: minor releases are 0.9.x from now on, until 1.0.0.

- **Trace of a chat reply**. Each deployed reply has a new **trace** icon (pulse line, no text). It shows that reply's distributed trace on the left of the chat as a waterfall: one row per span (gateway request, broker, LLM calls, A2A calls, MCP tool calls), nested by parent span id, on a shared time axis, coloured with the canvas hues, errors in red. Click a span for its kind, entity, status, duration, start offset and ids. **Network | Trace** above the left column switches back. A **full height** icon in the trace header gives the whole panel to the waterfall. Young replies are checked again by themselves while spans arrive (about 20 s). Read-only: it reuses the Tracer's task lookup. The Agent Network Tracer is unchanged.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Icons instead of text under a reply.** The **Trace** link under a deployed reply is now the **Tracer** icon (same action: open the task in the Agent Network Tracer).

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Exact span tree.** The span search now also reads `parent_span_id`. The Tracer's Traces tab and the chat waterfall nest spans by parent id and fall back to timing only when a parent is missing. Up to 2000 spans per trace (was 500).

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- New Explain entry `chatTrace`, screenshot specs `chat-trace` and `chat-trace-full`.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Agent Network Tracer: Minimize all / Open all**. A toggle at the top left of the Tracer graph turns every node into its icon tile, as on the flow canvas, so long flows fit. The path taken stays highlighted (hop numbers, accent ring on taken tiles). The choice is kept per broker file. New screenshot spec `tracer-mini`.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Marketplace links**. The public assets repo moved to `A2D-Agentic-Asset-Designer/octoloom-assets`: README images, repository, issues and the template catalog now point there. The Marketplace **Homepage** link opens *Meet the Octoloomies*.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.7.1

<span class="ol-ver-meta">released</span>

- **Pre-develop UX fixes**:
    - **Agent Network Tracer finds brokers in large environments.** API Manager returns at most 100 assets per page. The Tracer read only the first page, so a broker on a later page showed "No API Manager instance found" and "broker context: not found". It now reads every page. The same fix applies to the Projects & Deploy detection and the pre-deploy checks.
    - **Runtime logs and Object Store found.** The broker's Runtime Manager deployment is now found through the host in its upstream URL. Before, "The broker deployment was not found" appeared when the deployment name differed from the broker key.
    - **Elastic top bars.** On every canvas (network, broker flow, `exchange.json`), button labels hide before the top bar would wrap and come back when there is room. Icons and tooltips stay.
    - **Chat full height.** A new icon button in the chat header gives the whole panel to the conversation.
    - **The side bar stays on Octoloom** after opening a file from Projects & Deploy, even when another extension switches it to the Explorer.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Chat authentication**. The broker chat now works with brokers behind authentication. The shield button in the chat header sets credentials per broker (deployed or local): a bearer token, user sign-in (OAuth 2.0 authorization code + PKCE in the browser, with token refresh), client credentials, the OAuth 2.0 password grant, client ID headers, an API key header or Basic. The broker's inbound policies preselect a method. A 401 or 403 reply links to the settings. Secrets and tokens stay in VS Code Secret Storage, and the project status uses them to read the card of a protected broker.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock)</span>

- **Agent Network Tracer**. See what a deployed broker did for each task, inside the broker chat panel. Open it with the new **Tracer** button on a *Deployed and running* box, or **Trace** under a deployed chat reply. It has three columns: Read-only: it reads Log Search, runtime logs, Object Store task state and Observability spans with the Agent Fabric connected app. An access check names missing permissions and offers the Anypoint Code Builder sign-in instead. **JSON** exports a whole task (`octoloom.tracer.task/v1`, or NDJSON) for Splunk or Datadog, with credentials masked. New settings `agentNetwork.tracer.debugLog` and `agentNetwork.tracer.debugLogFile`, a new Explain entry and a new screenshot spec `tracer`.
    - **Tasks:** the broker's tasks in a period.
    - **Task:** Graph, Tree or List. The Graph is the broker's `.agent` flow with the path taken.
    - **Detail:** Status, Story, Message, Metadata, Traces, Log, Raw and JSON.

    <span class="ol-by">:material-account-heart-outline: [George Jeffcock](https://github.com/jeffcock)</span>


## 0.7.0

<span class="ol-ver-meta">2026-11-12 · released</span>

- **Octoloomies logo**. The Octoloom octopus logo now sits before the Meet the Octoloomies heading on the Marketplace page. No change to the extension's behaviour.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Portable tests**. The unit tests no longer read projects from a developer's own folders. They use the bundled fake-data templates, so they pass on every machine and in CI, and a guard test keeps it that way.

    <span class="ol-by">:material-account-heart-outline: [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.9

<span class="ol-ver-meta">2026-11-12 · released</span>

- **Branch guards**. New CI checks: PRs into develop must come from a `<type>/N-slug` work branch. A direct push to develop or main fails a check and opens an alert issue. Only develop may be PR'd into main. No change to the extension's behaviour.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Meet the Octoloomies**. A team section with photos, LinkedIn links and roles on the Marketplace page, plus quick links at the top of the page.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.8

<span class="ol-ver-meta">2026-11-12 · released</span>

- **Contributor skills**. A new golden rule: no feature is good enough if it breaks the UX. New skills for the canvas, component sizing (minimize / open, collapse / expand), templates, guides and Explain, deploy and publish, and governance and rulesets. No change to the extension's behaviour.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.7

<span class="ol-ver-meta">2026-11-12 · released</span>

- **Welcome page**. When VS Code starts, Octoloom opens a Welcome page; it doesn't open when you click the Octoloom icon later. You can open it again with the home button in Projects & Deploy or **Octoloom: Welcome**. It has three parts: Statistics are kept in global state on this machine. Successful builds, deploys and publishes are counted. Projects built earlier are picked up from `target/`. New setting `agentNetwork.showWelcome`, a new Explain entry and a new screenshot spec `welcome`.
    - **Start:** Probabilistic and Deterministic network cards that open New Project with that style.
    - **Recently built:** the 5 agent network projects built last on this machine.
    - **Your statistics:** local stat cards for workspaces, network projects and the Probabilistic / Deterministic ratio, brokers, agents, MCP servers, Exchange and A²D assets (A2A + MCP), policies in networks, deployments, publishes and the top 3 LLM providers.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Templates live test**. All 33 templates build and 29 of them deployed to a live org. The test found no template bugs. Some chat tests failed because the org's gateway was down (502).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.6

<span class="ol-ver-meta">2026-11-12 · released</span>

- **More templates**. There are now 35 New Project examples. The five new use cases are HR leave and patient intake (v1), and supply chain disruption, KYC / AML onboarding and IT incident response (v2). Each comes plain and governed. A new **secured** technical variant authenticates every agent and MCP connection (Basic or Client ID enforcement, alternating). User names and client ids are variables, and passwords and client secrets are secret variables with no default. The LLM URL is the variable `llmGateway.url`. The broker is rate limited, and v2 upstream calls are logged with outbound Message Logging. All upstreams are new public A²D mocks. The Technical tab subtitle mentions secured connections.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Component and instruction templates**. New flow patterns: Error handling, Retry once then fail, Human in the loop (ask for details) and Guardrail check (rejected), plus a Rejected reply. New instruction templates: Error handling, Retry, Ask the user when details are missing, and Guardrail screen. All of them are checked with the agent-network CLI build. The CLI requires every path to end in a terminal state, so human-in-the-loop replies complete with a question instead of pausing with input required. Explain: new Patterns entry, and the Reply entry is updated. Sub-menus now stay inside the window.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Screenshot harness: `@json:` references and new specs `new-project` and `agent-patterns`.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.5

<span class="ol-ver-meta">2026-11-12 · released</span>

- **Pre-deploy checks**. Build stops when a v2 broker's `implementation` file does not exist (and says when the file is in the project root instead). Before deploy, when Agent Fabric is connected, Octoloom checks the org for what the CLI only reports after publishing: an `exchange.json` dependency the org can't read, a registry key that is already an Exchange asset of another project, and a connection key that is already an API instance in the environment. Findings go to the *Agent Network CLI* output with a fix; deploy asks *Deploy anyway* or *Cancel*. Your own earlier deploys are not flagged, and a failed lookup never blocks. New Explain entry (tooltip on the Deploy button).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.4

<span class="ol-ver-meta">2026-11-12 · released</span>

- **Fix: MCP connection URLs.** The Agent Fabric runtime always adds the MCP server's `metadata.transport.path` (for example `/mcp`) to the connection URL, so a URL that already ends with `/mcp` makes the broker call `…/mcp/mcp` and find no tools. The Problems panel and the code view now warn about such a URL (resolved from the `exchange.json` defaults). Test connection calls exactly the URL the runtime calls, so it no longer passes on a URL that fails after deploy. The MCP connection template's example URL is now the server base (`https://example.com/`). Explain updated.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.3

<span class="ol-ver-meta">2026-11-12 · released</span>

- **Fix: Fix all on governance** no longer ends with "N findings are still reported after the fix". The P4A MCP tool rules (tool hints, closed input, output schema) are written for MCP server specs, and the governance CLI reports them for every tool in `agent-network.yaml`, whatever it declares, so their fixes can never clear a finding. Fix all now applies only the fixes the ruleset confirms (its count is what it clears). Those MCP tool findings keep a secondary Fix with a note, and the warning appears only for unexpected findings. Explain and README updated; new screenshot spec `governance-fix-all`.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.2

<span class="ol-ver-meta">2026-11-12 · released</span>

- **Setup & Connect** (new side bar view, first in the Octoloom side bar): Appearance (theme), Connections (Agent Fabric, A²D, P4A) and Tooling (Node.js, Java, anypoint-cli-v4, agent-network plugin, Install missing tools) moved here from Projects & Deploy. The order is now Setup & Connect, Projects & Deploy, Asset Palette. Setup & Connect starts collapsed and opens by itself only when no folder is open or the workspace has no projects yet. It has its own Explain entry.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Docs: the A²D API key is created in **A2D > Settings > Organization Settings > API Keys** (README, the Connect to A²D prompt and the 401 error).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.1

<span class="ol-ver-meta">released</span>

- **Fix: v1 `agent-network.yaml` opens the Octoloom canvas again** when Anypoint Code Builder is installed. ACB closed the Octoloom canvas and opened its own canvas plus the YAML text for v1 (probabilistic) networks. Clicking the file on a project card, in the explorer or from a link now keeps the Octoloom canvas. Only tabs that ACB opens in the first seconds are closed; *Open as text*, *Reopen Editor With…* and tabs you already had open are left alone. New setting `agentNetwork.keepOctoloomCanvas` (default on) turns this off.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.6.0

<span class="ol-ver-meta">2026-11-12 · released</span>

- **Governance, layout**: the Rulesets and Conformance columns can be resized (drag the splitter) and hidden (chevron in the column header; show them again from the canvas header). Widths and visibility are kept per panel.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Governance, Anypoint-style conformance** in the IDE: a Design time card, "N issues from M rules", one expandable row per rule (scope chip, ruleset, severity pill) or per component, severity filter, Expand / Collapse all. New center tabs: **Governed services** (conformance and identified issues cards, services table) and **Configuration** (scope card and expandable rulesets with a "Rule Name & Description | Severity" table). The workspace report starts with a summary of every project.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Fix / Fix all**: findings that can be fixed without guessing your data get a Fix button. The fix writes only keys from the v1 / v2 agent network reference: card capabilities, protocolVersion, name, description, URL / supportedInterfaces, v2 broker `interfaces.a2a.authorization.allowAnonymousAccess: false`, streamableHttp transport, allowed tools, tool annotations / closed input / output schema, and inline secrets moved to secret exchange.json variables. The change goes through the editor (Undo with Ctrl/Cmd+Z), the file is saved and the project is validated again. Inferred values are marked "review". Findings that need a decision (which policy, provider or URL) keep the copyable suggestion. A finding the ruleset still reports after its fix is marked, and its fix is not offered again.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **HTML report** redesigned in the Anypoint API Governance style: header with conformance chip, Governed Services / Configuration tabs, conformance and identified issues cards, services table, per-service sections with expandable rules and findings, and a Configuration tab with the rulesets and their rules. No scripts; prints with every section open.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Network reference: tool `annotations` (title, readOnlyHint, destructiveHint, idempotentHint, openWorldHint) and v2 broker `interfaces.a2a.authorization` (principal, allowAnonymousAccess) are known to the code view and the checks.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Known limitation: with governance plugin 1.1.3, P4A MCP server rulesets may keep reporting tool findings for MCP servers declared in agent-network.yaml after the fix (they read MCP server specs).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- README and Marketplace screenshots updated for the new governance views and report.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.5.0

<span class="ol-ver-meta">2026-11-11 · released</span>

- **Governance** (new): validate a project against rulesets with `anypoint-cli-v4 governance api validate`.
    - Ruleset sources: **Agent Fabric** (MuleSoft), **P4A** community rulesets and your own P4A rulesets (P4A token), rulesets published in **your organization's** Exchange (downloaded read-only), and local ruleset YAML files. Only rulesets that apply to A2A Brokers, A2A agents or MCP servers are listed, with chips for the asset types they cover.
    - The selection is made per project. Results show on a read-only canvas: components with findings get a shield badge (violation / warning / info); click one to filter the findings.
    - Each finding has the rule, the component, the v1 / v2 path, a fix with a copyable snippet based on the v1 / v2 reference, **Open on canvas** and the rule docs.
    - **Workspace report** with every project, **Validate all**, and a stand-alone **HTML report** (one project or the workspace, light and dark).
    - **Explain** entries for governance, rulesets and the report.
    - Shield buttons in Projects (per project and in the Projects header) and two commands: *Governance: Validate Against Rulesets* and *Governance: Workspace Report*.
    - **Local compliance check only**: the selection and the results are kept in VS Code workspace storage, never in the project. Build, publish and deploy do not read them. Reports are saved in Octoloom's storage by default, and you get a warning if you save one inside a project folder. Nothing is created or published in your org or in P4A.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Minimize to icons**: *Minimize all* on the network canvas and the broker flow shrinks every card to its icon and name (or one card at a time); auto layout packs them and the view fits the new layout. Saved with the canvas layout, not in YAML or `.agent` files.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Broker flow, actions**: executors and subagents / orchestrators can run both MCP tools and A2A agents (per the AgentScript reference). The action picker now groups the actions by kind with an explanation and suggests the bindings (`with message = ...` for A2A, tool inputs for MCP). New check: an executor that runs an A2A action without `with message = ...` (executors do not slot-fill).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Chat**: in the mini canvas, the Agents and MCP Servers boxes share the width 50/50 and fill the space when the panel is resized.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- README: new Governance and Minimize sections with screenshots, commands and known limitations.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.4.6

<span class="ol-ver-meta">2026-11-11 · released</span>

- README, Known limitations: running brokers that call an LLM locally fails with CLI plugin 1.5.0 (OpenAI returns 401 because it gets a placeholder key). The entry gives the cause, the manual workarounds tried locally (none worked) and what was tested, and recommends Deploy for LLM brokers. The old note that local run was "not available yet" is removed.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.4.5

<span class="ol-ver-meta">2026-11-11 · released</span>

- **Marketplace page / README**: new screenshots and sections:
    - New Project dialog with all **20 templates** (10 use cases, plain and governed, v1 and v2), with a table of the examples;
    - new **Code view** section (agent-network.yaml autocomplete, AgentScript reference completion, checks, Format, Apply);
    - **Broker chat** screenshot (network on the left, conversation with task states on the right);
    - updated **Projects & Deploy** screenshot (filter chips, + for new projects, tooling versions);
    - canvas minimap toggle mentioned.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- No functional changes since 0.4.2.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.4.2

<span class="ol-ver-meta">2026-11-11 · released</span>

- **Code view** (agent-network.yaml v1 and v2, AgentScript `.agent`, exchange.json) is now a real code editor:
    - Syntax colours that follow the VS Code theme, line numbers, folding, bracket matching, find (Ctrl/Cmd+F), undo history.
    - **Checks** while you type: YAML syntax errors at their position, the same problems as the Problems panel (on the key they refer to), keys that are not part of the v1 / v2 / AgentScript reference, unknown AgentScript blocks, and lines with wrong indentation. Hover an underline for the message; F8 jumps to the next one.
    - **Autocomplete** (as you type, or Ctrl+Space) from the reference: keys for the current level (keys already present are left out), values such as connection `kind`, authentication kinds, transport kinds, `inputFormat` and platforms, `ref.name` from the registry / connections, `${group.var}` from exchange.json. In `.agent` files: section and node headers, keys per node kind, `transition to` / `run` / `with` / `set`, `@generator.…` / `@actions.…` / `@llm.…` references to what is in the file, `target:` URIs from the network's connections (`llm://`, `mcp://`, `a2a://`, `brokers://…/a2a`), MCP `tool_name`s and echo `TASK_STATE_*` values.
    - **Format** (Shift+Alt+F): re-indents to 2 spaces per level. YAML is re-written by the YAML library; AgentScript keeps block text relative. Files already in the reference layout do not change.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Canvas**: the minimap can be hidden and shown again (map button in the zoom bar); the choice is kept.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Projects**: the list has filter chips (All, Deployed, Running locally, Draft, with counts), running projects come first, and *New project* (deterministic / probabilistic) moved behind a **+** in the section header. It shows automatically when there are no projects.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Projects**: the `.deployment/` folder written by Run locally is no longer picked up as a second project with the same name.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Chat**: in the mini canvas, the LLM box spans the full width under Agents and MCP.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.4.1

<span class="ol-ver-meta">2026-11-11 · released</span>

- LLMs (v2): new **Input format** field (`openai`, `anthropic`, `gemini`). With it, LLM connections can use OAuth 2.0 client credentials (JWT bearer token for an LLM gateway) and the other kinds listed under *Supported authentication*.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Problems: an LLM connection whose kind the LLM does not accept is flagged before the build (CLI error 3060), as are an invalid input format and an input format without authentication kinds (3062).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Build: when an LLM connection uses a kind other than apiKey and its LLM has no input format or does not list the kind, Octoloom adds them first (only for OpenAI, Azure OpenAI, Gemini and Anthropic platforms). API key setups are not changed.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- README: new, sharper screenshots (zoomed in, 2x) and sections on project templates (use cases / technical) and LLM authentication.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.4.0

<span class="ol-ver-meta">2026-11-11 · released</span>

- **OAuth 2.0 client credentials**: the LLM's *Supported authentication → Default configuration* now lists the attribute names for each kind and shows an example (Microsoft Entra ID token URL, `bodyEncoding: form`, scope). The connection form explains *Token URL*, *Body encoding* and *Scopes*.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **OAuth provider presets**: with *OAuth 2.0 client credentials* selected, *Fill in for…* writes the authentication block for Microsoft Entra ID, Okta, Auth0, Keycloak, Salesforce, Amazon Cognito, PingOne, Anypoint connected apps or any other OAuth 2.0 provider. It sets the token URL, body encoding and scopes, using `${provider.var}` placeholders, and declares those variables in exchange.json. The client secret is a secret variable with no default. *Setup steps for…* shows what to do at the provider (app registration, secret, role or scope), with a link to the provider's docs. For an existing block, Octoloom recognizes the provider from the token URL.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Test connectivity** applies the LLM's `defaultConfiguration` under the connection's authentication, the same way the CLI does. Token errors now come with a hint, for example "set Body encoding to form" when Entra ID reports a missing `grant_type`, or "check the client secret".

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Agent editor**: `key: -> transition to …` written on one line is shown as an error, because the CLI rejects it. Editing the block, or running Build, rewrites it in block form.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.3.6

<span class="ol-ver-meta">2026-11-11 · released</span>

- **Run locally (v2 / AgentScript)**: the play icon on a project runs the network on your machine with Docker, using `anypoint-cli agent-network project run-local`. It starts two Flex gateways (ingress and egress, registered locally in disconnected mode), a local Exchange and the agent graph. Nothing is created or changed in your Anypoint org.
    - A small form asks for the port (default 8081, or the next free port), the secrets, and watch mode (rebuild and restart on save).
    - Before it starts, Octoloom checks that Docker is installed and running and builds the project. Like deploy, it passes every exchange.json variable; secrets go through the terminal environment, not the command line. A secret left empty uses the value the CLI saved in the keychain on an earlier local run.
    - `.deployment/` is added to the project's `.gitignore`, because the local run writes gateway certificates and keys there.
    - Second status light per project (square): starting, running locally, stopped or failed, with the CLI's progress or failure reason. A local box lists the `http://localhost:<port>/<broker>/` URLs, with copy and chat buttons. A notification shows when the brokers answer.
    - The stop icon (or **Stop Local Run**) sends Ctrl+C to the run-local terminal; the CLI then stops the containers. Without a terminal it runs `stop-local`.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Broker chat**: a *Deployed / Local* switch for v2 networks chats with the broker running locally. Each target keeps its own conversation.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Known limitation** (agent-fabric plugin 1.5.0): the local egress gateway does not forward LLM API keys, so OpenAI answers 401 and brokers that call an LLM fail with "An internal error occurred". The chat shows a hint when this happens. The containers, the agent card and the broker endpoint itself work.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.3.5

<span class="ol-ver-meta">2026-11-11 · released</span>

- **Network editor templates**: the *+* (Add) menu now has a template level for each component, next to *Empty*:
    - **LLM providers** with their connection: OpenAI, Azure OpenAI, Google Gemini, LLM through a gateway, and (v2) Amazon Bedrock.
    - **Connections** to an agent or MCP server, with no authentication, API key, Basic, Client ID enforcement or OAuth 2.0 client credentials.
    - **Policies** (v2, reusable under `context.policies`): rate limiting, JWT validation, header injection, response timeout, PII detectors, MCP schema validation, prompt decorator, message logging. The schema dependency is added to exchange.json.
    - **Agents** (A2A 1.0 or 0.3.0) and **MCP servers** (streamable HTTP or SSE).
    - Each template adds its variables to exchange.json. Secrets get no default value, so deploy asks for them.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Built-in *JWT Validation* and *Message Logging* policies now start with a configuration the policy schema accepts (the build failed with "Error while trying to validate policies").

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Broker chat**, left canvas:
    - Every box expands (chevron) to show its details: description, A2A version, platform, URL and authentication; skills of the broker and the agents; tools of MCP servers (tools a v1 broker may not call are struck through); models of LLMs and the model the broker uses.
    - LLM boxes show the provider logo (OpenAI, Gemini, Bedrock, Salesforce, gateway) instead of a generic icon. The broker box has a neutral grey border.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- `.agent` editor: selecting a connection (edge) no longer breaks the view ("Cannot lerp prop className").

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- New Project dialog: the parent folder is never inside an existing project. It defaults to the last parent folder used (or the workspace folder); a folder inside a project is replaced by the folder that contains that project, and creating inside a project is refused.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.3.0

<span class="ol-ver-meta">released</span>

- **Deployment status lights** on each project in *Projects & Deploy*: grey not deployed, green deployed and running, red stopped or failed. A broker counts as running when it serves its agent card through the gateway.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Deployments are remembered** across restarts: environment, gateway, asset version and the URL of every broker (`<gateway URL>/<broker>/`, with the gateway URL read from Gateway Manager). Projects deployed before this version are found in API Manager. *Forget* removes the record without undeploying.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Broker chat**: a new window with a read-only canvas on the left and a chat with the deployed broker on the right. It includes skill shortcuts from the live agent card, task state, timing, and the raw JSON-RPC request and response. Conversations keep their context, and *input required* tasks continue. A2A 0.3.0 (v1) and 1.0 (v2). Open it from the chat icon next to a deployed broker URL, or with *Chat with Deployed Broker*.
    - The network on the left is boxed per broker: each broker box holds its agents, MCP servers and LLM, with the policies on each connection. Items no broker uses are listed separately.
    - Skill cards are larger and centered; the message box always stays visible at the bottom.
    - Probabilistic (v1, A2A 0.3.0) brokers answered every chat message with HTTP 503: the JSON-RPC id is now sent as a string.
    - Fixed "Something went wrong rendering this view" after sending a message.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- `.agent` editor *Preview* works with v1 and v2 brokers: the A2A version (0.3.0 or 1.0) is read from the agent card, with a retry in the other version when the broker refuses it. The broker URL defaults to the deployed one, conversations keep their context, and each reply shows protocol, task state, HTTP status and time. v2 brokers used to refuse every Preview message ("Unsupported A2A version").

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- After a successful deploy, a notification offers *Open chat* and *Copy URL*.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- New v2 projects from templates prefix their connection keys with the project name. API Manager uses the connection key as the instance id, and two projects with the same keys failed to deploy into one environment (HTTP 409 "API instance already exists").

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- New Project dialog: agent, MCP and policy chips are readable in dark mode.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **New Project dialog**: choose the style, then *Blank*, *Use cases* or *Technical*. 20 templates (10 per style); v1 uses A2A 0.3.0 only, v2 mixes A2A 1.0 and 0.3.0. Each network has 2–5 agents and 1–5 MCP servers, all public A²D mocks, and a README with test prompts. *Technical* variants add built-in Agent Fabric policies (rate limiting, header injection, MCP / A2A PII detection, MCP schema validation, A2A prompt decorator). Templates come from the public octoloom-assets repository, with a bundled offline copy. No credentials are included: set `openai.apiKey` at deploy time. On creation the template's asset prefix, asset id and group id are replaced with your project name and organization.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- `.agent` editor: **component templates** in a multi-level menu (+ Step, *Add node* or right-click): templates per node type plus patterns such as *Logical case selection*, *Check, then act* and *Extract, then run a tool*. Templates that need actions are disabled until the file has them.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- New generators, subagents and orchestrators get an `on_exit` to the final reply (the Agent Fabric build requires it). Transitions are written on two lines.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Instruction templates**: an *Insert template* picker on system and reasoning instructions and on v1 broker instructions.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Guides**: a short tour per canvas (Probabilistic, Deterministic, `.agent`) that highlights each area, with *Don't show again*. **Explain** shows what the selected component does, when to use it and examples.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Canvas: a node's type can no longer be changed after creation; connections can be deleted and drawn by dragging from a port.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Built-in policy list: policies the CLI already applies to every connection (tracing, telemetry, MCP support, A2A card policies, user context) are no longer offered. References to Agent Fabric policies carry their namespace.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.2.1

<span class="ol-ver-meta">released</span>

- Probabilistic (v1) networks only accept A2A **0.3.0** agents:
    - Adding an agent from the palette that declares another A2A version is refused with a message.
    - The *Protocol version* field of broker and agent cards only offers 0.3.0.
    - Problems shows an error for every broker or agent card with another or no protocol version, and for agents whose protocol is not `a2a`. Build, Publish and Deploy stop with an error while any of these remain.
    - Broker cards without a protocol version get 0.3.0 before the build.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.2.0

<span class="ol-ver-meta">released</span>

- Problems: a warning when an LLM provider has no model assigned (`metadata.models`) or when a broker uses a model its provider does not list. Calls through the gateway fail with HTTP 503 in that case. New LLM providers list `gpt-5-mini`, the broker default.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Deploy passes every exchange.json variable that has a value (the default, or what you typed in the deploy dialog) to the CLI as `--property`, so the CLI no longer asks for values you already provided. Secret values are only set in the terminal's environment: the typed command shows `$OCTOLOOM_P0`, never the value. The CLI still asks for variables without any value.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- *Test connectivity* for v1 LLM connections sends the API key from `spec.configuration.apiKey`.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Deploy, Publish, Undeploy, Unpublish and Setup gateways run in an interactive VS Code terminal. You can answer CLI prompts there, for example values for variables without a default during deploy. Credentials are passed through the environment, never on the command line. Build still writes to the *Agent Network CLI* output.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- v1 networks: an error when two brokers share the same card name (the CLI build fails on it).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- *Test connectivity* for MCP servers adds the server's transport path (for example `/mcp`) to the connection URL, as the gateway does. The live tool list uses the same URL.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Publish and Deploy build the project first. Build stops with an error toast if the build fails.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Before every build Octoloom repairs what the Agent Fabric CLI rejects and logs each fix in the *Agent Network CLI* output:
    - v1 LLM connections: the API key moves from `spec.authentication` to `spec.configuration.apiKey`. Agent and MCP connections lose a stray `spec.configuration`.
    - v1 MCP servers: `metadata.tools: {allowed: [...]}` moves to the brokers' `spec.tools[].mcp.allowed`.
    - v1 and v2 MCP servers: declared tools become a list of `{name, inputSchema}`.
    - A2A agent cards: every skill gets `tags` (and id, name, description if missing).
    - `.agent` flows: one-line `on_message: -> transition to …` is split onto two lines.
    - A missing exchange.json is created from the network's variables.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- New `.agent` broker flows use the two-line transition syntax.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- v1 connection form: *Configuration* appears only on LLM connections, *Authentication* only on agent and MCP connections.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- MCP servers declare tools as name, description and input schema. To limit which tools a broker may call, use *Allowed tools* on the broker.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- The component inspector lists only the `${…}` variables that the component and its connections use.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- New icons for agent-network.yaml, exchange.json and `.agent` broker flows, in the editor tabs and in the editor headers.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.1.6

<span class="ol-ver-meta">released</span>

- *exchange.json* on the canvas always opens the project's exchange.json next to agent-network.yaml. If it is missing, Octoloom creates a valid exchange.json with a variable for every `${…}` the network uses (URLs, API keys and secrets flagged as secret). Variables used by the network but missing in an existing exchange.json are added. An exchange.json that is not valid JSON can be replaced by the template (the old file is kept as `exchange.json.bak`).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Projects on the Octoloom home: Build, Publish, Deploy, Setup gateways, Undeploy and Unpublish are compact icons, aligned bottom right (hover for the name).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Marketplace page: new screenshots, including the A²D palette and the policy picker with P4A policies.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.1.5

<span class="ol-ver-meta">released</span>

- Checkboxes (capabilities, *Supports authenticated extended card*, …) sit on the same line as their label.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- The policy picker only lists policies for the selected component type (A2A agent, MCP server, LLM, broker), with a link to show the others. Org and P4A policies are classified from their name and description.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Agent cards without skills: *Read skills from the live agent* fills skills, capabilities and modes from the agent's `/.well-known/agent-card.json`. Adding an agent from Exchange or A²D now reads the live card too when the published card has no skills.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- The connectivity test of a v1 agent connection checks the A2A agent card (it only checked HTTP before).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.1.4

<span class="ol-ver-meta">released</span>

- One place for policies: the inspector's *Policies* section (with the policy picker) replaces the raw policy lists in the connection and broker forms.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Policy configuration is edited as fields (text, number, yes/no, lists, groups) with suggested settings for the built-in policies; a JSON view is still available and resizes in both directions.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- v1 broker: the LLM provider and model are set only under *LLM provider*; the former *Behaviour* section is now *Instructions and limits* (instructions, loops, errors, timeout, optional model parameters). Linked agents and MCP servers are edited through the *Agents* / *MCP servers* buttons.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- The connectivity test sits next to the connection (after the URL and authentication of a connection, under *Connections* for other components).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.1.3

<span class="ol-ver-meta">released</span>

- **Policies** for v1 and v2: apply them to brokers and connections from the inspector. Pick from the built-in Agent Fabric policies, your organization's Exchange policies or the **P4A catalog**. Octoloom adds the `exchange.json` dependency (classifier `schema`). Cards show the policies that are applied.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **P4A connection** (personal access token, stored in SecretStorage): a P4A policy that is not yet in your Agent Fabric org is deployed there through the P4A MCP server, after you confirm.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Header Injection editor** for custom headers next to OAuth, for example a `client_id` header that client ID enforcement requires.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Connectivity test** for brokers, agents, MCP servers, LLMs and connections: MCP initialize and tools/list, the A2A agent card, LLM `/models`. Uses the connection's auth, OAuth client credentials included.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Inline editing on cards**: allowed MCP tools, URL, LLM platform, broker limits. Click a card to open the inspector, and drag the inspector's edge to resize it.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Allowed tools** (v1) is a multi-select, with the tool list read from Exchange or the live MCP server.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- **Deterministic brokers** show the agents and MCP servers they use by section, and *Link* / *Unlink* adds or removes the actions in the `.agent` flow.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Renaming a broker, agent or connection updates its references, including the `.agent` flows.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- LLM provider logos in the inspector header and in the broker flow LLM list.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Fixed: deleting the *Done* node of a flow crashed the editor. Start and *Done* nodes can no longer be deleted.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.1.2

<span class="ol-ver-meta">released</span>

- Issues, repository and homepage links now point to the public octoloom-assets repository.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.1.1

<span class="ol-ver-meta">released</span>

- Agent Fabric assets dropped on the canvas are referenced and declared as `exchange.json` dependencies (`agent-metadata` / `mcp-metadata`) for v1 and v2, instead of being copied into the network. Removing one also removes its dependency.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- The Problems panel warns about references that are neither declared nor dependencies (build error 3009).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- New Agent Fabric logo.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Marketplace screenshots now load from a public host.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>


## 0.1.0

<span class="ol-ver-meta">released</span>

First release of **Octoloom for Agent Fabric**.

- Visual canvases for `agent-network.yaml`: Probabilistic (v1) and Deterministic (v2).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Broker flow editor for `brokers/*.agent` (AgentScript).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Form editor for `exchange.json`.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Asset palette with Agent Fabric (Exchange) and A²D assets, drag and drop onto the canvas, and card or row layouts.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Origin tags (A²D / Agent Fabric) and agent framework detection with a picker.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- LLM provider logos (OpenAI, Gemini, Amazon Bedrock, Salesforce) and Omni gateway detection from the URL.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- LLM provider and model picker for brokers, for both v1 and v2.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Collapse cards, fold sections, and hide or show connected cards (including a broker's LLM).

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Build, publish, deploy, undeploy, unpublish and gateway setup through anypoint-cli-v4, with automatic install of Node.js, Java 17 and the CLI plugin.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>

- Light, dark and auto themes.

    <span class="ol-by">:material-account-heart-outline: [Gabriel Bustos Sölch](https://github.com/gabrielmule), [Amir Khan](https://github.com/amirkhan-ak-sf)</span>
