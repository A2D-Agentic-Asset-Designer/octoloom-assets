// Deterministic (v2) broker flows, one per v2 use case. `A` = action names keyed by asset key.
const MSG = '{!@request.payload.message.parts[0].text}';
const echo = (id, text) => `echo ${id}:
  kind: "a2a:status_update_event"
  state: "TASK_STATE_COMPLETED"
  message: a2a.message({messageId: uuid(), parts: [a2a.textPart(${text})]})
`;
const enumProp = (name, desc, values, ind = '      ') => `${ind}${name}:
${ind}  type: "string"
${ind}  description: "${desc}"
${ind}  enum:
${values.map((v) => `${ind}    - "${v}"`).join('\n')}`;
const strProp = (name, desc, ind = '      ') => `${ind}${name}:
${ind}  type: "string"
${ind}  description: "${desc}"`;

export const FLOWS = {
  'v2-retail-returns': {
    system: 'You are the returns desk of an online retailer. Process returns only when the order system says the order is eligible.',
    actions: { check_return_eligibility: { mcp: 'orders_mcp', tool: 'check_return_eligibility' }, create_rma: { mcp: 'orders_mcp', tool: 'create_rma', inputs: { order_id: 'string', reason: 'string' } }, returns_desk_agent: { a2a: 'returns_desk_agent' }, refund_agent: { a2a: 'refund_agent' } },
    start: '@generator.extractReturn',
    body: `# Step 1: one LLM call turns the free-text request into structured fields.
generator extractReturn:
  description: "Extracts the order id and the return reason from the request."
  label: "Extract Return"
  system:
    instructions: |
      Extract the order id (for example ORD-1001) and a short return reason from the customer message.
      Use "UNKNOWN" when no order id is present.
  prompt: ->
    | ${MSG}
  outputs:
    properties:
${strProp('order_id', 'Order id, e.g. ORD-1001, or UNKNOWN')}
${strProp('reason', 'Short return reason')}
  on_exit: ->
    transition to @subagent.eligibilityGate

# Step 2: a deterministic gate. The subagent calls one MCP tool and classifies its answer.
subagent eligibilityGate:
  description: "Checks return eligibility with the Orders MCP."
  label: "Eligibility Gate"
  system:
    instructions: |
      Call the eligibility tool for the order id and report whether the order can be returned.
      Set eligible to "yes" only when the tool returns eligible true.
  reasoning:
    instructions: ->
      | Order: {!@generator.extractReturn.output.order_id}. Request: ${MSG}
    actions:
      check: @actions.check_return_eligibility
    max_number_of_loops: 3
    outputs:
      properties:
${enumProp('eligible', 'Whether the order can be returned', ['yes', 'no'], '        ')}
${strProp('detail', 'Eligibility detail from the tool', '        ')}
  on_exit: ->
    transition to @router.eligibilityRouter

router eligibilityRouter:
  description: "Eligible orders get an RMA and a refund; the others get advice."
  routes:
    - target: @executor.createRma
      when: @subagent.eligibilityGate.output.eligible == "yes"
      label: "Eligible"
  otherwise:
    target: @subagent.explainDecline

# Step 3a: no LLM. The RMA is created with bound arguments only.
executor createRma:
  description: "Creates the return authorisation."
  do: ->
    run @actions.create_rma
      with order_id = @generator.extractReturn.output.order_id
      with reason = @generator.extractReturn.output.reason
  on_exit: ->
    transition to @subagent.refund

subagent refund:
  description: "Issues the refund through the Refund agent."
  label: "Refund"
  reasoning:
    instructions: ->
      | Refund order {!@generator.extractReturn.output.order_id}. Reason: {!@generator.extractReturn.output.reason}
    actions:
      refund: @actions.refund_agent
  on_exit: ->
    transition to @echo.returnAccepted

${echo('returnAccepted', '"Return accepted for " + @generator.extractReturn.output.order_id + ". " + @subagent.refund.output')}
# Step 3b: explain the decision and offer alternatives.
subagent explainDecline:
  description: "Explains why the return is declined and offers alternatives."
  label: "Explain Decline"
  reasoning:
    instructions: ->
      | Order {!@generator.extractReturn.output.order_id} cannot be returned: {!@subagent.eligibilityGate.output.detail}. Explain this and offer alternatives.
    actions:
      returns_desk: @actions.returns_desk_agent
  on_exit: ->
    transition to @echo.returnDeclined

${echo('returnDeclined', '@subagent.explainDecline.output')}`,
  },

  'v2-insurance-claims': {
    system: 'You are a claims handler. Every claim is checked for coverage and fraud before any money moves.',
    actions: { fnol_agent: { a2a: 'fnol_agent' }, fraud_agent: { a2a: 'fraud_agent' }, adjuster_agent: { a2a: 'adjuster_agent' }, payments_agent: { a2a: 'payments_agent' }, check_coverage: { mcp: 'policy_admin_mcp', tool: 'check_coverage' }, create_claim: { mcp: 'claims_mcp', tool: 'create_claim' }, refer_to_siu: { mcp: 'claims_mcp', tool: 'refer_to_siu', inputs: { policy_id: 'string', reason: 'string' } } },
    start: '@generator.classifyClaim',
    body: `generator classifyClaim:
  description: "Classifies the loss and extracts the policy id."
  label: "Classify Claim"
  system:
    instructions: |
      Extract the policy id (for example POL-5001), the loss type and a one-line summary.
      Loss type is "motor" for vehicles and "property" for homes and buildings.
  prompt: ->
    | ${MSG}
  outputs:
    properties:
${strProp('policy_id', 'Policy id, e.g. POL-5001')}
${enumProp('loss_type', 'Type of loss', ['motor', 'property'])}
${strProp('summary', 'One-line loss summary')}
  on_exit: ->
    transition to @orchestrator.assessClaim

# Coordinates several agents and tools; the LLM decides the order.
orchestrator assessClaim:
  description: "Records the FNOL, checks coverage and screens for fraud."
  label: "Assess Claim"
  system:
    instructions: |
      1. Record the first notice of loss with the FNOL agent.
      2. Check coverage for the policy and loss type.
      3. Ask the Fraud Screening agent for a risk level.
      Set covered to "yes" or "no" from the coverage tool and fraud_risk to "high" or "low" from the fraud agent.
  reasoning:
    instructions: ->
      | Policy {!@generator.classifyClaim.output.policy_id}, {!@generator.classifyClaim.output.loss_type}: ${MSG}
    actions:
      record_fnol: @actions.fnol_agent
      coverage: @actions.check_coverage
      fraud: @actions.fraud_agent
    max_number_of_loops: 6
    outputs:
      properties:
${enumProp('covered', 'Coverage result', ['yes', 'no'], '        ')}
${enumProp('fraud_risk', 'Fraud risk level', ['high', 'low'], '        ')}
${strProp('detail', 'What was found', '        ')}
  on_exit: ->
    transition to @router.claimRouter

router claimRouter:
  description: "Not covered: stop. High fraud risk: refer to SIU. Otherwise settle."
  routes:
    - target: @echo.notCovered
      when: @orchestrator.assessClaim.output.covered == "no"
      label: "Not covered"
    - target: @executor.referToSiu
      when: @orchestrator.assessClaim.output.fraud_risk == "high"
      label: "High fraud risk"
  otherwise:
    target: @orchestrator.settleClaim

${echo('notCovered', '"Claim not covered for policy " + @generator.classifyClaim.output.policy_id + ": " + @orchestrator.assessClaim.output.detail')}
executor referToSiu:
  description: "Refers the claim to the special investigations unit."
  do: ->
    run @actions.refer_to_siu
      with policy_id = @generator.classifyClaim.output.policy_id
      with reason = "High fraud risk score"
  on_exit: ->
    transition to @echo.referred

${echo('referred', '"Claim for policy " + @generator.classifyClaim.output.policy_id + " was referred to special investigations. A specialist will contact you."')}
orchestrator settleClaim:
  description: "Creates the claim, gets a settlement and pays it."
  label: "Settle Claim"
  system:
    instructions: |
      Create the claim record, ask the adjuster for a settlement proposal, then pay it with the payments agent.
      Return a short summary with the claim id, settlement amount and payment id.
  reasoning:
    instructions: ->
      | Policy {!@generator.classifyClaim.output.policy_id}, {!@generator.classifyClaim.output.loss_type}: {!@generator.classifyClaim.output.summary}
    actions:
      create_claim: @actions.create_claim
      adjust: @actions.adjuster_agent
      pay: @actions.payments_agent
    max_number_of_loops: 8
  on_exit: ->
    transition to @echo.settled

${echo('settled', '@orchestrator.settleClaim.output')}`,
  },

  'v2-loan-origination': {
    system: 'You are a loan origination desk. Decisions follow the credit data; never promise an approval before the assessment.',
    actions: { intake_agent: { a2a: 'intake_agent' }, kyc_agent: { a2a: 'kyc_agent' }, credit_agent: { a2a: 'credit_agent' }, underwriting_agent: { a2a: 'underwriting_agent' }, notification_agent: { a2a: 'notification_agent' }, get_credit_score: { mcp: 'credit_bureau_mcp', tool: 'get_credit_score' }, get_accounts: { mcp: 'core_banking_mcp', tool: 'get_accounts' }, book_loan: { mcp: 'core_banking_mcp', tool: 'book_loan', inputs: { applicant_id: 'string', amount: 'number' } }, generate_contract: { mcp: 'documents_mcp', tool: 'generate_contract' } },
    start: '@generator.parseApplication',
    body: `generator parseApplication:
  description: "Extracts applicant, amount and product."
  label: "Parse Application"
  system:
    instructions: |
      Extract the applicant id (for example APP-100), the requested amount in CHF as a number, and the product.
      Product is "mortgage" for property financing, otherwise "personal".
  prompt: ->
    | ${MSG}
  outputs:
    properties:
${strProp('applicant_id', 'Applicant id, e.g. APP-100')}
      amount:
        type: "number"
        description: "Requested amount in CHF"
${enumProp('product', 'Loan product', ['personal', 'mortgage'])}
  on_exit: ->
    transition to @orchestrator.assess

orchestrator assess:
  description: "Runs intake, KYC and the credit analysis."
  label: "Assess Application"
  system:
    instructions: |
      Run intake, KYC and the credit analysis, and read the bureau score and the accounts.
      Decision rules: "approve" when KYC passed, score >= 700 and debt-to-income <= 35%.
      "refer" when KYC passed but the score or affordability is borderline. "decline" when KYC fails.
  reasoning:
    instructions: ->
      | Applicant {!@generator.parseApplication.output.applicant_id} requests {!@generator.parseApplication.output.amount} CHF ({!@generator.parseApplication.output.product}).
    actions:
      intake: @actions.intake_agent
      kyc: @actions.kyc_agent
      credit: @actions.credit_agent
      score: @actions.get_credit_score
      accounts: @actions.get_accounts
    max_number_of_loops: 8
    outputs:
      properties:
${enumProp('decision', 'Assessment decision', ['approve', 'refer', 'decline'], '        ')}
${strProp('summary', 'Reasons for the decision', '        ')}
  on_exit: ->
    transition to @router.decisionRouter

router decisionRouter:
  description: "Approve books the loan, refer goes to underwriting, decline notifies."
  routes:
    - target: @executor.bookLoan
      when: @orchestrator.assess.output.decision == "approve"
      label: "Approve"
    - target: @subagent.underwrite
      when: @orchestrator.assess.output.decision == "refer"
      label: "Refer"
  otherwise:
    target: @subagent.notifyDecline

executor bookLoan:
  description: "Books the approved loan."
  do: ->
    run @actions.book_loan
      with applicant_id = @generator.parseApplication.output.applicant_id
      with amount = @generator.parseApplication.output.amount
  on_exit: ->
    transition to @subagent.notifyApproval

subagent notifyApproval:
  description: "Generates the contract and notifies the applicant."
  label: "Notify Approval"
  reasoning:
    instructions: ->
      | The loan for {!@generator.parseApplication.output.applicant_id} is booked. Generate the contract and notify the applicant.
    actions:
      contract: @actions.generate_contract
      notify: @actions.notification_agent
  on_exit: ->
    transition to @echo.approved

${echo('approved', '"Approved: " + @orchestrator.assess.output.summary + " " + @subagent.notifyApproval.output')}
subagent underwrite:
  description: "Sends borderline applications to underwriting."
  label: "Underwriting"
  reasoning:
    instructions: ->
      | Underwrite application of {!@generator.parseApplication.output.applicant_id}: {!@orchestrator.assess.output.summary}
    actions:
      underwriting: @actions.underwriting_agent
  on_exit: ->
    transition to @echo.underwritten

${echo('underwritten', '@subagent.underwrite.output')}
subagent notifyDecline:
  description: "Notifies the applicant of a decline."
  label: "Notify Decline"
  reasoning:
    instructions: ->
      | Notify {!@generator.parseApplication.output.applicant_id} that the application was declined: {!@orchestrator.assess.output.summary}
    actions:
      notify: @actions.notification_agent
  on_exit: ->
    transition to @echo.declined

${echo('declined', '"Declined: " + @orchestrator.assess.output.summary')}`,
  },

  'v2-field-service': {
    system: 'You run field service for heating and solar equipment. Fix remotely when possible; dispatch only when needed and safe.',
    actions: { dispatch_agent: { a2a: 'dispatch_agent' }, parts_agent: { a2a: 'parts_agent' }, customer_comms_agent: { a2a: 'customer_comms_agent' }, get_asset: { mcp: 'asset_registry_mcp', tool: 'get_asset' }, run_diagnostics: { mcp: 'diagnostics_mcp', tool: 'run_diagnostics' }, check_stock: { mcp: 'inventory_mcp', tool: 'check_stock' }, get_forecast: { mcp: 'weather_mcp', tool: 'get_forecast' } },
    start: '@generator.parseRequest',
    body: `generator parseRequest:
  description: "Extracts the asset id and the symptom."
  label: "Parse Request"
  prompt: ->
    | Extract the asset id (for example HP-301 or INV-77) and the symptom from: ${MSG}
  outputs:
    properties:
${strProp('asset_id', 'Asset id')}
${strProp('symptom', 'Reported symptom')}
  on_exit: ->
    transition to @subagent.diagnose

subagent diagnose:
  description: "Looks up the asset and runs remote diagnostics."
  label: "Diagnose"
  system:
    instructions: |
      Look up the asset and run remote diagnostics.
      Set remote_fix to "yes" when diagnostics fixed the fault remotely, otherwise "no".
      Return the part id when a part is needed and the town of the site.
  reasoning:
    instructions: ->
      | Asset {!@generator.parseRequest.output.asset_id}: {!@generator.parseRequest.output.symptom}
    actions:
      asset: @actions.get_asset
      diagnostics: @actions.run_diagnostics
    max_number_of_loops: 4
    outputs:
      properties:
${enumProp('remote_fix', 'Fixed remotely', ['yes', 'no'], '        ')}
${strProp('part_id', 'Needed part id or NONE', '        ')}
${strProp('town', 'Town of the site', '        ')}
${strProp('detail', 'Diagnosis detail', '        ')}
  on_exit: ->
    transition to @router.fixRouter

router fixRouter:
  description: "Remote fixes only need a customer update; the rest are dispatched."
  routes:
    - target: @subagent.informCustomer
      when: @subagent.diagnose.output.remote_fix == "yes"
      label: "Fixed remotely"
  otherwise:
    target: @orchestrator.dispatchVisit

subagent informCustomer:
  description: "Tells the customer the fault was fixed remotely."
  label: "Inform Customer"
  reasoning:
    instructions: ->
      | Tell the customer the fault on {!@generator.parseRequest.output.asset_id} was fixed remotely: {!@subagent.diagnose.output.detail}
    actions:
      comms: @actions.customer_comms_agent
  on_exit: ->
    transition to @echo.resolvedRemotely

${echo('resolvedRemotely', '"Resolved remotely: " + @subagent.diagnose.output.detail')}
orchestrator dispatchVisit:
  description: "Checks parts and weather, reserves the part and books a technician."
  label: "Dispatch Visit"
  system:
    instructions: |
      Check stock for the part and the weather for the town. Reserve the part with the parts agent,
      book a technician with the dispatch agent and inform the customer of the visit window.
      If the forecast is unsafe for outdoor work, book the next safe day instead.
  reasoning:
    instructions: ->
      | Asset {!@generator.parseRequest.output.asset_id} in {!@subagent.diagnose.output.town} needs part {!@subagent.diagnose.output.part_id}: {!@subagent.diagnose.output.detail}
    actions:
      stock: @actions.check_stock
      weather: @actions.get_forecast
      parts: @actions.parts_agent
      dispatch: @actions.dispatch_agent
      comms: @actions.customer_comms_agent
    max_number_of_loops: 8
  on_exit: ->
    transition to @echo.dispatched

${echo('dispatched', '@orchestrator.dispatchVisit.output')}`,
  },

  'v2-campaign-studio': {
    system: 'You build marketing campaigns. Nothing is scheduled without compliance approval and consented audiences.',
    actions: { content_agent: { a2a: 'content_agent' }, compliance_agent: { a2a: 'compliance_agent' }, get_segment: { mcp: 'segments_mcp', tool: 'get_segment' }, find_assets: { mcp: 'brand_assets_mcp', tool: 'find_assets' }, schedule_email: { mcp: 'email_mcp', tool: 'schedule_email', inputs: { segment_id: 'string', subject: 'string' } }, forecast: { mcp: 'analytics_mcp', tool: 'forecast' } },
    start: '@generator.brief',
    body: `generator brief:
  description: "Turns the request into a campaign brief."
  label: "Campaign Brief"
  prompt: ->
    | Extract the segment id (for example SEG-VIP), the channel and the theme from: ${MSG}
  outputs:
    properties:
${strProp('segment_id', 'Audience segment id')}
${enumProp('channel', 'Campaign channel', ['email', 'social'])}
${strProp('theme', 'Campaign theme')}
  on_exit: ->
    transition to @orchestrator.createCampaign

orchestrator createCampaign:
  description: "Checks the audience, writes copy, gets compliance approval and a forecast."
  label: "Create Campaign"
  system:
    instructions: |
      Check the segment size and consent, find brand assets for the theme, have the content agent write the copy,
      and have the compliance agent review it. Get a forecast for the segment and channel.
      Set approved to "yes" only when compliance approved and, for email, the segment has consented contacts.
      Return the email subject line in subject.
  reasoning:
    instructions: ->
      | Segment {!@generator.brief.output.segment_id}, channel {!@generator.brief.output.channel}, theme {!@generator.brief.output.theme}.
    actions:
      segment: @actions.get_segment
      assets: @actions.find_assets
      write: @actions.content_agent
      review: @actions.compliance_agent
      forecast: @actions.forecast
    max_number_of_loops: 8
    outputs:
      properties:
${enumProp('approved', 'Compliance and consent approved', ['yes', 'no'], '        ')}
${strProp('subject', 'Email subject or post headline', '        ')}
${strProp('summary', 'Copy, assets and forecast', '        ')}
  on_exit: ->
    transition to @router.launchRouter

router launchRouter:
  description: "Approved email campaigns are scheduled; approved social posts are handed over; the rest are returned."
  routes:
    - target: @executor.scheduleEmail
      when: @orchestrator.createCampaign.output.approved == "yes" and @generator.brief.output.channel == "email"
      label: "Email approved"
    - target: @echo.socialReady
      when: @orchestrator.createCampaign.output.approved == "yes"
      label: "Social approved"
  otherwise:
    target: @echo.rejected

executor scheduleEmail:
  description: "Schedules the approved email campaign."
  do: ->
    run @actions.schedule_email
      with segment_id = @generator.brief.output.segment_id
      with subject = @orchestrator.createCampaign.output.subject
  on_exit: ->
    transition to @echo.scheduled

${echo('scheduled', '"Email campaign scheduled for " + @generator.brief.output.segment_id + ". " + @orchestrator.createCampaign.output.summary')}
${echo('socialReady', '"Social post approved and ready to publish: " + @orchestrator.createCampaign.output.summary')}
${echo('rejected', '"Campaign not approved: " + @orchestrator.createCampaign.output.summary')}`,
  },
  'v2-supply-chain': {
    system: 'You are the supply chain control tower. Decide from shipment and stock data, never from guesses.',
    actions: { get_shipment: { mcp: 'shipments_mcp', tool: 'get_shipment' }, reroute_shipment: { mcp: 'shipments_mcp', tool: 'reroute_shipment', inputs: { shipment_id: 'string' } }, get_stock: { mcp: 'inventory_mcp', tool: 'get_stock' }, find_alternative_supplier: { mcp: 'supplier_mcp', tool: 'find_alternative_supplier' }, supplier_risk_agent: { a2a: 'supplier_risk_agent' }, logistics_agent: { a2a: 'logistics_agent' }, buyer_agent: { a2a: 'buyer_agent' }, customer_comms_agent: { a2a: 'customer_comms_agent' } },
    start: '@generator.extractDisruption',
    body: `generator extractDisruption:
  description: "Extracts the shipment id and the kind of disruption."
  label: "Extract Disruption"
  system:
    instructions: |
      Extract the shipment id (for example SHP-4401) and classify the disruption.
      Kind is "delay" for late shipments and "shortage" when the supplier cannot deliver the quantity.
  prompt: ->
    | ${MSG}
  outputs:
    properties:
${strProp('shipment_id', 'Shipment id, e.g. SHP-4401')}
${enumProp('kind', 'Kind of disruption', ['delay', 'shortage'])}
  on_exit: ->
    transition to @subagent.assessImpact

subagent assessImpact:
  description: "Reads the shipment and the stock cover of its SKU and rates the impact."
  label: "Assess Impact"
  system:
    instructions: |
      Get the shipment, then the stock of its SKU.
      Severity is "severe" when the delay in days is larger than the days of cover, otherwise "manageable".
  reasoning:
    instructions: ->
      | Shipment {!@generator.extractDisruption.output.shipment_id}, kind {!@generator.extractDisruption.output.kind}.
    actions:
      shipment: @actions.get_shipment
      stock: @actions.get_stock
    max_number_of_loops: 4
    outputs:
      properties:
${enumProp('severity', 'Impact on stock', ['severe', 'manageable'], '        ')}
${strProp('detail', 'SKU, delay and days of cover', '        ')}
  on_exit: ->
    transition to @router.mitigationRouter

router mitigationRouter:
  description: "Severe delays are rerouted, shortages get a new supplier, the rest a plan."
  routes:
    - target: @executor.reroute
      when: @subagent.assessImpact.output.severity == "severe" and @generator.extractDisruption.output.kind == "delay"
      label: "Severe delay"
    - target: @orchestrator.resource
      when: @generator.extractDisruption.output.kind == "shortage"
      label: "Shortage"
  otherwise:
    target: @subagent.mitigationPlan

executor reroute:
  description: "Switches the shipment to a faster mode (no LLM)."
  do: ->
    run @actions.reroute_shipment
      with shipment_id = @generator.extractDisruption.output.shipment_id
  on_exit: ->
    transition to @subagent.informCustomers

subagent informCustomers:
  description: "Tells the affected customers the new date."
  label: "Inform Customers"
  reasoning:
    instructions: ->
      | Shipment {!@generator.extractDisruption.output.shipment_id} was rerouted. Impact: {!@subagent.assessImpact.output.detail}. Inform the affected customers.
    actions:
      comms: @actions.customer_comms_agent
  on_exit: ->
    transition to @echo.rerouted

orchestrator resource:
  description: "Finds an alternative supplier, checks its risk and places the order."
  label: "Re-source"
  system:
    instructions: |
      Find approved alternative suppliers for the SKU, ask the supplier risk agent which one to use,
      then ask the buyer agent to place the order. Summarise supplier, quantity and delivery date.
  reasoning:
    instructions: ->
      | Shortage on shipment {!@generator.extractDisruption.output.shipment_id}: {!@subagent.assessImpact.output.detail}
    actions:
      alternatives: @actions.find_alternative_supplier
      risk: @actions.supplier_risk_agent
      buy: @actions.buyer_agent
    max_number_of_loops: 6
  on_exit: ->
    transition to @echo.resourced

subagent mitigationPlan:
  description: "Stock covers the delay: proposes a plan with the logistics agent."
  label: "Mitigation Plan"
  reasoning:
    instructions: ->
      | Stock covers the disruption of {!@generator.extractDisruption.output.shipment_id}: {!@subagent.assessImpact.output.detail}. Ask logistics for options and propose a plan.
    actions:
      logistics: @actions.logistics_agent
  on_exit: ->
    transition to @echo.planned

${echo('rerouted', '"Shipment " + @generator.extractDisruption.output.shipment_id + " rerouted. " + @subagent.informCustomers.output')}
${echo('resourced', '"Shortage handled: " + @orchestrator.resource.output')}
${echo('planned', '"No stock-out expected. " + @subagent.mitigationPlan.output')}`,
  },

  'v2-kyc-onboarding': {
    system: 'You are the onboarding desk of a bank. Never open an account before identity, sanctions and risk checks are done.',
    actions: { verify_document: { mcp: 'identity_mcp', tool: 'verify_document' }, screen_name: { mcp: 'sanctions_mcp', tool: 'screen_name' }, score_customer: { mcp: 'risk_mcp', tool: 'score_customer' }, open_case: { mcp: 'risk_mcp', tool: 'open_case', inputs: { applicant_id: 'string', reason: 'string' } }, kyc_analyst_agent: { a2a: 'kyc_analyst_agent' }, account_opening_agent: { a2a: 'account_opening_agent' } },
    start: '@generator.extractApplicant',
    body: `generator extractApplicant:
  description: "Extracts the applicant id."
  label: "Extract Applicant"
  system:
    instructions: |
      Extract the applicant id (for example AP-7001) and the applicant name. Use "UNKNOWN" when no id is given.
  prompt: ->
    | ${MSG}
  outputs:
    properties:
${strProp('applicant_id', 'Applicant id, e.g. AP-7001, or UNKNOWN')}
${strProp('name', 'Applicant name')}
  on_exit: ->
    transition to @router.idRouter

router idRouter:
  description: "Without an applicant id nothing can be checked."
  routes:
    - target: @subagent.screening
      when: @generator.extractApplicant.output.applicant_id != "UNKNOWN"
      label: "Has id"
  otherwise:
    target: @echo.needId

subagent screening:
  description: "Verifies the document, screens sanctions and scores the risk."
  label: "Screening"
  system:
    instructions: |
      Call all three checks for the applicant. Band is "high" when the sanctions screen has hits or the score band is high,
      "low" when the document is verified, there are no hits and the score band is low, otherwise "medium".
  reasoning:
    instructions: ->
      | Applicant {!@generator.extractApplicant.output.applicant_id}.
    actions:
      document: @actions.verify_document
      sanctions: @actions.screen_name
      score: @actions.score_customer
    max_number_of_loops: 5
    outputs:
      properties:
${enumProp('band', 'Overall risk band', ['low', 'medium', 'high'], '        ')}
${strProp('findings', 'Document, sanctions and score results', '        ')}
  on_exit: ->
    transition to @router.riskRouter

router riskRouter:
  description: "Low risk opens the account, high risk opens a compliance case, medium goes to an analyst."
  routes:
    - target: @subagent.openAccount
      when: @subagent.screening.output.band == "low"
      label: "Low risk"
    - target: @executor.openCase
      when: @subagent.screening.output.band == "high"
      label: "High risk"
  otherwise:
    target: @subagent.analystReview

subagent openAccount:
  description: "Opens the account."
  label: "Open Account"
  reasoning:
    instructions: ->
      | Open an account for {!@generator.extractApplicant.output.applicant_id} ({!@generator.extractApplicant.output.name}).
    actions:
      open: @actions.account_opening_agent
  on_exit: ->
    transition to @echo.opened

subagent analystReview:
  description: "A KYC analyst reviews the medium-risk applicant, then the account is opened if approved."
  label: "Analyst Review"
  reasoning:
    instructions: ->
      | Medium risk for {!@generator.extractApplicant.output.applicant_id}: {!@subagent.screening.output.findings}. Ask the KYC analyst for a decision; if approved, open the account.
    actions:
      review: @actions.kyc_analyst_agent
      open: @actions.account_opening_agent
    max_number_of_loops: 4
  on_exit: ->
    transition to @echo.reviewed

executor openCase:
  description: "Opens a compliance case (no LLM, no account)."
  do: ->
    run @actions.open_case
      with applicant_id = @generator.extractApplicant.output.applicant_id
      with reason = @subagent.screening.output.findings
  on_exit: ->
    transition to @echo.caseOpened

${echo('needId', '"Please give the applicant id (for example AP-7001) to start the onboarding."')}
${echo('opened', '"Onboarding complete for " + @generator.extractApplicant.output.applicant_id + ". " + @subagent.openAccount.output')}
${echo('reviewed', '"Analyst review for " + @generator.extractApplicant.output.applicant_id + ": " + @subagent.analystReview.output')}
${echo('caseOpened', '"No account opened for " + @generator.extractApplicant.output.applicant_id + ": a compliance case was opened. " + @subagent.screening.output.findings')}`,
  },

  'v2-incident-response': {
    system: 'You are the incident commander. Classify first, then act. Customer communication only for P1.',
    actions: { get_service_health: { mcp: 'monitoring_mcp', tool: 'get_service_health' }, create_incident: { mcp: 'itsm_mcp', tool: 'create_incident', inputs: { service: 'string', priority: 'string' } }, page_oncall: { mcp: 'itsm_mcp', tool: 'page_oncall' }, triage_agent: { a2a: 'triage_agent' }, network_agent: { a2a: 'network_agent' }, database_agent: { a2a: 'database_agent' }, app_support_agent: { a2a: 'app_support_agent' }, status_page_agent: { a2a: 'status_page_agent' } },
    start: '@generator.classifyIncident',
    body: `generator classifyIncident:
  description: "Classifies the incident: service, priority and area."
  label: "Classify Incident"
  system:
    instructions: |
      Extract the affected service (for example checkout-api, orders-db, vpn-zurich).
      Priority is "p1" when all users or revenue are affected, "p2" when one team or region is affected, else "p3".
      Area is "network" for VPN, DNS or connectivity, "database" for databases and replication, otherwise "application".
  prompt: ->
    | ${MSG}
  outputs:
    properties:
${strProp('service', 'Affected service')}
${enumProp('priority', 'Incident priority', ['p1', 'p2', 'p3'])}
${enumProp('area', 'Technical area', ['network', 'database', 'application'])}
  on_exit: ->
    transition to @executor.openTicket

executor openTicket:
  description: "Every incident gets a ticket first (no LLM)."
  do: ->
    run @actions.create_incident
      with service = @generator.classifyIncident.output.service
      with priority = @generator.classifyIncident.output.priority
  on_exit: ->
    transition to @router.priorityRouter

router priorityRouter:
  description: "P1 is a major incident; the rest go to the specialist of the area."
  routes:
    - target: @orchestrator.majorIncident
      when: @generator.classifyIncident.output.priority == "p1"
      label: "P1"
    - target: @subagent.network
      when: @generator.classifyIncident.output.area == "network"
      label: "Network"
    - target: @subagent.database
      when: @generator.classifyIncident.output.area == "database"
      label: "Database"
  otherwise:
    target: @subagent.application

orchestrator majorIncident:
  description: "Pages on-call, triages, fixes and posts a status update."
  label: "Major Incident"
  system:
    instructions: |
      Page the on-call engineer, check the service health, ask the triage agent for the cause,
      ask application support to fix it, then have the status page agent post an update. Summarise the timeline.
  reasoning:
    instructions: ->
      | P1 on {!@generator.classifyIncident.output.service}. Report: ${MSG}
    actions:
      page: @actions.page_oncall
      health: @actions.get_service_health
      triage: @actions.triage_agent
      fix: @actions.app_support_agent
      status: @actions.status_page_agent
    max_number_of_loops: 8
  on_exit: ->
    transition to @echo.majorDone

subagent network:
  description: "Network specialist."
  label: "Network"
  reasoning:
    instructions: ->
      | Diagnose {!@generator.classifyIncident.output.service}: ${MSG}
    actions:
      health: @actions.get_service_health
      diagnose: @actions.network_agent
  on_exit: ->
    transition to @echo.specialistDone

subagent database:
  description: "Database specialist."
  label: "Database"
  reasoning:
    instructions: ->
      | Diagnose {!@generator.classifyIncident.output.service}: ${MSG}
    actions:
      health: @actions.get_service_health
      diagnose: @actions.database_agent
  on_exit: ->
    transition to @echo.dbDone

subagent application:
  description: "Application specialist."
  label: "Application"
  reasoning:
    instructions: ->
      | Diagnose {!@generator.classifyIncident.output.service}: ${MSG}
    actions:
      health: @actions.get_service_health
      diagnose: @actions.app_support_agent
  on_exit: ->
    transition to @echo.appDone

${echo('majorDone', '"Major incident on " + @generator.classifyIncident.output.service + ". " + @orchestrator.majorIncident.output')}
${echo('specialistDone', '@generator.classifyIncident.output.service + " (" + @generator.classifyIncident.output.priority + "): " + @subagent.network.output')}
${echo('dbDone', '@generator.classifyIncident.output.service + " (" + @generator.classifyIncident.output.priority + "): " + @subagent.database.output')}
${echo('appDone', '@generator.classifyIncident.output.service + " (" + @generator.classifyIncident.output.priority + "): " + @subagent.application.output')}`,
  },
};
