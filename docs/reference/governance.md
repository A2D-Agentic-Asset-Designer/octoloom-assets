# Governance

Local compliance checks with rulesets.

## Governance

Checks a project against governance rulesets with the Anypoint CLI (anypoint-cli-v4 governance api validate). Results are shown on a read-only canvas: brokers, agents and MCP servers with findings get a shield badge (red = violation, amber = warning, blue = info), and every finding has a fix based on the v1 or v2 reference. A local compliance check only: the selection and results are saved in VS Code (workspace storage), never in the project, and build, publish and deploy ignore them. Nothing is created or published in your organization or in P4A.

**When to use it:** Before you publish or deploy, or to check a project against your company standards.

**Examples:**

- Select "Agent Network Best Practices" (Agent Fabric) and press Validate
- Click a marked component to see only its findings, then Open on canvas to edit it
- Fix (per finding) or Fix all: Octoloom changes agent-network.yaml with keys from the v1 / v2 reference (for example capabilities on a card, interfaces.a2a.authorization.allowAnonymousAccess: false on a v2 broker, a streamableHttp transport, the allowed tools, secrets moved to exchange.json variables), saves it and validates again. Undo with Ctrl/Cmd+Z in the file
- MCP tool rules written for MCP server specs (tool hints, closed input, output schema) are reported for every tool in agent-network.yaml, whatever it declares. Fix all skips them, so its count is what it can clear; each one keeps its own Fix to write the reference keys anyway
- Findings that need a decision (which policy, provider or URL) keep the snippet to copy; v1 brokers have no authorization block, so those findings suggest a policy instead
- Drag the edges of the Rulesets and Conformance columns to resize them; the arrow buttons hide or show them
- Governed services and Configuration (above the canvas) show conformance per service and the rules of each selected ruleset
- The selection is saved per project; validate again after a change

## Rulesets

A ruleset is a governance profile (YAML) of rules with a severity. Octoloom lists only rulesets that apply to agent networks: A2A Broker (agents.Broker), A2A agents (agent cards, tools) and MCP servers (mcp.*). Sources: Agent Fabric (MuleSoft, from Exchange), P4A community rulesets and your own P4A rulesets (P4A token), rulesets published in your organization (downloaded read-only from Exchange) and local YAML files.

**When to use it:** Choose the rulesets that match the standards of the project. Combine several: findings name the rule and the ruleset.

**Examples:**

- Agent Network Best Practices: agent card fields, broker authorization, MCP transport, inline secrets
- P4A MCP Server Safety: tool side-effect hints, closed input schemas, declared auth
- Your organization: custom rulesets your team published to Exchange
- Local file: a ruleset YAML you are writing (+ in Local files)

## Governance report

The workspace report lists every agent network project in the workspace: conformance and identified issues across all governed services, one row per project, then each canvas with its marked components. Validate all checks every project that has rulesets selected. Report / Workspace report saves a stand-alone HTML file: an overview (conformance, issues, governed services table), a section per service with its rules (expand a rule to see each finding and its fix) and a Configuration tab with the scope and every rule of the selected rulesets (light and dark, no scripts). Reports are saved outside your projects by default (Octoloom storage), so they are never published or deployed.

**When to use it:** Reviews, audits, or sharing the state of all projects with your team.

**Examples:**

- Workspace report → Validate all → Workspace report (HTML)
- Project → Report: one project only
- Open a project from the report to fix its findings
