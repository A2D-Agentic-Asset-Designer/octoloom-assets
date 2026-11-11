# Field Service Dispatch

Diagnose an equipment fault, check parts and weather, and dispatch or resolve remotely.

- Style: Deterministic (Agent Network 2.0): an AgentScript flow in `brokers/` decides each step.
- Agents: Dispatch Agent (A2A 1.0, ServiceNow), Parts Logistics Agent (A2A 0.3.0, MuleSoft), Customer Communications Agent (A2A 1.0, AgentForce)
- MCP servers: Asset Registry MCP (get_asset); Diagnostics MCP (run_diagnostics); Parts Inventory MCP (check_stock); Weather MCP (get_forecast)

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time. No credentials are stored in this template.

## Try it

- Heat pump HP-301 shows error E42
- Solar inverter INV-77 is offline
