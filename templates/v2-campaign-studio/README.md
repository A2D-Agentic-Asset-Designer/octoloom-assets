# Marketing Campaign Studio

A tool-heavy deterministic flow: two agents and four marketing tool servers build and launch a campaign.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Content Agent (A2A 1.0, OpenAI), Marketing Compliance Agent (A2A 0.3.0, Anthropic)
- MCP servers: Audience Segments MCP (get_segment); Brand Assets MCP (find_assets); Email MCP (schedule_email); Analytics MCP (forecast)

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time. No credentials are stored in this template.

## Try it

- Launch a winter email campaign for segment SEG-VIP
- Plan a social post about our new eco line for SEG-ECO
