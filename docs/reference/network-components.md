# Network components

The cards of the network canvas (`agent-network.yaml`).

## Broker

The agent your users call. In 1.0 it is an LLM with instructions, linked agents and MCP tools. In 2.0 it is an AgentScript flow with an A2A interface.

**When to use it:** One per entry point. Split brokers by audience or domain.

**Examples:**

- Customer service front door
- Returns flow with eligibility gate
- IT helpdesk triage
- Kind and Implementation (.agent) of a 2.0 broker are in Protected broker settings, locked like the protected exchange.json defaults: click the lock icon to change them; the YAML always edits everything
- Removing a 2.0 broker asks whether to delete its .agent flow file too (it goes to the Trash; a file another broker uses is never offered)
- A 2.0 flow needs at least a trigger, one agent node (generator, subagent or orchestrator) and a reply (echo): delete anything else and the build still passes

## Agent

A remote A2A agent described by its agent card (skills, URL, protocol version). Brokers call it through a connection.

**When to use it:** A capability already exists as an agent (Agentforce, A2D mock, custom).

**Examples:**

- Refund agent (A2A 1.0)
- Order status agent (A2A 0.3.0)

## MCP server

A Model Context Protocol server with tools. Brokers may call only the tools you allow. Its connection URL is the server base: the runtime adds metadata.transport.path (for example /mcp).

**When to use it:** Deterministic system access: look up, create, update records.

**Examples:**

- orders_mcp: check_return_eligibility, create_rma
- crm_mcp: find_customer
- URL https://host/product-mcp/ + path /mcp → the runtime calls https://host/product-mcp/mcp (a URL ending with /mcp would call /mcp/mcp)

## LLM provider

The model provider and models brokers may use. The key comes from a connection secret at deploy time. A dashed icon tile means the LLM is referenced from Exchange (an exchange.json dependency, classifier llm-metadata), not declared in this project; its Platform and Models are read-only on the card.

**When to use it:** Every network that has a 1.0 broker or AgentScript LLM nodes.

**Examples:**

- OpenAI gpt-5-mini
- Azure OpenAI deployment
- Dashed tile: MuleSoft openai from Exchange, shared by every project that references it

## Connection

Where and how the gateway reaches an agent, MCP server or LLM: URL, authentication and policies.

**When to use it:** One per upstream. Change URLs per environment with variables.

**Examples:**

- ${refundAgent.url} with PII detection inbound
- openai_connection with apiKey ${openai.apiKey}
- MCP connection URL = server base without /mcp; Test connection calls exactly what the runtime calls

## Policy

An Agent Fabric gateway policy applied to a connection or broker interface: every MuleSoft-provided policy Anypoint offers on an Agent Fabric instance (Basic Authentication, Client ID Enforcement, JWT Validation, IP Allowlist, CORS, rate limiting, PII detection, header injection, schema validation, prompt decoration, …), your organization's own policies and P4A policies.

**When to use it:** Governance: protect upstreams, mask personal data, add headers, enforce limits. Add policy lists every policy for every component; switch to "Only for brokers" (or A2A agents, MCP servers, LLMs) to narrow it. Each applied policy collapses to its title with its chevron; with two or more they start collapsed, and Collapse all / Expand all is in the Policies header.

**Examples:**

- On a v2 canvas the Context card (context.policies and connections without an owner) sits left of the brokers; its orange Context port connects to each broker's Context row
- http-basic-authentication (Basic Authentication - Simple) on the broker
- rate-limiting 30 requests/min on the broker
- mcp-pii-detector "Log and mask" on an MCP connection
- a-two-a-prompt-decorator to add answer rules
