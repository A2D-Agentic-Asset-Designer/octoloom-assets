# Patient Intake (demo data) (secured)

A clinic front desk: triage questions, insurance check and appointment booking from one conversation. Fictional patients only.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Triage Nurse Agent (A2A 0.3.0, Vertex), Scheduling Agent (A2A 0.3.0, MuleSoft), Insurance Verification Agent (A2A 0.3.0, Bedrock)
- MCP servers: Clinic Records MCP (lookup_patient, record_intake)
- Secured: every agent and MCP connection authenticates (Basic or Client ID enforcement, alternating). User names and client ids are variables, passwords and client secrets are secret variables asked for at deploy time. The LLM URL is the variable `llmGateway.url` (api.openai.com by default, or your LLM gateway). Policies: rate-limiting.

All agents and MCP servers are public A2D mocks, so the network runs without any other system.
Set `openai.apiKey` at deploy time and `ingressgw.url` to your ingress gateway URL. No credentials are stored in this template.

## Try it

- P-5001 has had a sore throat and fever for 3 days
- Book a check-up for P-5002, insurance HealthPlus
