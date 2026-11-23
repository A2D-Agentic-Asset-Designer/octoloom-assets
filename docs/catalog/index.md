# Templates

Octoloom ships **43 ready-to-run templates**. Open one with **New Project** (Home → *New Probabilistic / Deterministic Network* → *Use cases* or *Technical*). Every upstream is a public A²D mock, so a template deploys and answers without any backend of yours.

| Kind | What it is |
|---|---|
| Use case | A business network: agents, MCP servers and an LLM broker or an AgentScript flow. |
| Governed | The same use case with built-in Agent Fabric gateway policies. |
| Secured | A use case whose agents, MCP servers or LLM need authentication (client credentials, API key, OAuth 2.0). |
| Fully mocked | The LLM is an A²D LLM mock too: deploy and chat without an OpenAI key. |
| Informatica IDMC | Uses Informatica IDMC MCP servers (needs an IDMC org). |

## Probabilistic (Agent Network 1.0)

| Template | Kind | Agents | MCP | Policies | Tutorial |
|---|---|---|---|---|---|
| [Employee Onboarding](v1-employee-onboarding.md) | Use case | 3 | 2 | 0 | [Tutorial](../tutorials/v1-employee-onboarding.md) |
| [Employee Onboarding: governed](v1-employee-onboarding-governed.md) | Governed | 3 | 2 | 6 | [Tutorial](../tutorials/v1-employee-onboarding-governed.md) |
| [Customer Service Broker](v1-customer-service.md) | Use case | 4 | 1 | 0 | [Tutorial](../tutorials/v1-customer-service.md) |
| [Customer Service Broker: governed](v1-customer-service-governed.md) | Governed | 4 | 1 | 5 | [Tutorial](../tutorials/v1-customer-service-governed.md) |
| [IT Helpdesk](v1-it-helpdesk.md) | Use case | 3 | 3 | 0 | [Tutorial](../tutorials/v1-it-helpdesk.md) |
| [IT Helpdesk: governed](v1-it-helpdesk-governed.md) | Governed | 3 | 3 | 6 | [Tutorial](../tutorials/v1-it-helpdesk-governed.md) |
| [Travel & Expense](v1-travel-expense.md) | Use case | 5 | 4 | 0 | [Tutorial](../tutorials/v1-travel-expense.md) |
| [Travel & Expense: governed](v1-travel-expense-governed.md) | Governed | 5 | 4 | 6 | [Tutorial](../tutorials/v1-travel-expense-governed.md) |
| [Procurement Assistant](v1-procurement.md) | Use case | 2 | 5 | 0 | [Tutorial](../tutorials/v1-procurement.md) |
| [Procurement Assistant: governed](v1-procurement-governed.md) | Governed | 2 | 5 | 6 | [Tutorial](../tutorials/v1-procurement-governed.md) |
| [HR Leave Requests](v1-hr-leave.md) | Use case | 2 | 2 | 0 | [Tutorial](../tutorials/v1-hr-leave.md) |
| [HR Leave Requests: governed](v1-hr-leave-governed.md) | Governed | 2 | 2 | 6 | [Tutorial](../tutorials/v1-hr-leave-governed.md) |
| [HR Leave Requests: secured](v1-hr-leave-secured.md) | Secured | 2 | 2 | 1 | [Tutorial](../tutorials/v1-hr-leave-secured.md) |
| [Patient Intake (demo data)](v1-patient-intake.md) | Use case | 3 | 1 | 0 | [Tutorial](../tutorials/v1-patient-intake.md) |
| [Patient Intake (demo data): governed](v1-patient-intake-governed.md) | Governed | 3 | 1 | 5 | [Tutorial](../tutorials/v1-patient-intake-governed.md) |
| [Patient Intake (demo data): secured](v1-patient-intake-secured.md) | Secured | 3 | 1 | 1 | [Tutorial](../tutorials/v1-patient-intake-secured.md) |
| [Hotel Concierge (fully mocked)](v1-hotel-concierge.md) | Fully mocked | 2 | 1 | 0 | [Tutorial](../tutorials/v1-hotel-concierge.md) |
| [Library Services (fully mocked)](v1-library-services.md) | Fully mocked | 2 | 3 | 0 | [Tutorial](../tutorials/v1-library-services.md) |
| [Fleet Maintenance (fully mocked)](v1-fleet-maintenance.md) | Fully mocked | 2 | 4 | 0 | [Tutorial](../tutorials/v1-fleet-maintenance.md) |
| [IDMC Customer Data Steward (needs Informatica IDMC)](v1-idmc-customer-steward.md) | Informatica IDMC | 0 | 4 | 0 | [Tutorial](../tutorials/v1-idmc-customer-steward.md) |

## Deterministic (Agent Network 2.0, AgentScript)

| Template | Kind | Agents | MCP | Policies | Tutorial |
|---|---|---|---|---|---|
| [Insurance Claims (FNOL to Payout)](v2-insurance-claims.md) | Use case | 4 | 2 | 0 | [Tutorial](../tutorials/v2-insurance-claims.md) |
| [Insurance Claims (FNOL to Payout): governed](v2-insurance-claims-governed.md) | Governed | 4 | 2 | 5 | [Tutorial](../tutorials/v2-insurance-claims-governed.md) |
| [Retail Returns](v2-retail-returns.md) | Use case | 2 | 1 | 0 | [Tutorial](../tutorials/v2-retail-returns.md) |
| [Retail Returns: governed](v2-retail-returns-governed.md) | Governed | 2 | 1 | 5 | [Tutorial](../tutorials/v2-retail-returns-governed.md) |
| [Loan Origination](v2-loan-origination.md) | Use case | 5 | 3 | 0 | [Tutorial](../tutorials/v2-loan-origination.md) |
| [Loan Origination: governed](v2-loan-origination-governed.md) | Governed | 5 | 3 | 6 | [Tutorial](../tutorials/v2-loan-origination-governed.md) |
| [Field Service Dispatch](v2-field-service.md) | Use case | 3 | 4 | 0 | [Tutorial](../tutorials/v2-field-service.md) |
| [Field Service Dispatch: governed](v2-field-service-governed.md) | Governed | 3 | 4 | 5 | [Tutorial](../tutorials/v2-field-service-governed.md) |
| [Marketing Campaign Studio](v2-campaign-studio.md) | Use case | 2 | 4 | 0 | [Tutorial](../tutorials/v2-campaign-studio.md) |
| [Marketing Campaign Studio: governed](v2-campaign-studio-governed.md) | Governed | 2 | 4 | 5 | [Tutorial](../tutorials/v2-campaign-studio-governed.md) |
| [Supply Chain Disruption](v2-supply-chain.md) | Use case | 4 | 3 | 0 | [Tutorial](../tutorials/v2-supply-chain.md) |
| [Supply Chain Disruption: governed](v2-supply-chain-governed.md) | Governed | 4 | 3 | 5 | [Tutorial](../tutorials/v2-supply-chain-governed.md) |
| [Supply Chain Disruption: secured](v2-supply-chain-secured.md) | Secured | 4 | 3 | 2 | [Tutorial](../tutorials/v2-supply-chain-secured.md) |
| [KYC / AML Onboarding](v2-kyc-onboarding.md) | Use case | 2 | 3 | 0 | [Tutorial](../tutorials/v2-kyc-onboarding.md) |
| [KYC / AML Onboarding: governed](v2-kyc-onboarding-governed.md) | Governed | 2 | 3 | 5 | [Tutorial](../tutorials/v2-kyc-onboarding-governed.md) |
| [KYC / AML Onboarding: secured](v2-kyc-onboarding-secured.md) | Secured | 2 | 3 | 2 | [Tutorial](../tutorials/v2-kyc-onboarding-secured.md) |
| [IT Incident Response](v2-incident-response.md) | Use case | 5 | 2 | 0 | [Tutorial](../tutorials/v2-incident-response.md) |
| [IT Incident Response: governed](v2-incident-response-governed.md) | Governed | 5 | 2 | 5 | [Tutorial](../tutorials/v2-incident-response-governed.md) |
| [IT Incident Response: secured](v2-incident-response-secured.md) | Secured | 5 | 2 | 2 | [Tutorial](../tutorials/v2-incident-response-secured.md) |
| [Event Ticketing (fully mocked)](v2-event-ticketing.md) | Fully mocked | 2 | 2 | 0 | [Tutorial](../tutorials/v2-event-ticketing.md) |
| [Warranty Repair (fully mocked)](v2-warranty-repair.md) | Fully mocked | 3 | 1 | 0 | [Tutorial](../tutorials/v2-warranty-repair.md) |
| [Utility Outage (fully mocked)](v2-utility-outage.md) | Fully mocked | 3 | 2 | 0 | [Tutorial](../tutorials/v2-utility-outage.md) |
| [IDMC Data Trust (needs Informatica IDMC)](v2-idmc-data-trust.md) | Informatica IDMC | 0 | 4 | 0 | [Tutorial](../tutorials/v2-idmc-data-trust.md) |
