# Canvases and editors

The editors, the canvas tools and the panels around them.

## Agent network canvas

The canvas of one agent network file: brokers, agents, MCP servers, LLMs, connections and policies as cards with edges between them. It edits the YAML, which stays the source of truth.

**When to use it:** Designing or reviewing a network.

**Examples:**

- Drag from a port to another card to connect them
- Select a card to edit it in the inspector
- Use the zoom bar, minimap and Minimize all to find your way in a large network
- Hover a button of the tool stack on the left (+ Add, Asset Palette, Auto layout, Minimize all) to see its name
- A dashed icon tile (in the card's colour) marks an external asset: an agent, MCP server or LLM referenced from Exchange (exchange.json dependency) and not declared in this project

## AgentScript flow

The canvas of one .agent file: its nodes (trigger, generator, router, sub-agent, orchestrator, executor, echo) and the paths between them. It edits the AgentScript text.

**When to use it:** Designing the behaviour of one agent.

**Examples:**

- Add a node from the palette on the left
- Select a node to edit it in the inspector
- Switch to the code view to see the AgentScript

## Inspector

The properties of the selected card or node. Edits go straight into the file.

**When to use it:** After selecting something on the canvas.

**Examples:**

- Drag its left edge to resize it; the width is kept
- Close it to give the canvas more room

## Canvas tools

The zoom bar, minimap and floating buttons of a canvas: zoom, fit, auto layout, Minimize all / Open all and the map of the whole canvas.

**When to use it:** Finding your way in a large canvas.

**Examples:**

- Fit shows every card
- Click the minimap to jump there
- Minimize all turns every card into its icon

## Flow outline

The outline of the .agent file on the left: every node by kind, and the palette of nodes you can add.

**When to use it:** To find a node in a long flow or add a new one.

**Examples:**

- Click a node in the outline to select it on the canvas
- Drag a node kind from the palette onto the canvas

## Problems

The validation findings of this file and the project checks across agent-network.yaml, exchange.json and the broker .agent files: errors, warnings and hints with the object they are about. A finding with a fix has a button that applies it as one edit: one Undo reverts every file it changed, and nothing is saved until you save. The same findings are in the VS Code Problems panel with a light bulb quick fix. When you save agent-network.yaml or a .agent file, variables it uses that exchange.json does not declare are added there (unsaved; setting agentNetwork.syncVariablesOnSave turns this off).

**When to use it:** Before a build or deploy; errors stop the build.

**Examples:**

- Click a problem to select the card it is about; in a broker flow it also opens the field the problem is about (for example Go to or Prompt)
- Collapse the bar with its chevron
- Two brokers share brokers/sales.agent: click Copy the flow to brokers/support.agent
- Variable ${crm.url} is not declared: click Add to exchange.json
- Renaming a broker offers to rename its .agent file too
- A flow path ends without a final reply: click Go to the final reply (done) to wire it (setting agentNetwork.flowCoach turns this suggestion off)
- The broker flow checks what Agent Fabric rejects at build or deploy: one trigger per interface, no transition back to the trigger, every path ending in a completed, failed, canceled or rejected reply, empty prompts, unknown LLM settings and out-of-range temperature or top_p
- Network checks: a broker card needs a description and unique skill ids; amazonSigv4 is for LLM connections only; a TLS context needs both name and group; OBJECT_STORE_DEFAULT_TTL_MS is at most 30 days
- Deleting an agent or MCP server also removes the flow actions that called it and the variables only it used, in one Undo; a message says what went with it

## Code view

The text of the file behind the canvas, with syntax colours (keys, values, strings, comments). Changes here and on the canvas are the same edit.

**When to use it:** To check or change the exact YAML or AgentScript.

**Examples:**

- Switch between Visual and the source in the toolbar
- Problems link to the line they are about
- Ctrl/Cmd+F finds, Ctrl/Cmd+H replaces: the find box at the top right works like VS Code (Aa match case, ab whole word, .* regex, Enter / Shift+Enter next and previous)

## exchange.json editor

A form over the exchange.json of a project: its name, version, variables and the Exchange assets it depends on. The fields that must match agent-network.yaml and the connected organization (Group ID, Organization ID, classifier, main, descriptor version) and the dependency list sit behind a lock: read-only each time the form opens, one click on the lock opens them for editing, another click locks them again. The JSON view always edits everything, and the file stays a normal file in the Explorer. Under Asset, the network description is the one Exchange shows on the asset page; it comes from agent-network.yaml. Findings about the project show at the top with a Fix button.

**When to use it:** Before publishing, or when a dependency or variable changes.

**Examples:**

- Bump the version before a new publish
- Click the lock on Protected Exchange defaults to change the Group ID, click it again to lock it
- "main is net.yaml": click Set main to agent-network.yaml
- Network description empty: click Copy the exchange.json description, it never overwrites one that is there

## Minimize to icons

Shrinks a card to just its icon tile and name, so large networks and flows show what is orchestrated without the details. Connections stay drawn between the icons. The choice is saved with the canvas layout (not in your YAML or .agent file).

**When to use it:** Reviewing or presenting a network with many brokers, agents and MCP servers, or a long AgentScript flow.

**Examples:**

- Minimize all (canvas button): every card becomes an icon; press it again (Open all) to restore every card
- Click the icon tile in a card header to minimize only that card
- Click a minimized icon to open that card again; double-click still opens or edits it as before
- Auto layout packs minimized icons tightly
- Drag any card to move it, in every state: open, collapsed or minimized, also by its icon tile or chevron. A drag moves the card; only a click minimizes, opens or collapses it

## Patterns

Patterns insert several wired nodes at once from + Step or the right-click menu: logical case selection, check then act, extract then run a tool, error handling (status output + failed reply), retry once then fail, human in the loop (ask one question when details are missing) and guardrail check (blocked requests end as rejected). Names are made unique and the last node links to the existing reply.

**When to use it:** You need a common flow shape: replace the placeholder instructions and conditions afterwards. Matching instruction templates (Error handling, Retry, Ask the user, Guardrail screen) are in the Insert template picker.

**Examples:**

- Error handling: subagent status ok / failed → router → reply or FAILED with the error
- Retry once: attempt → router → second attempt with the first error → router → FAILED
- Human in the loop: generator complete yes / no → question reply or continue
- Guardrail check: generator allowed / blocked → REJECTED with reason or continue

## Toolbar

The actions of this file: switch between the canvas and its source, the guided tour (Guide) and the file actions.

**When to use it:** Any time; hover a button for what it does.

**Examples:**

- Guide replays the tour of this canvas
- To learn what a card or tool is, use the floating info button
- With Explain on, click a toolbar button for its own card (New Version, Commit Version, Bump patch, Save…)
