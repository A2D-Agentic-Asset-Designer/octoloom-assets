<span class="ol-pill">Design</span>

# exchange.json form

<p class="lede"><strong>A no-code form for `exchange.json`: the asset name, version, description, tags, variables and dependencies Exchange shows.</strong> Exchange metadata without editing JSON; protected defaults are locked so you don't break the publish.</p>

!!! info "Where to find it"
    **exchange.json** in the toolbar

<figure markdown>
![The exchange.json form with protected defaults locked](../assets/ui/exchange-locked-annot-light.webp#only-light){ loading=lazy }
![The exchange.json form with protected defaults locked](../assets/ui/exchange-locked-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>The exchange.json form with protected defaults locked</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **Form** | Show the form view |
| <span class="ol-n">2</span> | **JSON** | JSON source |
| <span class="ol-n">3</span> | **Bump patch** | → 1.0.1 |
| <span class="ol-n">4</span> | **Network** | Open the Agent Network view of the deployed network |
| <span class="ol-n">5</span> | **Save** | Save the file (the YAML stays the source of truth) |
| <span class="ol-n">6</span> | **Fix** | Fix: Copy the exchange.json description. One undoable edit; not saved. |
| <span class="ol-n">7</span> | **×** | Remove |
| <span class="ol-n">8</span> | **Unlock to edit** | Unlock the generated file to edit it by hand |
| <span class="ol-n">9</span> | **Add variable** |  |
| <span class="ol-n">10</span> | **Remove group** | Remove this group |
| <span class="ol-n">11</span> | **Add group** |  |
| <span class="ol-n">12</span> | **Explain anything** | Explain anything: click, then click any object (the guided tour starts from here too). Drag to move; double-click to reset its place |

## How to use it

1. Click **exchange.json** in the toolbar.
2. Fill in name, description and tags; add **variables** for every URL.
3. Open a **lock** to change a protected default.
4. Click **Save**, then publish from Projects & Deploy.

## More screenshots

<figure markdown>
![Both locks open: protected fields and dependencies](../assets/ui/exchange-unlocked-light.webp#only-light){ loading=lazy }
![Both locks open: protected fields and dependencies](../assets/ui/exchange-unlocked-dark.webp#only-dark){ loading=lazy }
<figcaption>Both locks open: protected fields and dependencies</figcaption>
</figure>

## In detail

A form for the Exchange descriptor: asset identity, version, variables and their defaults (secrets are masked), and dependencies.

## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### exchange.json editor

A form over the exchange.json of a project: its name, version, variables and the Exchange assets it depends on. The fields that must match agent-network.yaml and the connected organization (Group ID, Organization ID, classifier, main, descriptor version) and the dependency list sit behind a lock: read-only each time the form opens, one click on the lock opens them for editing, another click locks them again. The JSON view always edits everything, and the file stays a normal file in the Explorer. Under Asset, the network description is the one Exchange shows on the asset page; it comes from agent-network.yaml. Findings about the project show at the top with a Fix button.

**When to use it:** Before publishing, or when a dependency or variable changes.

**Examples and details:**

- Bump the version before a new publish
- Click the lock on Protected Exchange defaults to change the Group ID, click it again to lock it
- "main is net.yaml": click Set main to agent-network.yaml
- Network description empty: click Copy the exchange.json description, it never overwrites one that is there

### exchange.json

Opens the Exchange descriptor of this project in its form: name, version, variables, dependencies and runtime limits.

**When to use it:** To change the version, a variable default or what Exchange shows.

**Examples and details:**

- Set a variable default for deploy and local runs
