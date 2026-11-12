# KYC / AML Onboarding (governed)

New banking customers are screened (document, sanctions, risk score); low risk opens the account, medium goes to an analyst, high opens a compliance case.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: KYC Analyst Agent (A2A 1.0, Azure), Account Opening Agent (A2A 0.3.0, AgentForce)
- MCP servers: Identity Verification MCP (verify_document); Sanctions Screening MCP (screen_name); Customer Risk MCP (score_customer, open_case)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time. No credentials are stored in this template.

## Try it

- Onboard applicant AP-7001, Lena Novak, from Austria
- Onboard applicant AP-7003, Victor Example, from Panama
