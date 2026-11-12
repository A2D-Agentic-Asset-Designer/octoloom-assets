# HR Leave Requests (governed)

Employees ask for time off; the broker checks balance, policy and team calendar before submitting the request.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Leave Policy Agent (A2A 0.3.0, AgentForce), Payroll Agent (A2A 0.3.0, Azure)
- MCP servers: HRIS MCP (get_leave_balance, submit_leave_request); Team Calendar MCP (check_team_calendar)
- Policies (Agent Fabric built-ins): rate-limiting, mcp-pii-detector, mcp-schema-validation, header-injection, a-two-a-pii-detector, a-two-a-prompt-decorator. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time and `ingressgw.url` to your ingress gateway URL. No credentials are stored in this template.

## Try it

- E-3001 wants vacation from 2026-12-21 to 2026-12-31
- Can E-3002 take 3 days of unpaid leave next week?
