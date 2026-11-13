# HR Leave Requests (secured)

Employees ask for time off; the broker checks balance, policy and team calendar before submitting the request.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Leave Policy Agent (A2A 0.3.0, AgentForce), Payroll Agent (A2A 0.3.0, Azure)
- MCP servers: HRIS MCP (get_leave_balance, submit_leave_request); Team Calendar MCP (check_team_calendar)
- Secured: every agent and MCP connection authenticates (Basic or Client ID enforcement, alternating). User names and client ids are variables, passwords and client secrets are secret variables asked for at deploy time. The LLM URL is the variable `llmGateway.url` (api.openai.com by default, or your LLM gateway). Policies: rate-limiting.

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
   - `hrisMcp.clientSecret`: Client secret (any value works with the A²D mocks)
   - `calendarMcp.password`: Password (any value works with the A²D mocks)
   - `leavePolicyAgent.password`: Password (any value works with the A²D mocks)
   - `payrollAgent.clientSecret`: Client secret (any value works with the A²D mocks)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **E-3001 wants vacation from 2026-12-21 to 2026-12-31**
  - You should see: HRIS `get_leave_balance`: Mia Keller has 14 days left. Team Calendar `check_team_calendar` (team M-410): Noah Weber is away 2026-12-22 to 2027-01-02. Leave Policy: allowed, outside the year-end freeze. `submit_leave_request` creates LR-7701, pending approval by M-410.
- **Can E-3002 take 3 days of unpaid leave next week?**
  - You should see: Luca Rossi has 1 vacation day left and used 2 unpaid days. Leave Policy: up to 5 unpaid days a year with manager approval. Payroll: the next payslip drops by 742.50 CHF gross. A request creates LR-7702.
- **Who in team M-410 is away over Christmas?**
  - You should see: Team Calendar: Noah Weber, 2026-12-22 to 2027-01-02.
- **E-3001 wants vacation from 2026-12-21 to 2026-12-31**
  - You should see: Same answer as the plain variant: the A²D mocks accept any credentials. The Tracer shows each authenticated upstream call.

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.
