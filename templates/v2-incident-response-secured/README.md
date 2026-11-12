# IT Incident Response (secured)

Alerts are classified; P1s become a major incident with on-call page and status page, others go to the network, database or application specialist.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Incident Triage Agent (A2A 1.0, AgentForce), Network Operations Agent (A2A 0.3.0, MuleSoft), Database Operations Agent (A2A 1.0, Snowflake), Application Support Agent (A2A 0.3.0, Azure), Status Page Agent (A2A 1.0, Vertex)
- MCP servers: Service Health Monitoring MCP (get_service_health); Incident Ticketing MCP (create_incident, page_oncall)
- Secured: every agent and MCP connection authenticates (Basic or Client ID enforcement, alternating). User names and client ids are variables, passwords and client secrets are secret variables asked for at deploy time. The LLM URL is the variable `llmGateway.url` (api.openai.com by default, or your LLM gateway). Upstream calls are logged with the outbound Message Logging policy. Policies: message-logging-outbound, rate-limiting.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time. No credentials are stored in this template.

## Try it

- P1: checkout-api returns 500 for all users since 10:02
- orders-db replication lag is 40 minutes
- VPN in the Zurich office drops every few minutes
