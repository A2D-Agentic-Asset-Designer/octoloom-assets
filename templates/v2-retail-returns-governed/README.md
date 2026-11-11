# Retail Returns (governed)

The smallest deterministic flow: extract the order, check eligibility, create the RMA and refund.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Returns Desk Agent (A2A 1.0, AgentForce), Refund Agent (A2A 0.3.0, MuleSoft)
- MCP servers: Orders MCP (check_return_eligibility, create_rma)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time. No credentials are stored in this template.

## Try it

- I want to return order ORD-1001, the jacket is too small
- Return ORD-1002 please
