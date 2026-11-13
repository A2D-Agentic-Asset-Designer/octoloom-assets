# Retail Returns

The smallest deterministic flow: extract the order, check eligibility, create the RMA and refund.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Returns Desk Agent (A2A 1.0, AgentForce), Refund Agent (A2A 0.3.0, MuleSoft)
- MCP servers: Orders MCP (check_return_eligibility, create_rma)

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **I want to return order ORD-1001, the jacket is too small**
  - You should see: Orders `check_return_eligibility`: eligible. `create_rma` creates RMA-88001, Refund Agent refunds RF-1001, 129 CHF.
- **Return ORD-1002 please**
  - You should see: Delivered 47 days ago, outside the 30-day window: declined. Returns Desk offers a 15% voucher (VC-RET-15) or a repair.
- **Return ORD-9999**
  - You should see: The order is not found, so it is not eligible: the flow takes the decline branch, no RMA.

The broker is deterministic: the branches are fixed in the flow in `brokers/` (open the `.agent` file to see them). The LLM only reads the ids from your prompt and writes the reply text, so the same input takes the same branch.
