# Toolbar buttons

The buttons at the top of every Octoloom editor.

## Visual / Code

Switches between the visual editor (canvas or form) and the source text of the same file. Both edit the file itself; nothing is converted or stored elsewhere.

**When to use it:** Code for a quick text edit, search (Cmd/Ctrl+F) or to see exactly what is saved; Visual for everything else.

**Examples:**

- An edit in Code shows on the canvas at once
- YAML errors: Fix in code opens the line

## Explorer

Shows or hides the outline of the flow on the left: sections, nodes and their order.

**When to use it:** To find a node in a long flow, or to make room for the canvas.

**Examples:**

- Click a node in the outline to select it on the canvas

## Network

Opens agent-network.yaml of this project on its canvas: the brokers, agents, MCP servers, LLMs and connections.

**When to use it:** To change what this broker connects to, or to build, publish and deploy the project.

**Examples:**

- From a flow: open the network the broker belongs to

## Network settings

Opens the settings of the whole network in the side panel: name, description (shown in Exchange) and other network-level fields.

**When to use it:** To change what Exchange shows for this network.

**Examples:**

- Set the description Exchange shows on the asset page

## Preview

A small chat panel beside the flow that sends messages to the deployed broker at a URL you enter (with an optional Authorization header). It talks to a running deployment; editing the flow changes nothing there until you publish and deploy again.

**When to use it:** To try the broker of this flow after a deploy without leaving the editor.

**Examples:**

- Paste the broker URL from Projects & Deploy
- For the full chat with traces, use the chat from Projects & Deploy

## New Version

Sets the next Major, Minor or Patch version in exchange.json and saves all files. It starts from the highest version already in Exchange, so the new number is always free. Nothing is published yet.

**When to use it:** Once before each publish of a change. Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again.

**Examples:**

- Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again
- Deploy with "Publish before deploy" publishes this same version
- No bump is needed to deploy a version that is already published: turn Publish before deploy off
- Major for a breaking change, Minor for new features, Patch for fixes

## Commit Version

Bumps the patch version in exchange.json to the next free one (from the highest in Exchange) and saves all files. It is the quick form of New Version → Patch. It does not publish, and it is not a Git commit.

**When to use it:** After a change, before Publish (or a deploy that publishes).

**Examples:**

- 1.0.3 is the highest in Exchange, exchange.json says 1.0.1: Commit Version sets 1.0.4
- Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again
- Then Publish (or Deploy with Publish before deploy)

## Bump patch

Raises the patch number of the version in this form by one (the tooltip shows the result). Save to keep it. It counts from this file only; New Version and Commit Version in the flow editor also look at Exchange.

**When to use it:** Before the next Publish of a change.

**Examples:**

- 1.0.0 → 1.0.1
- Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again

## exchange.json

Opens the Exchange descriptor of this project in its form: name, version, variables, dependencies and runtime limits.

**When to use it:** To change the version, a variable default or what Exchange shows.

**Examples:**

- Set a variable default for deploy and local runs

## Build & Deploy

The project actions: Validate (dry run, changes nothing), Build (local package), Publish (to Exchange, the version in exchange.json), Deploy… (to a gateway), Setup gateways… and Undeploy….

**When to use it:** To ship the network. Validate first when unsure.

**Examples:**

- Publish uses the version in exchange.json as it is and never bumps it; a version already in Exchange can't be published again
- Deploy… opens the same form as the rocket in Projects & Deploy

## Save

Saves this file (the same as Cmd/Ctrl+S). The canvas and the form edit the file text, so what you see is what is saved.

**When to use it:** Whenever you want the change on disk; Build and Publish use saved files.

**Examples:**

- Unsaved changes show a dot on the editor tab
