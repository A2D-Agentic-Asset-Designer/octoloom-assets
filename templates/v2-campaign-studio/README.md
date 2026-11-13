# Marketing Campaign Studio

A tool-heavy deterministic flow: two agents and four marketing tool servers build and launch a campaign.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Content Agent (A2A 1.0, OpenAI), Marketing Compliance Agent (A2A 0.3.0, Anthropic)
- MCP servers: Audience Segments MCP (get_segment); Brand Assets MCP (find_assets); Email MCP (schedule_email); Analytics MCP (forecast)

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

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.
