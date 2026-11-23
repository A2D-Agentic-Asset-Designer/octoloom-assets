<span class="ol-pill">Design</span>

# Code view

<p class="lede"><strong>The text of the open file (YAML, AgentScript or JSON) with syntax colours and a find / replace widget, next to the visual editor.</strong> Some changes are faster in text; both views edit the same file.</p>

!!! info "Where to find it"
    **Visual / Code** switch in the toolbar

<figure markdown>
![Code view of agent-network.yaml](../assets/ui/code-yaml-annot-light.webp#only-light){ loading=lazy }
![Code view of agent-network.yaml](../assets/ui/code-yaml-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>Code view of agent-network.yaml</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **Agent Network 2.0** | Agent Network 2.0: AgentScript brokers (.agent) with explicit, deterministic flows. |
| <span class="ol-n">2</span> | **Visual** | Visual canvas |
| <span class="ol-n">3</span> | **Code** | YAML source |
| <span class="ol-n">4</span> | **Network** | Open the Agent Network view of the deployed network |
| <span class="ol-n">5</span> | **exchange.json** | Open the Exchange asset form of this project |
| <span class="ol-n">6</span> | **Build & Deploy** | Validate, build, publish and deploy this network |
| <span class="ol-n">7</span> | **Save** | Save the file (the YAML stays the source of truth) |
| <span class="ol-n">8</span> | **Ctrl+Space** | Ctrl+Space: suggestions · Shift+Alt+F: format · Ctrl/Cmd+S: apply · Ctrl/Cmd+F: find · Ctrl/Cmd+H: replace · F8: next problem |
| <span class="ol-n">9</span> | **Re-indent to the reference layout** | Re-indent to the reference layout: 2 spaces per level (Shift+Alt+F) |
| <span class="ol-n">10</span> | **Revert** | Undo the unsaved changes |
| <span class="ol-n">11</span> | **Apply** | Apply to the file (Ctrl/Cmd+S) |
| <span class="ol-n">12</span> | **Open in text editor** | Open the file as text |
| <span class="ol-n">13</span> | **Explain anything** | Explain anything: click, then click any object (the guided tour starts from here too). Drag to move; double-click to reset its place |

## How to use it

1. Click **Code** in the toolbar; **Visual** brings the canvas back.
2. Press **Ctrl/Cmd+F** to find, **Ctrl/Cmd+H** to replace.
3. Click **Save**: the canvas shows the change.

## More screenshots

<figure markdown>
![Find and replace](../assets/ui/code-find-light.webp#only-light){ loading=lazy }
![Find and replace](../assets/ui/code-find-dark.webp#only-dark){ loading=lazy }
<figcaption>Find and replace</figcaption>
</figure>

## In detail

Every editor has a **Code** tab with a full code editor, aware of the Agent Fabric v1 and v2 reference and of AgentScript.

- **Syntax colours** for `agent-network.yaml`, `brokers/*.agent` and `exchange.json`, following your VS Code theme: keys, values, quoted strings, numbers, comments, and `:` / list `-` in YAML.
- **Autocomplete** (IntelliSense) from the reference: keys valid at the cursor for v1 or v2, allowed values (authentication kinds, transports, platforms, input formats, A2A protocol bindings), names of declared agents, MCP servers, LLMs, connections and policies, `${variables}` from `exchange.json`. In AgentScript: node kinds, block keys, statements (`transition to`, `run`, `with`, `set`), `@` references (`@actions.…`, `@router.…`, `@variables.…`), A2A task states and MCP tool names.
- **Checks** while you type: syntax errors, the same validation as the Problems panel (for example references to missing components or connections, undeclared variables, an MCP connection URL that already ends with the server's transport path such as `/mcp`), keys that are not in the reference, and lines with off-level indentation. Errors, warnings and notes are counted in the toolbar; hover the underline or press <kbd>F8</kbd> for the next one.
- **Format** (<kbd>Shift</kbd>+<kbd>Alt</kbd>+<kbd>F</kbd>): re-indent to 2 spaces per level. Auto-indent on Enter, folding, bracket matching, find and replace like VS Code (<kbd>Ctrl/Cmd</kbd>+<kbd>F</kbd>, <kbd>Ctrl/Cmd</kbd>+<kbd>H</kbd>): a find box at the top right with match case, whole word and regex toggles, the match count, previous / next, select all, replace and replace all.
- **Apply** (<kbd>Ctrl/Cmd</kbd>+<kbd>S</kbd>) writes to the file, **Revert** drops your edits, **Open in text editor** opens the file in VS Code.



## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### Code view

The text of the file behind the canvas, with syntax colours (keys, values, strings, comments). Changes here and on the canvas are the same edit.

**When to use it:** To check or change the exact YAML or AgentScript.

**Examples and details:**

- Switch between Visual and the source in the toolbar
- Problems link to the line they are about
- Ctrl/Cmd+F finds, Ctrl/Cmd+H replaces: the find box at the top right works like VS Code (Aa match case, ab whole word, .* regex, Enter / Shift+Enter next and previous)

### Visual / Code

Switches between the visual editor (canvas or form) and the source text of the same file. Both edit the file itself; nothing is converted or stored elsewhere.

**When to use it:** Code for a quick text edit, search (Cmd/Ctrl+F) or to see exactly what is saved; Visual for everything else.

**Examples and details:**

- An edit in Code shows on the canvas at once
- YAML errors: Fix in code opens the line
