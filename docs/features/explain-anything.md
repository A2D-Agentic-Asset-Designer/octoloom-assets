<span class="ol-pill">Help</span>

# Explain anything

<p class="lede"><strong>Click the button, then any object: a panel explains what it is, when to use it and gives examples. It also starts the guided tour.</strong> Help where you are, in the same words as this site's UI reference.</p>

!!! info "Where to find it"
    The floating **i** button, bottom right of every Octoloom view

<figure markdown>
![Explain on the network canvas](../assets/ui/explain-anything-light.webp#only-light){ loading=lazy }
![Explain on the network canvas](../assets/ui/explain-anything-dark.webp#only-dark){ loading=lazy }
<figcaption>Explain on the network canvas</figcaption>
</figure>

## How to use it

1. Click the floating **Explain** button.
2. Click any button, card or panel.
3. Use **Start the guide** for the tour of this view.
4. Click **Docs** on a card to open this site with a search for that object.

## More screenshots

<figure markdown>
![The Explain panel with the guided tour](../assets/ui/explain-guide-light.webp#only-light){ loading=lazy }
![The Explain panel with the guided tour](../assets/ui/explain-guide-dark.webp#only-dark){ loading=lazy }
<figcaption>The Explain panel with the guided tour</figcaption>
</figure>

<figure markdown>
![The Docs link at the end of every Explain card opens this site](../assets/ui/explain-docs-light.webp#only-light){ loading=lazy }
![The Docs link at the end of every Explain card opens this site](../assets/ui/explain-docs-dark.webp#only-dark){ loading=lazy }
<figcaption>The Docs link at the end of every Explain card opens this site</figcaption>
</figure>

## In detail

Every Octoloom editor and panel (canvases, broker flow, `exchange.json`, chat, Governance, Welcome, New project) has one round, dark blue **info button** floating near the bottom right, above the minimap. It replaces the Explain buttons the views used to have. Click it (or focus it and press Enter) to turn on Explain mode:

- **Hover** any object: it is outlined and named (Broker, Agent, Canvas tools, Problems, Trace…).
- **Click** it: the click is not passed to the view, so nothing is changed, opened or deployed. A card opens beside the object with what it is, when to use it and examples. For a card, it also shows the object's own name.
- **Click another object** to explain it next; **Esc** closes the card, and Esc again (or the info button) leaves Explain mode.
- **Start the guide:** on the network canvas and the broker flow, the hint next to the button (and each explanation card) has **Start the guide**, which replays the guided tour of that canvas.
- **Docs:** every explanation card has a **Docs** link. It opens the [Octoloom documentation site](https://octoloom.a2d-ai.com/) with a search for that object.
- **Toolbar and project buttons** each have their own card (Visual / Code, Preview, New Version, Commit Version, Build, Publish, Run locally…). The Publish card says how versions work: Publish uses the version in `exchange.json` as it is and never bumps it, and a version already in Exchange can't be published again.
- **Drag** the button anywhere. It feels like one button: every open Octoloom tab follows, so it is in the same place when you switch tabs (and after a restart). In a split view each editor group shows its own copy at that place. Double-click it to put it back everywhere.



## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### Explain anything

<div class="grid" markdown>

![explain-button](../assets/ui/explain-button-light.webp#only-light){ loading=lazy }
![explain-button](../assets/ui/explain-button-dark.webp#only-dark){ loading=lazy }

The floating info button on every Octoloom editor and panel (canvases, broker flow, chat, Governance, Welcome, New project). Turn it on, then click any card, panel, tool or canvas: instead of acting, the view tells you what that object is, when to use it and examples. Nothing is changed while it is on. Every card has a Docs link that opens the Octoloom documentation site (octoloom.a2d-ai.com) with a search for the object.

**When to use it:** Whenever you are unsure what something on screen does. Drag the button anywhere; every Octoloom tab follows, so it stays in the same place when you switch tabs.

</div>

**Examples and details:**

- Click the button (or press Enter on it), then click a broker card to read about brokers
- Hover first: the object that will be explained is outlined and named
- Esc, the close button or the info button again leaves Explain mode
- Drag the button out of the way; double-click it to put it back in its default place
