# Octoloom tutorials

One tutorial for every template project in Octoloom for Agent Fabric. Each one gives you three paths:

1. **Just use it**: import the template from **New Project**, deploy it and chat with it.
2. **Learn step by step**: the same project, explained part by part (canvas, AgentScript flow, policies, deploy, chat, Tracer), with screenshots.
3. **Build it from scratch**: start from a blank project and build the same network with forms, menus and buttons only (no code), one screenshot per step.

New to Octoloom? Start with **[Getting started](../getting-started.md)**, then pick a template. A good learning order is the smallest ones first: *Retail Returns* (deterministic) and *Customer Service* (probabilistic), then their governed and secured variants. No OpenAI key yet? The **Fully mocked** ones (*Hotel Concierge*, *Event Ticketing* and four more) use an A²D LLM mock, so you can deploy and chat with only an Anypoint org.

## Probabilistic networks (Agent Network 1.0)

An LLM broker reads its instructions and picks agents and MCP tools.

| Tutorial | Kind | Agents | MCP | Policies |
|---|---|---|---|---|
| [Customer Service Broker](v1-customer-service.md) | Use case | 4 | 1 | 0 |
| [Employee Onboarding](v1-employee-onboarding.md) | Use case | 3 | 2 | 0 |
| [HR Leave Requests](v1-hr-leave.md) | Use case | 2 | 2 | 0 |
| [IT Helpdesk](v1-it-helpdesk.md) | Use case | 3 | 3 | 0 |
| [Patient Intake (demo data)](v1-patient-intake.md) | Use case | 3 | 1 | 0 |
| [Procurement Assistant](v1-procurement.md) | Use case | 2 | 5 | 0 |
| [Travel & Expense](v1-travel-expense.md) | Use case | 5 | 4 | 0 |
| [Fleet Maintenance (fully mocked)](v1-fleet-maintenance.md) | Fully mocked | 2 | 4 | 0 |
| [Hotel Concierge (fully mocked)](v1-hotel-concierge.md) | Fully mocked | 2 | 1 | 0 |
| [Library Services (fully mocked)](v1-library-services.md) | Fully mocked | 2 | 3 | 0 |
| [Customer Service Broker: governed](v1-customer-service-governed.md) | Governed | 4 | 1 | 5 |
| [Employee Onboarding: governed](v1-employee-onboarding-governed.md) | Governed | 3 | 2 | 6 |
| [HR Leave Requests: governed](v1-hr-leave-governed.md) | Governed | 2 | 2 | 6 |
| [IT Helpdesk: governed](v1-it-helpdesk-governed.md) | Governed | 3 | 3 | 6 |
| [Patient Intake (demo data): governed](v1-patient-intake-governed.md) | Governed | 3 | 1 | 5 |
| [Procurement Assistant: governed](v1-procurement-governed.md) | Governed | 2 | 5 | 6 |
| [Travel & Expense: governed](v1-travel-expense-governed.md) | Governed | 5 | 4 | 6 |
| [HR Leave Requests: secured](v1-hr-leave-secured.md) | Secured | 2 | 2 | 1 |
| [Patient Intake (demo data): secured](v1-patient-intake-secured.md) | Secured | 3 | 1 | 1 |
| [IDMC Customer Data Steward (needs Informatica IDMC)](v1-idmc-customer-steward.md) | IDMC | 0 | 4 | 0 |

## Deterministic networks (Agent Network 2.0, AgentScript)

AgentScript flows decide every step: routers, gates, executors.

| Tutorial | Kind | Agents | MCP | Policies |
|---|---|---|---|---|
| [Field Service Dispatch](v2-field-service.md) | Use case | 3 | 4 | 0 |
| [IT Incident Response](v2-incident-response.md) | Use case | 5 | 2 | 0 |
| [Insurance Claims (FNOL to Payout)](v2-insurance-claims.md) | Use case | 4 | 2 | 0 |
| [KYC / AML Onboarding](v2-kyc-onboarding.md) | Use case | 2 | 3 | 0 |
| [Loan Origination](v2-loan-origination.md) | Use case | 5 | 3 | 0 |
| [Marketing Campaign Studio](v2-campaign-studio.md) | Use case | 2 | 4 | 0 |
| [Retail Returns](v2-retail-returns.md) | Use case | 2 | 1 | 0 |
| [Supply Chain Disruption](v2-supply-chain.md) | Use case | 4 | 3 | 0 |
| [Event Ticketing (fully mocked)](v2-event-ticketing.md) | Fully mocked | 2 | 2 | 0 |
| [Utility Outage (fully mocked)](v2-utility-outage.md) | Fully mocked | 3 | 2 | 0 |
| [Warranty Repair (fully mocked)](v2-warranty-repair.md) | Fully mocked | 3 | 1 | 0 |
| [Field Service Dispatch: governed](v2-field-service-governed.md) | Governed | 3 | 4 | 5 |
| [IT Incident Response: governed](v2-incident-response-governed.md) | Governed | 5 | 2 | 5 |
| [Insurance Claims (FNOL to Payout): governed](v2-insurance-claims-governed.md) | Governed | 4 | 2 | 5 |
| [KYC / AML Onboarding: governed](v2-kyc-onboarding-governed.md) | Governed | 2 | 3 | 5 |
| [Loan Origination: governed](v2-loan-origination-governed.md) | Governed | 5 | 3 | 6 |
| [Marketing Campaign Studio: governed](v2-campaign-studio-governed.md) | Governed | 2 | 4 | 5 |
| [Retail Returns: governed](v2-retail-returns-governed.md) | Governed | 2 | 1 | 5 |
| [Supply Chain Disruption: governed](v2-supply-chain-governed.md) | Governed | 4 | 3 | 5 |
| [IT Incident Response: secured](v2-incident-response-secured.md) | Secured | 5 | 2 | 2 |
| [KYC / AML Onboarding: secured](v2-kyc-onboarding-secured.md) | Secured | 2 | 3 | 2 |
| [Supply Chain Disruption: secured](v2-supply-chain-secured.md) | Secured | 4 | 3 | 2 |
| [IDMC Data Trust (needs Informatica IDMC)](v2-idmc-data-trust.md) | IDMC | 0 | 4 | 0 |

---
The tutorials are generated from the bundled templates with `tutorials/tools/build.py` and updated when the templates change. Screenshots use fake data.
