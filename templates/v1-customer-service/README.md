# Customer Service Broker

One front door for orders, returns, billing and loyalty questions, backed by a CRM tool server.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Order Status Agent (A2A 0.3.0, MuleSoft), Returns Agent (A2A 0.3.0, AgentForce), Billing Agent (A2A 0.3.0, Bedrock), Loyalty Agent (A2A 0.3.0, Vertex)
- MCP servers: CRM MCP (get_customer, create_case, list_cases)

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time and `ingressgw.url` to your ingress gateway URL. No credentials are stored in this template.

## Try it

- Where is order SO-9001 for customer C-2001?
- I want to return the shoes from order SO-9002
- How many points do I have? I am C-2001
