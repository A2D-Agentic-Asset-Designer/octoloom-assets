<span class="ol-pill">Start</span>

# Home page

<p class="lede"><strong>Your start page: create a network, reopen a recent project, open a tutorial and see your own usage numbers.</strong> It is the shortest way back into your work and shows, at a glance, how much you have built.</p>

!!! info "Where to find it"
    Opens when VS Code starts · **Projects & Deploy → Home** · *Octoloom: Welcome*

<figure markdown>
![The Home page: start cards, tutorials, recently built projects and your statistics](../assets/ui/welcome-annot-light.webp#only-light){ loading=lazy }
![The Home page: start cards, tutorials, recently built projects and your statistics](../assets/ui/welcome-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>The Home page: start cards, tutorials, recently built projects and your statistics</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **Open folder…** | Open the project folder |
| <span class="ol-n">2</span> | **Projects & Deploy** | The projects list with status lights |
| <span class="ol-n">3</span> | **Setup & Connect** | Connect Anypoint, A²D and IDMC |
| <span class="ol-n">4</span> | **Getting started** | Open the Getting started tutorial on GitHub |
| <span class="ol-n">5</span> | **All template tutorials** | Open the list of template tutorials on GitHub |
| <span class="ol-n">6</span> | **Open the Octoloom documentation site** | Open the Octoloom documentation site (octoloom.a2d-ai.com): every view, button and component with screenshots |
| <span class="ol-n">7</span> | **Open folder** | Open the folder in this window |
| <span class="ol-n">8</span> | **Open the coverage map** | Open the coverage map: policies, governance, authentication and where the assets of every agent network come from |
| <span class="ol-n">9</span> | **Explain anything** | Explain anything: click, then click any object (the guided tour starts from here too). Drag to move; double-click to reset its place |

<figure markdown>
![The installed version, with a link when the Marketplace has a newer one](../assets/ui/welcome-update-light.webp#only-light){ loading=lazy }
![The installed version, with a link when the Marketplace has a newer one](../assets/ui/welcome-update-dark.webp#only-dark){ loading=lazy }
<figcaption>The installed version, with a link when the Marketplace has a newer one</figcaption>
</figure>

## How to use it

1. Click **New Probabilistic Network** or **New Deterministic Network** to open New project with that style.

2. Under **Recently built**, click a card to open its canvas, or *Open folder* to open it in this window.

3. Under **Tutorials**, open *Getting started*, the tutorial list or **Documentation** (this site).

4. Under **Your statistics**, click **Coverage map** to see policy, auth and governance coverage.

## In detail

When VS Code starts, Octoloom opens its **Welcome** page next to the VS Code one. It doesn't open when you click the Octoloom icon later. You can also open it with the home button in **Projects & Deploy** or with **Octoloom: Welcome**.

The page has five sections, in this order. Each is open by default; click its heading to fold it, and Octoloom remembers that.

- **Quick Actions:** cards for a new **Probabilistic** or **Deterministic** network. Each opens New Project with that style. There are also links to Open folder, Projects & Deploy, Setup & Connect and the **Coverage map**.
- **Quick Start:** three guided journeys (Beginner walks, Advanced runs, Expert climbs), each in its own Octoloom tab: the steps on the left, a page with pictures of the Anypoint screens on the right, buttons that open the right view, and Previous / Next. Each journey lists only its own templates. Reopen them any time with *Octoloom: Quick Start*. The chips on each card show which connections it needs and which are already in place.
  - **Prerequisites** (every journey):
    1. An Anypoint account: [sign up](https://anypoint.mulesoft.com/login/signup) or log in.
    2. A **Small Managed Omni Gateway**: Runtime Manager → Omni Gateways → Add Managed Omni Gateway, for example `octoloom-tutorial`; Edge channel, 1.15.0 or later; *Upstream Response Timeout* and *Connection Idle Timeout* 60 s; *Distributed Tracing* on. **Check my gateway** lists the gateways of the connected environment.
    3. A connected app `Octoloom-CA` (client credentials) with **least-privilege scopes**, not *Select all*.
    4. Connect Octoloom to Agent Fabric.
  - **Beginner:** a fully mocked template (Probabilistic or Deterministic), the canvas explained, Run locally for a Deterministic network, deploy, chat and trace. No LLM key needed.
  - **Advanced:** adds **Connect to A²D** (an API key from A2D → Settings → Organization Settings → API Keys). Then a use-case network built with A²D mock agents, MCP servers and LLM mocks; deploy, chat, trace and share it in an A²D session.
  - **Expert:** adds **Connect to A²D** and **Connect to P4A**. For P4A you need a personal access token (`p4a_…`), and to deploy P4A policies, a P4A connection to your Anypoint org and a workspace. Then a governed or secured technical template, Agent Fabric and P4A policies, Governance, deploy and the Coverage map.
- **Tutorials:** *Getting started* (a 10-step tour of Octoloom) and *All template tutorials*: one per template, with **Just use it** (create, deploy, chat) and **Learn step by step** (canvas, broker flow, policies, deploy, chat, Tracer, with screenshots) and **Build it from scratch** (an empty project, then every card, connection and policy added by hand, with screenshots). They live in [octoloom-assets/tutorials](../tutorials/index.md). **Documentation** opens the [Octoloom documentation site](https://octoloom.a2d-ai.com/).
- **Recently built:** the 5 agent network projects built last on this machine, as cards. Each card shows the style, agents, MCP servers, policies and when the project was built. Click a card to open its canvas, or *Open folder* to open the project in this window.
- **Your statistics** (this user profile):
  - workspaces opened with Octoloom;
  - network projects and the Probabilistic / Deterministic ratio;
  - brokers, agents and MCP servers;
  - Exchange and A²D assets (A2A + MCP);
  - policies used in networks;
  - deployments and publishes to Exchange;
  - the top 3 LLM providers.
- **How it is counted:** totals come from the projects Octoloom has seen in your workspaces. Builds, deploys and publishes count when they succeed. Projects built before 0.6.7 are picked up from their `target/` folder. The numbers stay on your machine (the anonymous usage counts are separate, see [Privacy and security](#privacy-and-security)).
- **Version:** under the title you see the installed Octoloom version. When the Visual Studio Marketplace has a newer one, a link (*0.9.26 available on the Marketplace*) opens Octoloom in the Extensions view so you can update. **Setup & Connect → Tooling** shows the same in its Octoloom row.
- **Turning it off:** clear *Show on startup* or set `agentNetwork.showWelcome`.



## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### Octoloom Welcome

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

### Tutorials

Links to the Octoloom tutorials on GitHub (octoloom-assets/tutorials): Getting started, a tour of Octoloom from Setup & Connect to chat, trace and share, and one tutorial per template project. Each template tutorial has three paths: Just use it (create, deploy, chat in 3 steps), Learn step by step (the canvas, the broker flow, policies, validate, build, deploy, chat and trace, explained with screenshots) and Build it from scratch (start from an empty project and add every broker, agent, MCP server, LLM, connection and policy yourself, with screenshots). The Documentation link opens the Octoloom documentation site (octoloom.a2d-ai.com): every view, button and component explained with screenshots, all templates and tutorials, and the version history.

**When to use it:** You are new to Octoloom, or want to see what a template does before you create it. The links open in your browser.

**Examples and details:**

- Getting started: the 10-step tour
- All template tutorials: the list of every template, Probabilistic and Deterministic, with its agents, MCP servers and policies
- Retail Returns is the smallest deterministic template to start with
- Build it from scratch: the same network as the template, built card by card from New Project → Empty

### Octoloom version

The Octoloom version installed in this VS Code. Once per session Octoloom reads the latest version from the public Visual Studio Marketplace (a read-only request that sends no project or usage data). When a newer version exists, Octoloom Welcome and Setup & Connect → Tooling say "<version> available"; click it to open Octoloom in the Extensions view and update.

**When to use it:** Check which version you run before you report a problem, or update when a new version is available. Offline or behind a proxy, only the installed version is shown.

**Examples and details:**

- Octoloom Welcome: "Version 0.9.25" under the title
- Tooling: the Octoloom row shows the installed version, with a warning and "0.9.26 available" when there is an update
- Click "available" to open the extension page in the Extensions view, where Update installs it
