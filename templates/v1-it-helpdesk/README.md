# IT Helpdesk

Triage and access agents work with ITSM, monitoring and knowledge-base tools to resolve tickets.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: IT Triage Agent (A2A 0.3.0, OpenAI), Access Request Agent (A2A 0.3.0, ServiceNow), Device Support Agent (A2A 0.3.0, MuleSoft)
- MCP servers: ITSM MCP (create_incident, get_incident); Monitoring MCP (get_service_health); Knowledge Base MCP (search_articles)

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time and `ingressgw.url` to your ingress gateway URL. No credentials are stored in this template.

## Try it

- VPN is not connecting since this morning
- I need access to the finance SharePoint
- My laptop screen flickers
