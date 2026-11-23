// octoloom#302: progress updates for v2 (AgentScript) brokers.
// In front of every step (generator, subagent, orchestrator, executor) the flow gets one Reply node
// with state TASK_STATE_WORKING and a plain sentence made from the step's description. Every
// transition / router target that pointed at the step goes through its Reply first, so the chat
// (Live on, octoloom#292) shows what the broker is doing. An echo costs no LLM call.
// Usage as a module: addProgress(agentText) -> agentText. CLI: node progress.mjs <file.agent>... (in place)
import fs from 'node:fs';

const STEP = /^(generator|subagent|orchestrator|executor) ([A-Za-z_][A-Za-z0-9_]*):\s*$/;
const DOUBLE = new Set(['Puts', 'Refers', 'Gets', 'Sets', 'Plans', 'Ships', 'Runs']);
// Hand-written lines where the description doesn't read well as "<verb>ing ...".
const OVERRIDE = {
  createCampaign: 'Checking the audience, writing the copy, getting compliance approval and a forecast...',
  diagnose: 'Looking up the asset and running remote diagnostics...',
  dispatchVisit: 'Checking parts and weather, reserving the part and booking a technician...',
  customerAddress: 'Verifying the address (from the request or the master record)...',
  verifyAddress: 'Verifying and standardizing the address...',
  classifyIncident: 'Classifying the incident: service, priority and area...',
  openTicket: 'Opening the incident ticket...',
  majorIncident: 'Major incident: paging on-call, triaging, fixing and posting a status update...',
  network: 'Handing over to the network specialist...',
  database: 'Handing over to the database specialist...',
  application: 'Handing over to the application specialist...',
  assessClaim: 'Recording the FNOL, checking coverage and screening for fraud...',
  settleClaim: 'Creating the claim, getting a settlement and paying it...',
  screening: 'Verifying the document, screening sanctions and scoring the risk...',
  analystReview: 'A KYC analyst reviews the medium-risk applicant...',
  notifyApproval: 'Generating the contract and notifying the applicant...',
  explainDecline: 'Explaining why the return is declined and looking for alternatives...',
  assessImpact: 'Reading the shipment and the stock cover of its SKU, rating the impact...',
  resource: 'Finding an alternative supplier, checking its risk and placing the order...',
  classifyClaim: 'Classifying the loss and reading the policy id...',
  catalog: 'Finding governed data assets in CDGC and reading their data quality score...',
  mitigationPlan: 'Stock covers the delay: planning with the logistics agent...',
};

/** "Checks the free seats." -> "Checking the free seats..."; undefined when it doesn't start with a verb. */
export function gerund(description) {
  const d = description.replace(/\s*\([^)]*\)/g, '').replace(/[.\s]+$/, '').trim();
  const m = d.match(/^([A-Z][a-z]+s)\b(.*)$/);
  if (!m || /:/.test(d.split(' ').slice(0, 3).join(' '))) return undefined;
  let [, w, rest] = m;
  let g;
  if (DOUBLE.has(w)) g = w.slice(0, -1) + w.slice(-2, -1) + 'ing';
  else if (/ies$/.test(w)) g = w.slice(0, -3) + 'ying';
  else if (/(ch|sh|ss|x)es$/.test(w)) g = w.slice(0, -2) + 'ing';
  else if (/ees$/.test(w)) g = w.slice(0, -1) + 'ing';
  else if (/es$/.test(w) && !/[aeiou]es$/.test(w.slice(0, -1) + 's')) g = w.slice(0, -2) + 'ing';
  else g = w.slice(0, -1).replace(/e$/, '') + 'ing';
  return `${g}${rest}...`;
}

const human = (name) => name.replace(/([a-z0-9])([A-Z])/g, '$1 $2').replace(/_/g, ' ').toLowerCase();
const cap = (s) => s[0].toUpperCase() + s.slice(1);
const quote = (s) => JSON.stringify(s);

export function addProgress(text) {
  if (/state: "TASK_STATE_WORKING"/.test(text)) return text; // already has progress updates
  const lines = text.split('\n');
  const steps = [];
  for (let i = 0; i < lines.length; i++) {
    const m = lines[i].match(STEP);
    if (!m) continue;
    const desc = (lines.slice(i + 1, i + 4).find((l) => /^  description: /.test(l)) || '').replace(/^  description: /, '').replace(/^"|"$/g, '');
    const label = (lines.slice(i + 1, i + 5).find((l) => /^  label: /.test(l)) || '').replace(/^  label: /, '').replace(/^"|"$/g, '');
    steps.push({ kind: m[1], name: m[2], line: i, msg: OVERRIDE[m[2]] ?? gerund(desc) ?? `${cap(label ? label.toLowerCase() : human(m[2]))}...` });
  }
  if (!steps.length) return text;
  const echoName = (s) => `progress${s.name[0].toUpperCase()}${s.name.slice(1)}`;
  // Redirect references to each step (transition to / target:), never `.output` reads.
  let body = lines.join('\n');
  for (const s of steps) {
    const re = new RegExp(`((?:transition to|target:)\\s*)@${s.kind}\\.${s.name}\\b(?![.\\w])`, 'g');
    body = body.replace(re, `$1@echo.${echoName(s)}`);
  }
  // All Replies go at the end of the file, in step order: the first echo in the file stays the final
  // reply, which the flow editor uses as the default next step of a new node (agentModel / componentTemplates).
  const out = body.replace(/\s+$/, '').split('\n');
  out.push('', '# Progress updates (octoloom#302): each one tells the caller what the broker does next, then', '# moves on to that step. With Live on, the chat shows them while the broker works. No LLM call.');
  for (const s of steps) {
    out.push('',
      `echo ${echoName(s)}:`,
      `  kind: "a2a:status_update_event"`,
      `  state: "TASK_STATE_WORKING"`,
      `  message: a2a.message({messageId: uuid(), parts: [a2a.textPart(${quote(s.msg)})]})`,
      `  on_exit: ->`,
      `    transition to @${s.kind}.${s.name}`);
  }
  out.push('');
  return out.join('\n');
}

if (process.argv[1] && process.argv[1].endsWith('progress.mjs')) {
  for (const f of process.argv.slice(2)) fs.writeFileSync(f, addProgress(fs.readFileSync(f, 'utf8')));
}
