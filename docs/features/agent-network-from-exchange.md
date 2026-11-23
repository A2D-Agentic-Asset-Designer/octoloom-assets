<span class="ol-pill">Start</span>

# Network from Exchange

<p class="lede"><strong>Download an agent network published in your Exchange into a project folder and open it on the canvas.</strong> Continue work on a network someone else published, or bring a published version back to change it.</p>

!!! info "Where to find it"
    **Projects & Deploy → Exchange icon** · *Octoloom: Agent Network from Exchange*

<figure markdown>
![Agent network from Exchange: networks of the org, version picker and Save to](../assets/ui/exchange-import-annot-light.webp#only-light){ loading=lazy }
![Agent network from Exchange: networks of the org, version picker and Save to](../assets/ui/exchange-import-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>Agent network from Exchange: networks of the org, version picker and Save to</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **1.0.1** | Latest version |
| <span class="ol-n">2</span> | **Browse…** | Pick a folder |
| <span class="ol-n">3</span> | **Cancel** | Close without changes |
| <span class="ol-n">4</span> | **Download and open** | Download the asset and open it as a project |
| <span class="ol-n">5</span> | **Explain anything** | Explain anything: click, then click any object (the guided tour starts from here too). Drag to move; double-click to reset its place |

## How to use it

1. Click the **Exchange** icon next to **+** in Projects & Deploy.
2. Search and pick an agent network, then a **version**.
3. Choose **Save to** (workspace folder and new folder name).
4. Click **Download and open**: Octoloom adds the folder to the workspace and opens the canvas.

## More screenshots

<figure markdown>
![The From Exchange card in the new-project menu](../assets/ui/projects-new-exchange-light.webp#only-light){ loading=lazy }
![The From Exchange card in the new-project menu](../assets/ui/projects-new-exchange-dark.webp#only-dark){ loading=lazy }
<figcaption>The From Exchange card in the new-project menu</figcaption>
</figure>

## In detail

Continue work on an agent network that is already published in Exchange, by you on another machine or by a colleague. Click the **Exchange icon** next to **+** in Projects & Deploy, or choose **From Exchange** in the **+** menu. The dialog lists only **Agent Network** assets: your organization first, or everything you can see. You can search them and pick a version. Each one shows whether it is Deterministic (v2) or Probabilistic (v1).

**Download and open** saves the version's project files (`agent-network.yaml`, `exchange.json` and `brokers/*.agent`) in a **new folder** of your workspace folder. Existing folders are never overwritten: Octoloom adds `-2`, `-3`, and so on. The project is added to the workspace and opens on the canvas. Only read calls go to Exchange. Secrets are not part of the asset, so you set them again at deploy. If the `exchange.json` version is already in Exchange, bump it before the next Publish.



## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### Agent network from Exchange

Downloads an agent network that is published in Exchange (by you or a colleague) and opens it as an Octoloom project. The dialog lists only Agent Network assets, Deterministic and Probabilistic. The chosen version is saved in a new folder of your workspace, which is never overwritten.

**When to use it:** To reuse, review, govern or redeploy a network that lives in Exchange, or to continue work on another machine.

**Examples and details:**

- Click the Exchange icon next to + in Projects & Deploy, or choose From Exchange in the + menu
- Search by name, switch between your organization and everything you can see, and pick a version
- Secrets are not in Exchange: set them again when you deploy
- If the exchange.json version is already published, bump it before the next Publish
