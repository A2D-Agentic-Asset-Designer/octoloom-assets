# Loan Origination

Five agents (A2A 1.0 and 0.3.0) and three banking tool servers take a loan from application to decision.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Loan Intake Agent (A2A 1.0, AgentForce), KYC Agent (A2A 1.0, Azure), Credit Analysis Agent (A2A 0.3.0, Snowflake), Underwriting Agent (A2A 0.3.0, MuleSoft), Customer Notification Agent (A2A 1.0, Vertex)
- MCP servers: Credit Bureau MCP (get_credit_score); Core Banking MCP (get_accounts, book_loan); Documents MCP (generate_contract)

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

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.
