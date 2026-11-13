# Customer Service Broker

One front door for orders, returns, billing and loyalty questions, backed by a CRM tool server.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Order Status Agent (A2A 0.3.0, MuleSoft), Returns Agent (A2A 0.3.0, AgentForce), Billing Agent (A2A 0.3.0, Bedrock), Loyalty Agent (A2A 0.3.0, Vertex)
- MCP servers: CRM MCP (get_customer, create_case, list_cases)

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **Where is order SO-9001 for customer C-2001?**
  - You should see: CRM `get_customer` finds Lena Fischer (Gold). Order Status Agent: SO-9001 shipped with DHL, ETA 2026-11-12.
- **I want to return the shoes from order SO-9002**
  - You should see: Order Status Agent: SO-9002 is delivered. Returns Agent opens return RMA-4410.
- **Why was I charged twice on invoice INV-7781? I am C-2001**
  - You should see: Billing Agent: invoice INV-7781 has one charge and one pre-authorisation, released within 3 days. The broker may log CRM case CS-30551 with `create_case`.
- **How many points do I have? I am C-2001. Redeem them for a voucher**
  - You should see: Loyalty Agent: 1,840 points, Gold tier until 2027-03-31. Redeeming 500 points gives voucher VC-5050 (10 EUR), 1,340 points left.
- **Exchange the shoes from SO-9002 for a bigger size**
  - You should see: Returns Agent: exchange EX-118, size 42 replaces size 41.

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.
