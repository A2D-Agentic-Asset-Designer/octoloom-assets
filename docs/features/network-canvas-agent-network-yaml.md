<span class="ol-pill">Design</span>

# Network canvas

<p class="lede"><strong>The visual editor of `agent-network.yaml`: brokers, agents, MCP servers, LLMs and their connections as cards, with an inspector on the right.</strong> See the whole network and change it without hand-editing YAML; the YAML stays the source and is always in sync.</p>

!!! info "Where to find it"
    Open `agent-network.yaml` · **Network** in any Octoloom toolbar

<figure markdown>
![A deterministic (2.0) network: broker, agents, MCP server and LLM](../assets/ui/network-v2-annot-light.webp#only-light){ loading=lazy }
![A deterministic (2.0) network: broker, agents, MCP server and LLM](../assets/ui/network-v2-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>A deterministic (2.0) network: broker, agents, MCP server and LLM</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **Agent Network 2.0** | Agent Network 2.0: AgentScript brokers (.agent) with explicit, deterministic flows. |
| <span class="ol-n">2</span> | **Visual** | Visual canvas |
| <span class="ol-n">3</span> | **Code** | YAML source |
| <span class="ol-n">4</span> | **Network** | Open the Agent Network view of the deployed network |
| <span class="ol-n">5</span> | **exchange.json** | Open the Exchange asset form of this project |
| <span class="ol-n">6</span> | **Build & Deploy** | Validate, build, publish and deploy this network |
| <span class="ol-n">7</span> | **Save** | Save the file (the YAML stays the source of truth) |
| <span class="ol-n">8</span> | **Flow** | Open the broker flow (.agent) |
| <span class="ol-n">9</span> | **Collapse card** | Collapse or expand the card body |
| <span class="ol-n">10</span> | **Edit** | Edit the linked agents or MCP servers of this broker |
| <span class="ol-n">11</span> | **Add to the network** | Add a broker, agent, MCP server, LLM or policy |
| <span class="ol-n">12</span> | **Asset Palette** | Asset Palette (Exchange / A²D) |
| <span class="ol-n">13</span> | **Auto layout** | Arrange the cards automatically |
| <span class="ol-n">14</span> | **Minimize all components to their icons** | Minimize all components to their icons (click an icon to open or minimize one). Auto layout packs them. |
| <span class="ol-n">15</span> | **Zoom out** | Zoom the canvas out |
| <span class="ol-n">16</span> | **90%** | Reset to 100% |
| <span class="ol-n">17</span> | **Zoom in** | Zoom the canvas in |
| <span class="ol-n">18</span> | **Fit to screen** | Fit all cards into the view |
| <span class="ol-n">19</span> | **Hide the minimap** | Show or hide the minimap |
| <span class="ol-n">20</span> | **Explain anything** | Explain anything: click, then click any object (the guided tour starts from here too). Drag to move; double-click to reset its place |

## How to use it

1. Click **+** (Add to the network) to add a broker, agent, MCP server or LLM, or drag one from the **Asset Palette**.
2. Drag from a card's port to another card to connect them.
3. Click a card to edit it in the **inspector** (name, description, URL, policies, authentication).
4. Watch the **Problems** bar; click a problem to jump to the card, or **Fix** where offered.
5. Click **Save**, then **Build & Deploy**.

## More screenshots

<figure markdown>
![A probabilistic (1.0) network](../assets/ui/network-v1-light.webp#only-light){ loading=lazy }
![A probabilistic (1.0) network](../assets/ui/network-v1-dark.webp#only-dark){ loading=lazy }
<figcaption>A probabilistic (1.0) network</figcaption>
</figure>

<figure markdown>
![Context edges between a broker and its agents](../assets/ui/network-v2-context-light.webp#only-light){ loading=lazy }
![Context edges between a broker and its agents](../assets/ui/network-v2-context-dark.webp#only-dark){ loading=lazy }
<figcaption>Context edges between a broker and its agents</figcaption>
</figure>

<figure markdown>
![The Problems bar with Fix buttons](../assets/ui/network-problems-fix-light.webp#only-light){ loading=lazy }
![The Problems bar with Fix buttons](../assets/ui/network-problems-fix-dark.webp#only-dark){ loading=lazy }
<figcaption>The Problems bar with Fix buttons</figcaption>
</figure>

<figure markdown>
![A warning in Problems: an MCP URL that ends in /mcp](../assets/ui/network-mcp-url-light.webp#only-light){ loading=lazy }
![A warning in Problems: an MCP URL that ends in /mcp](../assets/ui/network-mcp-url-dark.webp#only-dark){ loading=lazy }
<figcaption>A warning in Problems: an MCP URL that ends in /mcp</figcaption>
</figure>

<figure markdown>
![The canvas buttons explain themselves on hover](../assets/ui/network-fab-tip-light.webp#only-light){ loading=lazy }
![The canvas buttons explain themselves on hover](../assets/ui/network-fab-tip-dark.webp#only-dark){ loading=lazy }
<figcaption>The canvas buttons explain themselves on hover</figcaption>
</figure>

## In detail

- Cards for **brokers, agents, MCP servers and LLMs**, with edges for the references between them. Ports sit on the exact row an edge refers to. On a v2 canvas the **Context** card (the `context.policies` and connections without an owner) sits left of the brokers, and an orange edge connects it to each broker's **Context** row.
- **Dashed icon tile** = an **external asset**: an agent, MCP server or LLM referenced from Exchange (an `exchange.json` dependency) instead of declared in this project, for example MuleSoft's `openai` LLM in the v2 templates. The dashes take the card's colour (cyan for LLMs, blue for agents, pink for MCP servers), and its Exchange settings are read-only on the card.
- **Add menu with templates** (the *+* button): each component offers *Empty* or a ready-made entry: LLM providers (OpenAI, Azure OpenAI, Gemini, LLM through a gateway, Bedrock on v2), connections with a chosen authentication, reusable v2 policies, A2A 1.0 / 0.3.0 agents and HTTP / SSE MCP servers. Variables go into `exchange.json`; secrets have no default and are asked for at deploy time.
- **Tool stack** on the left of the canvas: **+** Add, **Asset Palette**, **Auto layout** and **Minimize all**. Hover a button to see its name.
- **Inspector** panel: identity, connections, interfaces (A2A card, skills), MCP tools, framework, tags, description, **policies** and a **connectivity test**. Drag its left edge to resize it.
- **Inline editing**: click a value with a dashed underline, or the pencil on a row, to edit it on the card. Examples: allowed MCP tools (multi-select read from Exchange or the live server), connection URL, LLM platform, broker loops and timeout.
- **Allowed tools** (v1): choose any number of tools of an MCP server with checkboxes. No selection means all tools are allowed.
- **Deterministic brokers** (v2) show the agents and MCP servers they use, grouped by section. *Link* adds the matching actions to the broker's `.agent` flow (`a2a://…` / `mcp://…`), and the trash icon removes them. An agent or MCP server that no broker uses shows a *Link to …* shortcut.
- **Delete** a component: select it and press <kbd>Delete</kbd>, or use the trash icon in the inspector. Its references, connection and `exchange.json` dependency are removed with it. A flow's start and *Done* nodes cannot be deleted.
- **Collapse** any card, **fold** a section, or **hide/show** connected cards with the eye button (for example, hide every MCP server of a broker, or its LLM). Positions and visibility are saved for each workspace.
- **Problems** panel with schema validation. Click a problem to jump to the card.
- **Auto layout**, zoom and fit, and a minimap you can collapse or show from the toolbar.
- Switch between **Visual** and **Code** at any time. Edits go to the YAML directly, and comments and formatting are kept. See [Code view](#code-view-yaml-agentscript-json).

## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### Agent network canvas

The canvas of one agent network file: brokers, agents, MCP servers, LLMs, connections and policies as cards with edges between them. It edits the YAML, which stays the source of truth.

**When to use it:** Designing or reviewing a network.

**Examples and details:**

- Drag from a port to another card to connect them
- Select a card to edit it in the inspector
- Use the zoom bar, minimap and Minimize all to find your way in a large network
- Hover a button of the tool stack on the left (+ Add, Asset Palette, Auto layout, Minimize all) to see its name
- A dashed icon tile (in the card's colour) marks an external asset: an agent, MCP server or LLM referenced from Exchange (exchange.json dependency) and not declared in this project

### Broker

<div class="grid" markdown>

![card-broker](../assets/ui/card-broker-light.webp#only-light){ loading=lazy }
![card-broker](../assets/ui/card-broker-dark.webp#only-dark){ loading=lazy }

The agent your users call. In 1.0 it is an LLM with instructions, linked agents and MCP tools. In 2.0 it is an AgentScript flow with an A2A interface.

**When to use it:** One per entry point. Split brokers by audience or domain.

</div>

**Examples and details:**

- Customer service front door
- Returns flow with eligibility gate
- IT helpdesk triage
- Kind and Implementation (.agent) of a 2.0 broker are in Protected broker settings, locked like the protected exchange.json defaults: click the lock icon to change them; the YAML always edits everything
- Removing a 2.0 broker asks whether to delete its .agent flow file too (it goes to the Trash; a file another broker uses is never offered)
- A 2.0 flow needs at least a trigger, one agent node (generator, subagent or orchestrator) and a reply (echo): delete anything else and the build still passes

### Agent

<div class="grid" markdown>

![card-agent](../assets/ui/card-agent-light.webp#only-light){ loading=lazy }
![card-agent](../assets/ui/card-agent-dark.webp#only-dark){ loading=lazy }

A remote A2A agent described by its agent card (skills, URL, protocol version). Brokers call it through a connection.

**When to use it:** A capability already exists as an agent (Agentforce, A2D mock, custom).

</div>

**Examples and details:**

- Refund agent (A2A 1.0)
- Order status agent (A2A 0.3.0)

### MCP server

<div class="grid" markdown>

![card-mcp](../assets/ui/card-mcp-light.webp#only-light){ loading=lazy }
![card-mcp](../assets/ui/card-mcp-dark.webp#only-dark){ loading=lazy }

A Model Context Protocol server with tools. Brokers may call only the tools you allow. Its connection URL is the server base: the runtime adds metadata.transport.path (for example /mcp).

**When to use it:** Deterministic system access: look up, create, update records.

</div>

**Examples and details:**

- orders_mcp: check_return_eligibility, create_rma
- crm_mcp: find_customer
- URL https://host/product-mcp/ + path /mcp → the runtime calls https://host/product-mcp/mcp (a URL ending with /mcp would call /mcp/mcp)

### LLM provider

<div class="grid" markdown>

![card-llm](../assets/ui/card-llm-light.webp#only-light){ loading=lazy }
![card-llm](../assets/ui/card-llm-dark.webp#only-dark){ loading=lazy }

The model provider and models brokers may use. The key comes from a connection secret at deploy time. A dashed icon tile means the LLM is referenced from Exchange (an exchange.json dependency, classifier llm-metadata), not declared in this project; its Platform and Models are read-only on the card.

**When to use it:** Every network that has a 1.0 broker or AgentScript LLM nodes.

</div>

**Examples and details:**

- OpenAI gpt-5-mini
- Azure OpenAI deployment
- Dashed tile: MuleSoft openai from Exchange, shared by every project that references it

### Connection

Where and how the gateway reaches an agent, MCP server or LLM: URL, authentication and policies.

**When to use it:** One per upstream. Change URLs per environment with variables.

**Examples and details:**

- ${refundAgent.url} with PII detection inbound
- openai_connection with apiKey ${openai.apiKey}
- MCP connection URL = server base without /mcp; Test connection calls exactly what the runtime calls

### Inspector

The properties of the selected card or node. Edits go straight into the file.

**When to use it:** After selecting something on the canvas.

**Examples and details:**

- Drag its left edge to resize it; the width is kept
- Close it to give the canvas more room

### Canvas tools

<div class="grid" markdown>

![canvas-fabs](../assets/ui/canvas-fabs-light.webp#only-light){ loading=lazy }
![canvas-fabs](../assets/ui/canvas-fabs-dark.webp#only-dark){ loading=lazy }

The zoom bar, minimap and floating buttons of a canvas: zoom, fit, auto layout, Minimize all / Open all and the map of the whole canvas.

**When to use it:** Finding your way in a large canvas.

</div>

**Examples and details:**

- Fit shows every card
- Click the minimap to jump there
- Minimize all turns every card into its icon

### Problems

<div class="grid" markdown>

![problems-bar](../assets/ui/problems-bar-light.webp#only-light){ loading=lazy }
![problems-bar](../assets/ui/problems-bar-dark.webp#only-dark){ loading=lazy }

The validation findings of this file and the project checks across agent-network.yaml, exchange.json and the broker .agent files: errors, warnings and hints with the object they are about. A finding with a fix has a button that applies it as one edit: one Undo reverts every file it changed, and nothing is saved until you save. The same findings are in the VS Code Problems panel with a light bulb quick fix. When you save agent-network.yaml or a .agent file, variables it uses that exchange.json does not declare are added there (unsaved; setting agentNetwork.syncVariablesOnSave turns this off).

**When to use it:** Before a build or deploy; errors stop the build.

</div>

**Examples and details:**

- Click a problem to select the card it is about; in a broker flow it also opens the field the problem is about (for example Go to or Prompt)
- Collapse the bar with its chevron
- Two brokers share brokers/sales.agent: click Copy the flow to brokers/support.agent
- Variable ${crm.url} is not declared: click Add to exchange.json
- Renaming a broker offers to rename its .agent file too
- A flow path ends without a final reply: click Go to the final reply (done) to wire it (setting agentNetwork.flowCoach turns this suggestion off)
- The broker flow checks what Agent Fabric rejects at build or deploy: one trigger per interface, no transition back to the trigger, every path ending in a completed, failed, canceled or rejected reply, empty prompts, unknown LLM settings and out-of-range temperature or top_p
- Network checks: a broker card needs a description and unique skill ids; amazonSigv4 is for LLM connections only; a TLS context needs both name and group; OBJECT_STORE_DEFAULT_TTL_MS is at most 30 days
- Deleting an agent or MCP server also removes the flow actions that called it and the variables only it used, in one Undo; a message says what went with it
