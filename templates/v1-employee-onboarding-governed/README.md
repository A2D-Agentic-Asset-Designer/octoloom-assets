# Employee Onboarding (governed)

HR, IT and facilities agents plus directory and learning tools prepare a new hire for day one.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: HR Records Agent (A2A 0.3.0, AgentForce), IT Provisioning Agent (A2A 0.3.0, Azure), Facilities Agent (A2A 0.3.0, MuleSoft)
- MCP servers: Identity Directory MCP (lookup_employee, create_account); Learning MCP (list_courses, assign_training)
- Policies (Agent Fabric built-ins): rate-limiting, mcp-pii-detector, mcp-schema-validation, header-injection, a-two-a-pii-detector, a-two-a-prompt-decorator. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **Onboard employee E-1001 who starts Monday as a Sales Engineer**
  - You should see: Identity Directory `lookup_employee` finds Jane Rivera (Sales Engineer, Lausanne, starts 2026-11-16). HR Records sends contract CT-2026-118, IT Provisioning orders laptop LT-5531 and `create_account` creates the account, Facilities books desk LS-3-14 and badge B-77812.
- **Assign the onboarding training to E-1001**
  - You should see: Learning MCP `list_courses` and `assign_training`: 3 courses assigned, due 2026-12-15.
- **What is still open for the onboarding of E-1002?**
  - You should see: Omar Haddad (Data Analyst, Remote). The broker asks the agents for the open items (contract, laptop, account, badge) and lists them.
- **My email is jane.doe@example.com and my phone is +41 79 123 45 67. Onboard employee E-1001 who starts Monday as a Sales Engineer**
  - You should see: Same answer as the first prompt. The PII detector policies log the email and phone number; on the MCP connections with the MCP PII detector they are masked before the tool sees them. Check the policy logs in Anypoint Monitoring.
- **Send the first prompt more than 30 times within a minute**
  - You should see: The broker answers HTTP 429 (Too Many Requests) once the rate limit of 60 requests per minute is reached.

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.
