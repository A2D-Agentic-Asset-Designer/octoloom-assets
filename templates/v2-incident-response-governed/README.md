# IT Incident Response (governed)

Alerts are classified; P1s become a major incident with on-call page and status page, others go to the network, database or application specialist.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Incident Triage Agent (A2A 1.0, AgentForce), Network Operations Agent (A2A 0.3.0, MuleSoft), Database Operations Agent (A2A 1.0, Snowflake), Application Support Agent (A2A 0.3.0, Azure), Status Page Agent (A2A 1.0, Vertex)
- MCP servers: Service Health Monitoring MCP (get_service_health); Incident Ticketing MCP (create_incident, page_oncall)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time. No credentials are stored in this template.

## Try it

- P1: checkout-api returns 500 for all users since 10:02
- orders-db replication lag is 40 minutes
- VPN in the Zurich office drops every few minutes
