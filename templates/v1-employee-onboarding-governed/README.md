# Employee Onboarding (governed)

HR, IT and facilities agents plus directory and learning tools prepare a new hire for day one.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: HR Records Agent (A2A 0.3.0, AgentForce), IT Provisioning Agent (A2A 0.3.0, Azure), Facilities Agent (A2A 0.3.0, MuleSoft)
- MCP servers: Identity Directory MCP (lookup_employee, create_account); Learning MCP (list_courses, assign_training)
- Policies (Agent Fabric built-ins): rate-limiting, mcp-pii-detector, mcp-schema-validation, header-injection, a-two-a-pii-detector, a-two-a-prompt-decorator. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time and `ingressgw.url` to your ingress gateway URL. No credentials are stored in this template.

## Try it

- Onboard employee E-1001 who starts Monday as a Sales Engineer
- What is still open for the onboarding of E-1002?
