# Marketing Campaign Studio (governed)

A tool-heavy deterministic flow: two agents and four marketing tool servers build and launch a campaign.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Content Agent (A2A 1.0, OpenAI), Marketing Compliance Agent (A2A 0.3.0, Anthropic)
- MCP servers: Audience Segments MCP (get_segment); Brand Assets MCP (find_assets); Email MCP (schedule_email); Analytics MCP (forecast)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **Launch a winter email campaign for segment SEG-VIP**
  - You should see: Audience Segments `get_segment`, Brand Assets `find_assets`, Content drafts, Marketing Compliance approves. Email `schedule_email` schedules EM-2026-311 for 2026-11-14 08:00 UTC, Analytics `forecast`: 41% open rate, 86,000 CHF expected revenue.
- **Plan a social post about our new eco line for SEG-ECO**
  - You should see: Compliance approves with a change: "carbon neutral" becomes "lower-impact materials". The flow ends in the social-ready branch.
- **Send an email about the eco line to SEG-ECO**
  - You should see: SEG-ECO has 0 email-consented contacts: the campaign is returned, nothing is scheduled.
- **My email is jane.doe@example.com and my phone is +41 79 123 45 67. Launch a winter email campaign for segment SEG-VIP**
  - You should see: Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring.
- **Send the first prompt more than 30 times within a minute**
  - You should see: The broker answers HTTP 429 (Too Many Requests) once the rate limit of 30 requests per minute is reached.

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.
