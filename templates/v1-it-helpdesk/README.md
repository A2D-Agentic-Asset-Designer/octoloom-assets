# IT Helpdesk

Triage and access agents work with ITSM, monitoring and knowledge-base tools to resolve tickets.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: IT Triage Agent (A2A 0.3.0, OpenAI), Access Request Agent (A2A 0.3.0, ServiceNow), Device Support Agent (A2A 0.3.0, MuleSoft)
- MCP servers: ITSM MCP (create_incident, get_incident); Monitoring MCP (get_service_health); Knowledge Base MCP (search_articles)

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **VPN is not connecting since this morning**
  - You should see: IT Triage classifies it as Network/VPN P3. Monitoring `get_service_health`: vpn degraded (outage OUT-552). Knowledge Base `search_articles` returns KB-1201.
- **I need access to the finance SharePoint**
  - You should see: Access Request Agent opens access request AR-7781.
- **My laptop screen flickers**
  - You should see: Knowledge Base returns KB-2210. Device Support pushes a display driver update and books swap SW-3310 for tomorrow 10:00 if it still flickers.
- **P1: nobody can log in to email. Open an incident**
  - You should see: ITSM `create_incident` creates INC-90001.
- **What is the status of INC-90017?**
  - You should see: ITSM `get_incident`: in progress, assigned to Alex Kim.

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.
