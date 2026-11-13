# Field Service Dispatch (governed)

Diagnose an equipment fault, check parts and weather, and dispatch or resolve remotely.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Dispatch Agent (A2A 1.0, ServiceNow), Parts Logistics Agent (A2A 0.3.0, MuleSoft), Customer Communications Agent (A2A 1.0, AgentForce)
- MCP servers: Asset Registry MCP (get_asset); Diagnostics MCP (run_diagnostics); Parts Inventory MCP (check_stock); Weather MCP (get_forecast)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **Heat pump HP-301 shows error E42**
  - You should see: Asset Registry `get_asset`, Diagnostics `run_diagnostics` needs a visit. Parts Inventory `check_stock`: CMP-42 from Bern. Weather `get_forecast`: Vevey OK. Parts Logistics reserves it, Dispatch books technician T-14 (Marco) tomorrow 08:00-10:00, Customer Communications confirms.
- **Solar inverter INV-77 is offline**
  - You should see: Diagnostics `run_diagnostics`: lost connectivity, fixed with a remote reboot. Customer Communications informs the customer; no visit.
- **My email is jane.doe@example.com and my phone is +41 79 123 45 67. Heat pump HP-301 shows error E42**
  - You should see: Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring.
- **Send the first prompt more than 30 times within a minute**
  - You should see: The broker answers HTTP 429 (Too Many Requests) once the rate limit of 30 requests per minute is reached.

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.
