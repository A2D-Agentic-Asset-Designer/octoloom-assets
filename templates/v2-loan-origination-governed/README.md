# Loan Origination (governed)

Five agents (A2A 1.0 and 0.3.0) and three banking tool servers take a loan from application to decision.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Loan Intake Agent (A2A 1.0, AgentForce), KYC Agent (A2A 1.0, Azure), Credit Analysis Agent (A2A 0.3.0, Snowflake), Underwriting Agent (A2A 0.3.0, MuleSoft), Customer Notification Agent (A2A 1.0, Vertex)
- MCP servers: Credit Bureau MCP (get_credit_score); Core Banking MCP (get_accounts, book_loan); Documents MCP (generate_contract)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, a-two-a-pii-detector, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time. No credentials are stored in this template.

## Try it

- Applicant APP-100 asks for a 25,000 CHF personal loan
- Applicant APP-200 wants 300,000 CHF for a mortgage
