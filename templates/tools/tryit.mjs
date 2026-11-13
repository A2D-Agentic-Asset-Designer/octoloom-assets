// Example prompts per use case for the template READMEs (#95), with what the A2D mocks answer.
// p = prompt to paste into the broker chat, see = what the reply and the Tracer should show.
export const TRY = {
  'v1-employee-onboarding': [
    { p: 'Onboard employee E-1001 who starts Monday as a Sales Engineer', see: 'Identity Directory `lookup_employee` finds Jane Rivera (Sales Engineer, Lausanne, starts 2026-11-16). HR Records sends contract CT-2026-118, IT Provisioning orders laptop LT-5531 and `create_account` creates the account, Facilities books desk LS-3-14 and badge B-77812.' },
    { p: 'Assign the onboarding training to E-1001', see: 'Learning MCP `list_courses` and `assign_training`: 3 courses assigned, due 2026-12-15.' },
    { p: 'What is still open for the onboarding of E-1002?', see: 'Omar Haddad (Data Analyst, Remote). The broker asks the agents for the open items (contract, laptop, account, badge) and lists them.' },
  ],
  'v1-customer-service': [
    { p: 'Where is order SO-9001 for customer C-2001?', see: 'CRM `get_customer` finds Lena Fischer (Gold). Order Status Agent: SO-9001 shipped with DHL, ETA 2026-11-12.' },
    { p: 'I want to return the shoes from order SO-9002', see: 'Order Status Agent: SO-9002 is delivered. Returns Agent opens return RMA-4410.' },
    { p: 'Why was I charged twice on invoice INV-7781? I am C-2001', see: 'Billing Agent: invoice INV-7781 has one charge and one pre-authorisation, released within 3 days. The broker may log CRM case CS-30551 with `create_case`.' },
    { p: 'How many points do I have? I am C-2001. Redeem them for a voucher', see: 'Loyalty Agent: 1,840 points, Gold tier until 2027-03-31. Redeeming 500 points gives voucher VC-5050 (10 EUR), 1,340 points left.' },
    { p: 'Exchange the shoes from SO-9002 for a bigger size', see: 'Returns Agent: exchange EX-118, size 42 replaces size 41.' },
  ],
  'v1-it-helpdesk': [
    { p: 'VPN is not connecting since this morning', see: 'IT Triage classifies it as Network/VPN P3. Monitoring `get_service_health`: vpn degraded (outage OUT-552). Knowledge Base `search_articles` returns KB-1201.' },
    { p: 'I need access to the finance SharePoint', see: 'Access Request Agent opens access request AR-7781.' },
    { p: 'My laptop screen flickers', see: 'Knowledge Base returns KB-2210. Device Support pushes a display driver update and books swap SW-3310 for tomorrow 10:00 if it still flickers.' },
    { p: 'P1: nobody can log in to email. Open an incident', see: 'ITSM `create_incident` creates INC-90001.' },
    { p: 'What is the status of INC-90017?', see: 'ITSM `get_incident`: in progress, assigned to Alex Kim.' },
  ],
  'v1-travel-expense': [
    { p: 'Book a trip from Zurich to London for 2026-12-02 to 2026-12-04', see: 'Flights `search_flights`: LX318, 212 CHF. Hotels `search_hotels`: Thames Bridge, 210 GBP. Policy Advisor checks the hotel limit (220 GBP per night). Travel Booking books LX318 (PNR K7Q2ZP) and the hotel (H-55120).' },
    { p: 'Can I fly business class to London?', see: 'Policy Advisor: business class only for flights over 6 hours, so economy.' },
    { p: 'Do I need a visa for India? And for the UK?', see: 'Visa Agent: India needs an e-Business visa (apply 4 days ahead); the UK needs no visa but an ETA.' },
    { p: 'Submit my hotel bill of 420 GBP for reimbursement', see: 'Expense Audit approves the hotel (2 nights at 210 GBP, within the limit). Currency `convert_currency`: 1.1483, 482.30 CHF. Expense `create_expense_report` creates ER-6610; Reimbursement schedules RB-8812 for 2026-11-25.' },
  ],
  'v1-procurement': [
    { p: 'Order 5 monitors for cost centre CC-410', see: 'Catalog `search_catalog`: MON-27A, 349 CHF from SUP-88. Budget `check_budget`: CC-410 has 5,200 left. Supplier Risk: SUP-88 approved (risk 23). Contracts `find_contract`: FC-2026-04 (12% off). Purchase Orders `create_purchase_order`: PO-450021, 1,535.60.' },
    { p: 'Is supplier SUP-88 approved? And SUP-91?', see: 'Supplier Registry `get_supplier` and Supplier Risk: SUP-88 approved (risk 23), SUP-91 not approved (risk 71).' },
    { p: 'Order 5 monitors for cost centre CC-999', see: 'Budget `check_budget`: CC-999 has only 120 left, so no purchase order is created.' },
    { p: 'Find an alternative to MON-27A', see: 'Sourcing Agent: 27" QHD monitor MON-27B from SUP-88 at 219 CHF (contract FC-2026-04).' },
  ],
  'v1-hr-leave': [
    { p: 'E-3001 wants vacation from 2026-12-21 to 2026-12-31', see: 'HRIS `get_leave_balance`: Mia Keller has 14 days left. Team Calendar `check_team_calendar` (team M-410): Noah Weber is away 2026-12-22 to 2027-01-02. Leave Policy: allowed, outside the year-end freeze. `submit_leave_request` creates LR-7701, pending approval by M-410.' },
    { p: 'Can E-3002 take 3 days of unpaid leave next week?', see: 'Luca Rossi has 1 vacation day left and used 2 unpaid days. Leave Policy: up to 5 unpaid days a year with manager approval. Payroll: the next payslip drops by 742.50 CHF gross. A request creates LR-7702.' },
    { p: 'Who in team M-410 is away over Christmas?', see: 'Team Calendar: Noah Weber, 2026-12-22 to 2027-01-02.' },
  ],
  'v1-patient-intake': [
    { p: 'P-5001 has had a sore throat and fever for 3 days', see: 'Clinic Records `lookup_patient`: Alex Demo, HealthPlus, penicillin allergy. Triage Nurse: urgency "soon". Scheduling books APT-9101 tomorrow 09:40 with Dr. Brandt, Insurance Verification: 20 CHF co-pay, `record_intake` saves IN-3301.' },
    { p: 'Book a check-up for P-5002, insurance HealthPlus', see: 'Triage "routine", Scheduling books APT-9102 on 2026-11-27 14:00 with Dr. Okafor. The record says Sam Example is insured with CareOne (no co-pay), so the broker may point out the mismatch.' },
    { p: 'P-5001 has chest pain right now', see: 'Triage Nurse: "emergency". The broker stops and tells the patient to call emergency services; no appointment is booked.' },
  ],
  'v2-insurance-claims': [
    { p: 'My car was hit in a parking lot, policy POL-5001', see: 'FNOL takes the claim, Policy Admin `check_coverage` confirms motor cover, Claims `create_claim`, creates CLM-30017, Fraud: low (12), Adjuster proposes 1,980 CHF (2,480 minus 500 deductible) and Payments releases PAY-77120.' },
    { p: 'Water damage in the kitchen, policy POL-5002, about 18,000 CHF', see: 'Fraud risk high (82): new policy and amount above 10,000 CHF. Claims `refer_to_siu` opens SIU-0091 (investigator R. Meier). No payment.' },
    { p: 'Storm damage on my roof, policy POL-5003', see: 'Policy Admin: the policy lapsed. The flow ends in the not-covered branch.' },
  ],
  'v2-retail-returns': [
    { p: 'I want to return order ORD-1001, the jacket is too small', see: 'Orders `check_return_eligibility`: eligible. `create_rma` creates RMA-88001, Refund Agent refunds RF-1001, 129 CHF.' },
    { p: 'Return ORD-1002 please', see: 'Delivered 47 days ago, outside the 30-day window: declined. Returns Desk offers a 15% voucher (VC-RET-15) or a repair.' },
    { p: 'Return ORD-9999', see: 'The order is not found, so it is not eligible: the flow takes the decline branch, no RMA.' },
  ],
  'v2-loan-origination': [
    { p: 'Applicant APP-100 asks for a 25,000 CHF personal loan', see: 'Intake, KYC, Credit Bureau `get_credit_score` and Credit Analysis approve. Core Banking `book_loan` books LN-2026-0100 at 4.9%, Documents `generate_contract` creates DOC-77100, Customer Notification informs the applicant.' },
    { p: 'Applicant APP-200 wants 300,000 CHF for a mortgage', see: 'Bureau score 655, debt-to-income 41%: the assessment refers it. Underwriting approves 260,000 CHF with a 20% equity condition.' },
  ],
  'v2-field-service': [
    { p: 'Heat pump HP-301 shows error E42', see: 'Asset Registry `get_asset`, Diagnostics `run_diagnostics` needs a visit. Parts Inventory `check_stock`: CMP-42 from Bern. Weather `get_forecast`: Vevey OK. Parts Logistics reserves it, Dispatch books technician T-14 (Marco) tomorrow 08:00-10:00, Customer Communications confirms.' },
    { p: 'Solar inverter INV-77 is offline', see: 'Diagnostics `run_diagnostics`: lost connectivity, fixed with a remote reboot. Customer Communications informs the customer; no visit.' },
  ],
  'v2-campaign-studio': [
    { p: 'Launch a winter email campaign for segment SEG-VIP', see: 'Audience Segments `get_segment`, Brand Assets `find_assets`, Content drafts, Marketing Compliance approves. Email `schedule_email` schedules EM-2026-311 for 2026-11-14 08:00 UTC, Analytics `forecast`: 41% open rate, 86,000 CHF expected revenue.' },
    { p: 'Plan a social post about our new eco line for SEG-ECO', see: 'Compliance approves with a change: "carbon neutral" becomes "lower-impact materials". The flow ends in the social-ready branch.' },
    { p: 'Send an email about the eco line to SEG-ECO', see: 'SEG-ECO has 0 email-consented contacts: the campaign is returned, nothing is scheduled.' },
  ],
  'v2-supply-chain': [
    { p: 'Shipment SHP-4401 with SKU-778 is delayed 9 days at the port', see: 'Shipments `get_shipment`, Inventory `get_stock`: 4 days of cover, shorter than the delay. Logistics `reroute_shipment` to rail, ETA 2026-11-21, +2,300 EUR. Customer Communications informs 12 customers.' },
    { p: 'Supplier reports a shortage of SKU-912 for shipment SHP-4402', see: 'Inventory: 21 days of cover. Supplier Risk: SUP-12 is high risk; `find_alternative_supplier`: SUP-31 in 5 days at +4%. Buyer places PO-66120 for 4,000 units, delivery 2026-11-18.' },
  ],
  'v2-kyc-onboarding': [
    { p: 'Onboard applicant AP-7001, Lena Novak, from Austria', see: 'Identity `verify_document`, Sanctions `screen_name`: no hit, Risk `score_customer`: low (12). Account Opening opens CH93-0000-7001.' },
    { p: 'Onboard applicant AP-7002 from Germany', see: 'Risk medium (48): the KYC Analyst confirms the source of funds, and Account Opening opens CH93-0000-7002 with enhanced monitoring.' },
    { p: 'Onboard applicant AP-7003, Victor Example, from Panama', see: 'Sanctions hit (0.93), risk high (91): Risk `open_case` opens CMP-2026-0419. No account.' },
    { p: 'Onboard applicant AP-9999', see: 'No document on file, so the risk band is medium and the KYC Analyst asks for more proof; no account is opened.' },
  ],
  'v2-incident-response': [
    { p: 'P1: checkout-api returns 500 for all users since 10:02', see: 'Triage, Monitoring `get_service_health`, Ticketing `create_incident` INC-50211 and `page_oncall` (Dana Example). Triage blames deploy 2026.11.12-3, Application Support rolls back to 2026.11.12-2, Status Page posts update ST-818.' },
    { p: 'orders-db replication lag is 40 minutes', see: 'Routed to the Database Operations Agent: batch job BJ-4410 is throttled, lag below 1 minute in 15 minutes.' },
    { p: 'VPN in the Zurich office drops every few minutes', see: 'Routed to the Network Operations Agent: vpn-zrh-2 flaps because of an expiring certificate; failover to vpn-zrh-1, renewal at 14:00.' },
  ],
};
