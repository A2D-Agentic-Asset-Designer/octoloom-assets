# IT Incident Response

Alerts are classified; P1s become a major incident with on-call page and status page, others go to the network, database or application specialist.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Incident Triage Agent (A2A 1.0, AgentForce), Network Operations Agent (A2A 0.3.0, MuleSoft), Database Operations Agent (A2A 1.0, Snowflake), Application Support Agent (A2A 0.3.0, Azure), Status Page Agent (A2A 1.0, Vertex)
- MCP servers: Service Health Monitoring MCP (get_service_health); Incident Ticketing MCP (create_incident, page_oncall)

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **P1: checkout-api returns 500 for all users since 10:02**
  - You should see: Triage, Monitoring `get_service_health`, Ticketing `create_incident` INC-50211 and `page_oncall` (Dana Example). Triage blames deploy 2026.11.12-3, Application Support rolls back to 2026.11.12-2, Status Page posts update ST-818.
- **orders-db replication lag is 40 minutes**
  - You should see: Routed to the Database Operations Agent: batch job BJ-4410 is throttled, lag below 1 minute in 15 minutes.
- **VPN in the Zurich office drops every few minutes**
  - You should see: Routed to the Network Operations Agent: vpn-zrh-2 flaps because of an expiring certificate; failover to vpn-zrh-1, renewal at 14:00.

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.
