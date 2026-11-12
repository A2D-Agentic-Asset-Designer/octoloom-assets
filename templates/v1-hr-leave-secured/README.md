# HR Leave Requests (secured)

Employees ask for time off; the broker checks balance, policy and team calendar before submitting the request.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Leave Policy Agent (A2A 0.3.0, AgentForce), Payroll Agent (A2A 0.3.0, Azure)
- MCP servers: HRIS MCP (get_leave_balance, submit_leave_request); Team Calendar MCP (check_team_calendar)
- Secured: every agent and MCP connection authenticates (Basic or Client ID enforcement, alternating). User names and client ids are variables, passwords and client secrets are secret variables asked for at deploy time. The LLM URL is the variable `llmGateway.url` (api.openai.com by default, or your LLM gateway). Policies: rate-limiting.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time and `ingressgw.url` to your ingress gateway URL. No credentials are stored in this template.

## Try it

- E-3001 wants vacation from 2026-12-21 to 2026-12-31
- Can E-3002 take 3 days of unpaid leave next week?
