# Patient Intake (demo data)

A clinic front desk: triage questions, insurance check and appointment booking from one conversation. Fictional patients only.

- Style: Probabilistic (Agent Network 1.0): the LLM broker picks agents and tools from its instructions.
- Agents: Triage Nurse Agent (A2A 0.3.0, Vertex), Scheduling Agent (A2A 0.3.0, MuleSoft), Insurance Verification Agent (A2A 0.3.0, Bedrock)
- MCP servers: Clinic Records MCP (lookup_patient, record_intake)

All agents and MCP servers are public A2D mocks, so the network runs without any other system. No credentials are stored in this template.

## Deploy in 3 steps

1. **Setup & Connect**: connect Agent Fabric (connected app client ID and secret, organization). A²D is not needed: the mock URLs are already the defaults in `exchange.json`.
2. In `exchange.json`, fill in `ingressgw.url` (ingress gateway base url). In **Projects & Deploy**, click **Deploy** on this project (or **Build & Deploy** in the editor) and pick your gateway. Octoloom asks for each secret variable; nothing you type is stored:
   - `openai.apiKey`: your OpenAI API key (required)
3. When the status light turns green (**Deployed and running**), click **Open chat** and paste a prompt below. The **ANT** icon under a reply opens the task in the Agent Network Tracer, with each agent and tool call.

## Try it

- **P-5001 has had a sore throat and fever for 3 days**
  - You should see: Clinic Records `lookup_patient`: Alex Demo, HealthPlus, penicillin allergy. Triage Nurse: urgency "soon". Scheduling books APT-9101 tomorrow 09:40 with Dr. Brandt, Insurance Verification: 20 CHF co-pay, `record_intake` saves IN-3301.
- **Book a check-up for P-5002, insurance HealthPlus**
  - You should see: Triage "routine", Scheduling books APT-9102 on 2026-11-27 14:00 with Dr. Okafor. The record says Sam Example is insured with CareOne (no co-pay), so the broker may point out the mismatch.
- **P-5001 has chest pain right now**
  - You should see: Triage Nurse: "emergency". The broker stops and tells the patient to call emergency services; no appointment is booked.

The broker is probabilistic: the LLM picks the agents and tools, so the wording and the order of the calls can change between runs. The ids and numbers come from the mocks and stay the same.
