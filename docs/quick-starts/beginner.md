<span class="ol-pill">Quick Start · Beginner · ~30 min</span>

# Beginner journey

<p class="lede">Pick a fully mocked template, learn the canvas, run a Deterministic network locally, then deploy it to your Omni Gateway and chat with it. No LLM key needed.</p>

**Needs:** Anypoint. **Steps:** 9. Open it in VS Code with **Home → Quick Start → Beginner**, or *Octoloom: Quick Start* in the Command Palette.

## The journey at a glance

1. [Anypoint account](#1-anypoint-account)
2. [Small Managed Omni Gateway](#2-small-managed-omni-gateway)
3. [Connected app Octoloom-CA](#3-connected-app-octoloom-ca)
4. [Connect Octoloom to Agent Fabric](#4-connect-octoloom-to-agent-fabric)
5. [A fully mocked template](#5-a-fully-mocked-template)
6. [Learn the canvas](#6-learn-the-canvas)
7. [Run it locally (Deterministic)](#7-run-it-locally-deterministic)
8. [Deploy to your Omni Gateway](#8-deploy-to-your-omni-gateway)
9. [Chat and trace](#9-chat-and-trace)

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

### 5. A fully mocked template

<figure markdown>
![Beginner onboarding tab, step 5 of 9: A fully mocked template](../assets/ui/qs-beginner-4-light.webp#only-light){ loading=lazy }
![Beginner onboarding tab, step 5 of 9: A fully mocked template](../assets/ui/qs-beginner-4-dark.webp#only-dark){ loading=lazy }
<figcaption>Beginner onboarding tab, step 5 of 9: A fully mocked template</figcaption>
</figure>


| | **Probabilistic** (v1) | **Deterministic** (v2) |
|---|---|---|
| Who decides | An LLM broker reads its instructions and picks agents and MCP tools | An AgentScript flow decides every step: routers, gates, executors |
| Protocol | A2A 0.3.0 | A2A 1.0 and 0.3.0 |
| Good for | Open questions, assistants | Processes with fixed steps |
| Run locally | – | Yes (Docker Desktop) |

**Fully mocked templates**: every agent, MCP server and the LLM are A²D mocks. They deploy and answer without an OpenAI key or a real back end.

| Probabilistic | Deterministic |
|---|---|
| Hotel Concierge | Event Ticketing |
| Library Services | Warranty Repair |
| Fleet Maintenance | Utility Outage |

Click **New Deterministic network** (recommended) or **New Probabilistic network**, choose **Use cases**, then a template marked *fully mocked*. Or pick one under **Templates for this journey** in the tab (listed at the end of this page) and create it right here.


<figure markdown>
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-light.webp#only-light){ loading=lazy }
![New project: style, start from, the template list and the README preview](../assets/ui/new-project-dark.webp#only-dark){ loading=lazy }
<figcaption>New project: style, start from, the template list and the README preview</figcaption>
</figure>

### 6. Learn the canvas

<figure markdown>
![Beginner onboarding tab, step 6 of 9: Learn the canvas](../assets/ui/qs-beginner-5-light.webp#only-light){ loading=lazy }
![Beginner onboarding tab, step 6 of 9: Learn the canvas](../assets/ui/qs-beginner-5-dark.webp#only-dark){ loading=lazy }
<figcaption>Beginner onboarding tab, step 6 of 9: Learn the canvas</figcaption>
</figure>


The project opens on the canvas. Everything you see is written to the project files: `agent-network.yaml`, the `.agent` flow files and `exchange.json` stay visible and editable.

- **Brokers** (purple) receive the requests and call the **agents** (blue) and **MCP servers** (pink). The **LLM** (teal) is the model a broker or flow step uses.
- **Policies** (amber) protect a broker or a connection.
- The **Asset Palette** on the left lists what you can drop on the canvas: Exchange, A²D, IDMC.
- **Problems** at the bottom lists what still blocks a build.
- The floating **Explain** button explains any component with examples; **Start the guide** replays the tour of the canvas.
- On a Deterministic network, open a broker's **flow** to see its steps.

Click a card and read its Explain text before you go on.


<figure markdown>
![A deterministic (2.0) network: broker, agents, MCP server and LLM](../assets/ui/network-v2-light.webp#only-light){ loading=lazy }
![A deterministic (2.0) network: broker, agents, MCP server and LLM](../assets/ui/network-v2-dark.webp#only-dark){ loading=lazy }
<figcaption>A deterministic (2.0) network: broker, agents, MCP server and LLM</figcaption>
</figure>

### 7. Run it locally (Deterministic)

<figure markdown>
![Beginner onboarding tab, step 7 of 9: Run it locally (Deterministic)](../assets/ui/qs-beginner-6-light.webp#only-light){ loading=lazy }
![Beginner onboarding tab, step 7 of 9: Run it locally (Deterministic)](../assets/ui/qs-beginner-6-dark.webp#only-dark){ loading=lazy }
<figcaption>Beginner onboarding tab, step 7 of 9: Run it locally (Deterministic)</figcaption>
</figure>


**Run locally** starts the network on your machine in Docker. Nothing changes in your Anypoint org.

1. Start **Docker Desktop**.
2. In **Projects & Deploy**, click the **play** icon of the project (or run *Octoloom: Run Locally*).
3. Wait for the square status light to turn green. Brokers answer on `http://localhost:<port>/<broker>/`.
4. Click **Open chat**, switch the chat to **Local** and send a message.
5. Stop the run with the **stop** icon.

Probabilistic networks: skip this step and deploy.

> If the broker's LLM call fails locally (a known limitation of CLI plugin 1.5.0, see *Known limitations* in the README), go on with **Deploy**: the deployed network answers.


<figure markdown>
![Run locally: variables](../assets/ui/run-local-vars-light.webp#only-light){ loading=lazy }
![Run locally: variables](../assets/ui/run-local-vars-dark.webp#only-dark){ loading=lazy }
<figcaption>Run locally: variables</figcaption>
</figure>

### 8. Deploy to your Omni Gateway

<figure markdown>
![Beginner onboarding tab, step 8 of 9: Deploy to your Omni Gateway](../assets/ui/qs-beginner-7-light.webp#only-light){ loading=lazy }
![Beginner onboarding tab, step 8 of 9: Deploy to your Omni Gateway](../assets/ui/qs-beginner-7-dark.webp#only-dark){ loading=lazy }
<figcaption>Beginner onboarding tab, step 8 of 9: Deploy to your Omni Gateway</figcaption>
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

### 9. Chat and trace

<figure markdown>
![Beginner onboarding tab, step 9 of 9: Chat and trace](../assets/ui/qs-beginner-8-light.webp#only-light){ loading=lazy }
![Beginner onboarding tab, step 9 of 9: Chat and trace](../assets/ui/qs-beginner-8-dark.webp#only-dark){ loading=lazy }
<figcaption>Beginner onboarding tab, step 9 of 9: Chat and trace</figcaption>
</figure>


1. Click **Open chat** on the deployed project.
2. Send one of the sample prompts of the template's README.
3. Watch the live status (*Working on it…*) and the **Network** view: every call between broker, agents and MCP servers is numbered.
4. Open **Traces** for the timing of each call, and the **Tracer** for the details.

You built, deployed and talked to your first agent network.


<figure markdown>
![Chat with live progress updates](../assets/ui/chat-progress-light.webp#only-light){ loading=lazy }
![Chat with live progress updates](../assets/ui/chat-progress-dark.webp#only-dark){ loading=lazy }
<figcaption>Chat with live progress updates</figcaption>
</figure>

<figure markdown>
![The trace of a reply: every call in order, one failed](../assets/ui/chat-trace-light.webp#only-light){ loading=lazy }
![The trace of a reply: every call in order, one failed](../assets/ui/chat-trace-dark.webp#only-dark){ loading=lazy }
<figcaption>The trace of a reply: every call in order, one failed</figcaption>
</figure>

## Templates for this journey

The Beginner tab lists these templates; click one to create the project right in the tab.

| Template | Style | Agents | MCP | Tutorial |
|---|---|---|---|---|
| [Event Ticketing (fully mocked)](../catalog/v2-event-ticketing.md) | Deterministic | 2 | 2 | [Tutorial](../tutorials/v2-event-ticketing.md) |
| [Utility Outage (fully mocked)](../catalog/v2-utility-outage.md) | Deterministic | 3 | 2 | [Tutorial](../tutorials/v2-utility-outage.md) |
| [Warranty Repair (fully mocked)](../catalog/v2-warranty-repair.md) | Deterministic | 3 | 1 | [Tutorial](../tutorials/v2-warranty-repair.md) |
| [Fleet Maintenance (fully mocked)](../catalog/v1-fleet-maintenance.md) | Probabilistic | 2 | 4 | [Tutorial](../tutorials/v1-fleet-maintenance.md) |
| [Hotel Concierge (fully mocked)](../catalog/v1-hotel-concierge.md) | Probabilistic | 2 | 1 | [Tutorial](../tutorials/v1-hotel-concierge.md) |
| [Library Services (fully mocked)](../catalog/v1-library-services.md) | Probabilistic | 2 | 3 | [Tutorial](../tutorials/v1-library-services.md) |

---

**Next:** [the Advanced journey](advanced.md)
