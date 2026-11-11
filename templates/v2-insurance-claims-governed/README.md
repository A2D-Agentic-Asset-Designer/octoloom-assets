# Insurance Claims (FNOL to Payout) (governed)

Classify a claim, check coverage, gate on fraud risk, then settle through adjuster and payment agents.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: FNOL Intake Agent (A2A 1.0, AgentForce), Fraud Screening Agent (A2A 0.3.0, Databricks), Claims Adjuster Agent (A2A 1.0, MuleSoft), Claims Payments Agent (A2A 0.3.0, Bedrock)
- MCP servers: Policy Admin MCP (check_coverage); Claims MCP (create_claim, refer_to_siu)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time. No credentials are stored in this template.

## Try it

- My car was hit in a parking lot, policy POL-5001
- Water damage in the kitchen, policy POL-5002, about 18,000 CHF
