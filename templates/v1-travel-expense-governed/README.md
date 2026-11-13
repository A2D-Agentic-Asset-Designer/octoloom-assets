# Travel & Expense (governed)

Five specialist agents and four travel and finance tool servers plan trips and settle expenses.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Travel Booking Agent (A2A 0.3.0, MuleSoft), Policy Advisor Agent (A2A 0.3.0, AgentForce), Visa Agent (A2A 0.3.0, Bedrock), Expense Audit Agent (A2A 0.3.0, OpenAI), Reimbursement Agent (A2A 0.3.0, Snowflake)
- MCP servers: Flights MCP (search_flights); Hotels MCP (search_hotels); Expense MCP (create_expense_report); Currency MCP (convert_currency)
- Policies (Agent Fabric built-ins): rate-limiting, mcp-pii-detector, mcp-schema-validation, header-injection, a-two-a-pii-detector, a-two-a-prompt-decorator. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **Book a trip from Zurich to London for 2026-12-02 to 2026-12-04**
  - You should see: Flights `search_flights`: LX318, 212 CHF. Hotels `search_hotels`: Thames Bridge, 210 GBP. Policy Advisor checks the hotel limit (220 GBP per night). Travel Booking books LX318 (PNR K7Q2ZP) and the hotel (H-55120).
- **Can I fly business class to London?**
  - You should see: Policy Advisor: business class only for flights over 6 hours, so economy.
- **Do I need a visa for India? And for the UK?**
  - You should see: Visa Agent: India needs an e-Business visa (apply 4 days ahead); the UK needs no visa but an ETA.
- **Submit my hotel bill of 420 GBP for reimbursement**
  - You should see: Expense Audit approves the hotel (2 nights at 210 GBP, within the limit). Currency `convert_currency`: 1.1483, 482.30 CHF. Expense `create_expense_report` creates ER-6610; Reimbursement schedules RB-8812 for 2026-11-25.
- **My email is jane.doe@example.com and my phone is +41 79 123 45 67. Book a trip from Zurich to London for 2026-12-02 to 2026-12-04**
  - You should see: Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring.
- **Send the first prompt more than 30 times within a minute**
  - You should see: The broker answers HTTP 429 (Too Many Requests) once the rate limit of 60 requests per minute is reached.

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.
