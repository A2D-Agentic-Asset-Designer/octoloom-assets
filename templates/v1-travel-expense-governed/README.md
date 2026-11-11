# Travel & Expense (governed)

Five specialist agents and four travel and finance tool servers plan trips and settle expenses.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Travel Booking Agent (A2A 0.3.0, MuleSoft), Policy Advisor Agent (A2A 0.3.0, AgentForce), Visa Agent (A2A 0.3.0, Bedrock), Expense Audit Agent (A2A 0.3.0, OpenAI), Reimbursement Agent (A2A 0.3.0, Snowflake)
- MCP servers: Flights MCP (search_flights); Hotels MCP (search_hotels); Expense MCP (create_expense_report); Currency MCP (convert_currency)
- Policies (Agent Fabric built-ins): rate-limiting, mcp-pii-detector, mcp-schema-validation, header-injection, a-two-a-pii-detector, a-two-a-prompt-decorator. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time and `ingressgw.url` to your ingress gateway URL. No credentials are stored in this template.

## Try it

- Book a trip from Zurich to London for 2026-12-02 to 2026-12-04
- Do I need a visa for India?
- Submit my hotel bill of 420 GBP for reimbursement
