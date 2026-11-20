# Library Services (fully mocked)

A library broker answers member, loan, catalog and event questions with two agents and three tool servers. Fully mocked: the LLM is an A²D LLM mock too, so no OpenAI key is needed.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Holds Agent (A2A 0.3.0, Azure), Events Agent (A2A 0.3.0, AgentForce)
- MCP servers: Members MCP (get_member); Loans MCP (get_loans); Library Catalog MCP (search_books)

Fully mocked: the agents, the MCP servers **and the LLM** are public A2D mocks, so the network runs without an OpenAI key or any other system. The LLM mock answers the prompts below with scripted tool calls and replies; any other prompt gets a short hint. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `a2dLlm.apiKey`: the A²D LLM mock key: keep the default, any value works
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **Tracer** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **Which loans does member M-310 have?**
  - You should see: Members MCP `get_member` (Ines Moreau) and Loans MCP `get_loans`: The Left Hand of Darkness (due 2026-11-27) and Piranesi (due 2026-12-02).
- **Place a hold on Dune for member M-310**
  - You should see: Library Catalog MCP `search_books`: all 3 copies on loan, next return 2026-11-25. The Holds Agent places hold H-9120 (position 1).
- **Which workshops are on next week?**
  - You should see: The Events Agent lists Intro to 3D printing (Tuesday 18:00) and Family coding club (Saturday 10:00).

The LLM is an A²D LLM mock: it answers the prompts above with the same tool calls and replies every time (the broker is probabilistic, but its LLM is scripted). Swap `a2dLlm.url` for a real OpenAI-compatible endpoint to let a real model drive it.
