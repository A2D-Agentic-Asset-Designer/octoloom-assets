<span class="ol-pill">UI reference</span>

# Toolbar buttons

<p class="lede">The buttons at the top of every Octoloom editor.</p>

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

## Visual / Code

Switches between the visual editor (canvas or form) and the source text of the same file. Both edit the file itself; nothing is converted or stored elsewhere.

**When to use it:** Code for a quick text edit, search (Cmd/Ctrl+F) or to see exactly what is saved; Visual for everything else.

**Examples and details:**

- An edit in Code shows on the canvas at once
- YAML errors: Fix in code opens the line

## Explorer

Shows or hides the outline of the flow on the left: sections, nodes and their order.

**When to use it:** To find a node in a long flow, or to make room for the canvas.

**Examples and details:**

- Click a node in the outline to select it on the canvas

## Network

Opens agent-network.yaml of this project on its canvas: the brokers, agents, MCP servers, LLMs and connections.

**When to use it:** To change what this broker connects to, or to build, publish and deploy the project.

**Examples and details:**

- From a flow: open the network the broker belongs to

## Network settings

Opens the settings of the whole network in the side panel: name, description (shown in Exchange) and other network-level fields.

**When to use it:** To change what Exchange shows for this network.

**Examples and details:**

- Set the description Exchange shows on the asset page

## Preview

A small chat panel beside the flow that sends messages to the deployed broker at a URL you enter (with an optional Authorization header). It talks to a running deployment; editing the flow changes nothing there until you publish and deploy again.

**When to use it:** To try the broker of this flow after a deploy without leaving the editor.

**Examples and details:**

- Paste the broker URL from Projects & Deploy
- For the full chat with traces, use the chat from Projects & Deploy

## New Version

Sets the next Major, Minor or Patch version in exchange.json and saves all files. It starts from the highest version already in Exchange, so the new number is always free. Nothing is published yet.

**When to use it:** Once before each publish of a change. Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again.

**Examples and details:**

- Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again
- Deploy with "Publish before deploy" publishes this same version
- No bump is needed to deploy a version that is already published: turn Publish before deploy off
- Major for a breaking change, Minor for new features, Patch for fixes

## Commit Version

Bumps the patch version in exchange.json to the next free one (from the highest in Exchange) and saves all files. It is the quick form of New Version → Patch. It does not publish, and it is not a Git commit.

**When to use it:** After a change, before Publish (or a deploy that publishes).

**Examples and details:**

- 1.0.3 is the highest in Exchange, exchange.json says 1.0.1: Commit Version sets 1.0.4
- Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again
- Then Publish (or Deploy with Publish before deploy)

## Bump patch

Raises the patch number of the version in this form by one (the tooltip shows the result). Save to keep it. It counts from this file only; New Version and Commit Version in the flow editor also look at Exchange.

**When to use it:** Before the next Publish of a change.

**Examples and details:**

- 1.0.0 → 1.0.1
- Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again

## exchange.json

Opens the Exchange descriptor of this project in its form: name, version, variables, dependencies and runtime limits.

**When to use it:** To change the version, a variable default or what Exchange shows.

**Examples and details:**

- Set a variable default for deploy and local runs

## Build & Deploy

The project actions: Validate (dry run, changes nothing), Build (local package), Publish (to Exchange, the version in exchange.json), Deploy… (to a gateway), Setup gateways… and Undeploy….

**When to use it:** To ship the network. Validate first when unsure.

**Examples and details:**

- Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again
- Deploy… opens the same form as the rocket in Projects & Deploy

## Save

Saves this file (the same as Cmd/Ctrl+S). The canvas and the form edit the file text, so what you see is what is saved.

**When to use it:** Whenever you want the change on disk; Build and Publish use saved files.

**Examples and details:**

- Unsaved changes show a dot on the editor tab
