# Patient Intake (demo data) (governed)

A clinic front desk: triage questions, insurance check and appointment booking from one conversation. Fictional patients only.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Triage Nurse Agent (A2A 0.3.0, Vertex), Scheduling Agent (A2A 0.3.0, MuleSoft), Insurance Verification Agent (A2A 0.3.0, Bedrock)
- MCP servers: Clinic Records MCP (lookup_patient, record_intake)
- Policies (Agent Fabric built-ins): rate-limiting, mcp-pii-detector, a-two-a-pii-detector, header-injection, a-two-a-prompt-decorator. They are declared in agent-network.yaml and listed as `schema` dependencies in exchange.json.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time and `ingressgw.url` to your ingress gateway URL. No credentials are stored in this template.

## Try it

- P-5001 has had a sore throat and fever for 3 days
- Book a check-up for P-5002, insurance HealthPlus
