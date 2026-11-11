# Procurement Assistant

A tool-heavy broker: two agents and five procurement tool servers turn requests into purchase orders.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Supplier Risk Agent (A2A 0.3.0, Databricks), Sourcing Agent (A2A 0.3.0, LangChain)
- MCP servers: Catalog MCP (search_catalog); Budget MCP (check_budget); Supplier Registry MCP (get_supplier); Contracts MCP (find_contract); Purchase Orders MCP (create_purchase_order)

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time and `ingressgw.url` to your ingress gateway URL. No credentials are stored in this template.

## Try it

- Order 5 monitors for cost centre CC-410
- Is supplier SUP-88 approved?
