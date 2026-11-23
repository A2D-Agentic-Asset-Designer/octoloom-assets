<span class="ol-pill">UI reference</span>

# Network components

<p class="lede">The cards of the network canvas (`agent-network.yaml`).</p>

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

## Broker

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

## Agent

<div class="grid" markdown>

![card-agent](../assets/ui/card-agent-light.webp#only-light){ loading=lazy }
![card-agent](../assets/ui/card-agent-dark.webp#only-dark){ loading=lazy }

A remote A2A agent described by its agent card (skills, URL, protocol version). Brokers call it through a connection.

**When to use it:** A capability already exists as an agent (Agentforce, A2D mock, custom).

</div>

**Examples and details:**

- Refund agent (A2A 1.0)
- Order status agent (A2A 0.3.0)

## MCP server

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

## LLM provider

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

## Connection

Where and how the gateway reaches an agent, MCP server or LLM: URL, authentication and policies.

**When to use it:** One per upstream. Change URLs per environment with variables.

**Examples and details:**

- ${refundAgent.url} with PII detection inbound
- openai_connection with apiKey ${openai.apiKey}
- MCP connection URL = server base without /mcp; Test connection calls exactly what the runtime calls

<figure markdown>
![Context edges between a broker and its agents](../assets/ui/network-v2-context-light.webp#only-light){ loading=lazy }
![Context edges between a broker and its agents](../assets/ui/network-v2-context-dark.webp#only-dark){ loading=lazy }
<figcaption>Context edges between a broker and its agents</figcaption>
</figure>

## Policy

<div class="grid" markdown>

![card-policy](../assets/ui/card-policy-light.webp#only-light){ loading=lazy }
![card-policy](../assets/ui/card-policy-dark.webp#only-dark){ loading=lazy }

An Agent Fabric gateway policy applied to a connection or broker interface: every MuleSoft-provided policy Anypoint offers on an Agent Fabric instance (Basic Authentication, Client ID Enforcement, JWT Validation, IP Allowlist, CORS, rate limiting, PII detection, header injection, schema validation, prompt decoration, …), your organization's own policies and P4A policies.

**When to use it:** Governance: protect upstreams, mask personal data, add headers, enforce limits. Add policy lists every policy for every component; switch to "Only for brokers" (or A2A agents, MCP servers, LLMs) to narrow it. Each applied policy collapses to its title with its chevron; with two or more they start collapsed, and Collapse all / Expand all is in the Policies header.

</div>

**Examples and details:**

- On a v2 canvas the Context card (context.policies and connections without an owner) sits left of the brokers; its orange Context port connects to each broker's Context row
- http-basic-authentication (Basic Authentication - Simple) on the broker
- rate-limiting 30 requests/min on the broker
- mcp-pii-detector "Log and mask" on an MCP connection
- a-two-a-prompt-decorator to add answer rules
