# Procurement Assistant (governed)

A tool-heavy broker: two agents and five procurement tool servers turn requests into purchase orders.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Supplier Risk Agent (A2A 0.3.0, Databricks), Sourcing Agent (A2A 0.3.0, LangChain)
- MCP servers: Catalog MCP (search_catalog); Budget MCP (check_budget); Supplier Registry MCP (get_supplier); Contracts MCP (find_contract); Purchase Orders MCP (create_purchase_order)
- Policies (Agent Fabric built-ins): rate-limiting, mcp-pii-detector, mcp-schema-validation, header-injection, a-two-a-pii-detector, a-two-a-prompt-decorator. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **Order 5 monitors for cost centre CC-410**
  - You should see: Catalog `search_catalog`: MON-27A, 349 CHF from SUP-88. Budget `check_budget`: CC-410 has 5,200 left. Supplier Risk: SUP-88 approved (risk 23). Contracts `find_contract`: FC-2026-04 (12% off). Purchase Orders `create_purchase_order`: PO-450021, 1,535.60.
- **Is supplier SUP-88 approved? And SUP-91?**
  - You should see: Supplier Registry `get_supplier` and Supplier Risk: SUP-88 approved (risk 23), SUP-91 not approved (risk 71).
- **Order 5 monitors for cost centre CC-999**
  - You should see: Budget `check_budget`: CC-999 has only 120 left, so no purchase order is created.
- **Find an alternative to MON-27A**
  - You should see: Sourcing Agent: 27" QHD monitor MON-27B from SUP-88 at 219 CHF (contract FC-2026-04).
- **My email is jane.doe@example.com and my phone is +41 79 123 45 67. Order 5 monitors for cost centre CC-410**
  - You should see: Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring.
- **Send the first prompt more than 30 times within a minute**
  - You should see: The broker answers HTTP 429 (Too Many Requests) once the rate limit of 60 requests per minute is reached.

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.
