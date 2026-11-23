# Warranty Repair (fully mocked)

Check the device warranty: covered repairs are booked and confirmed, the others get a quote. Three agents, one tool server. Fully mocked: the LLM is an A²D LLM mock too, so no OpenAI key is needed.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Repair Agent (A2A 0.3.0, MuleSoft), Notification Agent (A2A 1.0, Vertex), Quote Agent (A2A 1.0, AgentForce)
- MCP servers: Device Registry MCP (check_warranty)

Fully mocked: the agents, the MCP servers **and the LLM** are public A2D mocks, so the network runs without an OpenAI key or any other system. The LLM mock answers the prompts below with scripted tool calls and replies; any other prompt gets a short hint. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `a2dLlm.apiKey`: the A²D LLM mock key: keep the default, any value works
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **Tracer** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **My laptop SN-1001 has a flickering screen**
  - You should see: Warranty Gate: covered until 2027-05-31. The Repair Agent books RP-1001 with courier pickup, the Notification Agent confirms it by SMS and email.
- **SN-2002 has a swollen battery**
  - You should see: Warranty Gate: expired on 2026-03-01. The Quote Agent sends QT-2002 (89.00 CHF, 3 working days).

The LLM is an A²D LLM mock: it answers the prompts above with the same tool calls and replies every time (the flow in `brokers/` decides the branches, the mock fills in the LLM steps). Swap `a2dLlm.url` for a real OpenAI-compatible endpoint to let a real model drive it.

**Live progress** (the antenna button next to Send) is on by default: while the broker works, the chat lists the progress updates of the flow (one per step) and keeps them above the answer.
