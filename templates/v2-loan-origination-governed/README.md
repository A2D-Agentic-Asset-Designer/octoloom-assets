# Loan Origination (governed)

Five agents (A2A 1.0 and 0.3.0) and three banking tool servers take a loan from application to decision.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Loan Intake Agent (A2A 1.0, AgentForce), KYC Agent (A2A 1.0, Azure), Credit Analysis Agent (A2A 0.3.0, Snowflake), Underwriting Agent (A2A 0.3.0, MuleSoft), Customer Notification Agent (A2A 1.0, Vertex)
- MCP servers: Credit Bureau MCP (get_credit_score); Core Banking MCP (get_accounts, book_loan); Documents MCP (generate_contract)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, a-two-a-pii-detector, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **Applicant APP-100 asks for a 25,000 CHF personal loan**
  - You should see: Intake, KYC, Credit Bureau `get_credit_score` and Credit Analysis approve. Core Banking `book_loan` books LN-2026-0100 at 4.9%, Documents `generate_contract` creates DOC-77100, Customer Notification informs the applicant.
- **Applicant APP-200 wants 300,000 CHF for a mortgage**
  - You should see: Bureau score 655, debt-to-income 41%: the assessment refers it. Underwriting approves 260,000 CHF with a 20% equity condition.
- **My email is jane.doe@example.com and my phone is +41 79 123 45 67. Applicant APP-100 asks for a 25,000 CHF personal loan**
  - You should see: Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring.
- **Send the first prompt more than 30 times within a minute**
  - You should see: The broker answers HTTP 429 (Too Many Requests) once the rate limit of 30 requests per minute is reached.

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.
