# Supply Chain Disruption (governed)

A late or short shipment is assessed against stock; severe delays are rerouted and customers told, other cases get a mitigation plan.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Supplier Risk Agent (A2A 1.0, Snowflake), Logistics Agent (A2A 0.3.0, MuleSoft), Procurement Buyer Agent (A2A 1.0, AgentForce), Customer Communications Agent (A2A 0.3.0, Vertex)
- MCP servers: Shipments MCP (get_shipment, reroute_shipment); Inventory MCP (get_stock); Supplier MCP (find_alternative_supplier)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time. No credentials are stored in this template.

## Try it

- Shipment SHP-4401 with SKU-778 is delayed 9 days at the port
- Supplier reports a shortage of SKU-912 for shipment SHP-4402
