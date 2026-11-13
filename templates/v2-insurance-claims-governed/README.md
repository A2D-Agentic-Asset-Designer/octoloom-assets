# Insurance Claims (FNOL to Payout) (governed)

Classify a claim, check coverage, gate on fraud risk, then settle through adjuster and payment agents.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: FNOL Intake Agent (A2A 1.0, AgentForce), Fraud Screening Agent (A2A 0.3.0, Databricks), Claims Adjuster Agent (A2A 1.0, MuleSoft), Claims Payments Agent (A2A 0.3.0, Bedrock)
- MCP servers: Policy Admin MCP (check_coverage); Claims MCP (create_claim, refer_to_siu)
- Policies (Agent Fabric built-ins): a2a-v1-pii-detector, header-injection, mcp-pii-detector, mcp-schema-validation, rate-limiting. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **My car was hit in a parking lot, policy POL-5001**
  - You should see: FNOL takes the claim, Policy Admin `check_coverage` confirms motor cover, Claims `create_claim`, creates CLM-30017, Fraud: low (12), Adjuster proposes 1,980 CHF (2,480 minus 500 deductible) and Payments releases PAY-77120.
- **Water damage in the kitchen, policy POL-5002, about 18,000 CHF**
  - You should see: Fraud risk high (82): new policy and amount above 10,000 CHF. Claims `refer_to_siu` opens SIU-0091 (investigator R. Meier). No payment.
- **Storm damage on my roof, policy POL-5003**
  - You should see: Policy Admin: the policy lapsed. The flow ends in the not-covered branch.
- **My email is jane.doe@example.com and my phone is +41 79 123 45 67. My car was hit in a parking lot, policy POL-5001**
  - You should see: Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring.
- **Send the first prompt more than 30 times within a minute**
  - You should see: The broker answers HTTP 429 (Too Many Requests) once the rate limit of 30 requests per minute is reached.

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.
