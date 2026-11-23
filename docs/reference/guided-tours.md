# Guided tours

Each canvas shows a short tour the first time you open it (*Don't show again* hides it). Replay it with **Guide** in the toolbar or **Start the guide** on the Explain button.

## Probabilistic network (Agent Network 1.0)

1. **How this style works**: An LLM broker reads its instructions, then decides at run time which linked agents and MCP tools to call. You describe goals and rules; the model picks the path. A2A 0.3.0.
2. **The canvas**: Brokers are the large cards. Agents and MCP servers linked to a broker are drawn to its right; the LLM provider and connections sit below. Drag cards to arrange them; positions are saved per file.
3. **Add components**: Use + to add a broker, agent, MCP server, LLM provider or policy. The box button opens the Asset Palette, where you drag Exchange or A2D assets onto a broker to link them.
4. **Edit a component**: Select a card to edit it on the right: broker instructions (with templates), allowed MCP tools, LLM model, connection URLs and policies.
5. **Visual or code**: Switch to Code to edit agent-network.yaml directly. Both views edit the same file.
6. **Build and deploy**: Build & Deploy runs the Anypoint CLI: build, publish to Exchange, deploy to your gateway. Secrets such as the OpenAI key are asked at deploy time and never stored in files.
7. **Minimize to icons**: Minimize all shrinks every card to its icon so you see what is orchestrated at a glance; press it again to open all. Click any card's icon to minimize just that card, and click a minimized icon to open it again.
8. **Explain anything**: The floating info button explains anything: click it, then click a card, a panel or a tool for what it is, when to use it and examples. Drag it out of the way if it covers something. Replay this tour with Start the guide in the Explain hint.

## Deterministic network (Agent Network 2.0)

1. **How this style works**: Each broker runs an AgentScript flow (brokers/*.agent). The flow decides every step: generators extract, routers branch, executors call tools with bound inputs, subagents use the LLM only where you allow it. A2A 1.0 and 0.3.0 agents can be mixed.
2. **The network canvas**: This canvas holds the registry (agents, MCP servers, LLMs), the connections and the policies. Open a broker to edit its flow in the .agent editor.
3. **Add components**: Use + to add brokers, registry entries, connections and policies, or drag assets from the Asset Palette.
4. **Policies on connections**: Policies attach to a connection (inbound or outbound) or to the broker interface. Built-ins like rate limiting, PII detection and header injection come from Agent Fabric.
5. **Build and deploy**: Build & Deploy builds, publishes and deploys through the Anypoint CLI. Every template README.md lists the deploy steps and prompts to try, with the expected answers.
6. **Minimize to icons**: Minimize all shrinks every card to its icon; press it again to open all. Click a card's icon to minimize or open just that card.
7. **Explain anything**: The floating info button explains anything: click it, then click a card, a panel or a tool for what it is, when to use it and examples. Drag it out of the way if it covers something. Replay this tour with Start the guide in the Explain hint.

## AgentScript flow editor (.agent)

1. **A flow of steps**: A trigger receives the A2A message and transitions through nodes until a Reply ends the task. Each node reads earlier outputs with @kind.name.output.field.
2. **Explorer**: Settings (system instructions, LLM, connections/actions, variables) and the list of nodes. Drag a chip from the bottom onto the canvas to add a node.
3. **Canvas**: Drag from a card's output port onto another card to connect it. Click a connection to delete it. Right-click a card (or the canvas) for the add menu with templates.
4. **Add the next step**: + Step opens a multi-level menu: each node type has an Empty entry and templates; Patterns insert several wired nodes, e.g. Logical case selection (generator → router → subagents).
5. **Inspector**: Select a node to edit it. Instruction fields have an Insert template picker. A node's type cannot change after creation; add a new node instead.
6. **Preview and versions**: Preview chats with the deployed broker. New Version / Commit Version bump exchange.json.
7. **Minimize to icons**: Minimize all shrinks every node to its icon so the flow fits on screen; press Open all to restore. Click a node's icon to minimize or open just that node.
8. **Explain anything**: The floating info button explains anything: click it, then click a card, a panel or a tool for what it is, when to use it and examples. Drag it out of the way if it covers something. Replay this tour with Start the guide in the Explain hint.
