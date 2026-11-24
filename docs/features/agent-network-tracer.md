<span class="ol-pill">Chat and observe</span>

# Agent Network Tracer

<p class="lede"><strong>The tasks of a broker from the Agent Fabric logs: the path each task took through the flow, its story, messages and raw logs.</strong> Understand what a broker did for a real request, after the fact.</p>

!!! info "Where to find it"
    Chat → **Show the tracer** · the Tracer icon under a reply

<figure markdown>
![The Agent Network Tracer: tasks, the path on the broker graph, the story](../assets/ui/tracer-annot-light.webp#only-light){ loading=lazy }
![The Agent Network Tracer: tasks, the path on the broker graph, the story](../assets/ui/tracer-annot-dark.webp#only-dark){ loading=lazy }
<figcaption>The Agent Network Tracer: tasks, the path on the broker graph, the story</figcaption>
</figure>

| # | Control | What it does |
|---|---|---|
| <span class="ol-n">1</span> | **Collapse the left side** | Collapse the left side (the chat keeps the space) |
| <span class="ol-n">2</span> | **Network** | The agent network (read-only) |
| <span class="ol-n">3</span> | **The trace of a reply** | The trace of a reply: pick the trace icon under a deployed reply |
| <span class="ol-n">4</span> | **Deployed and running · Sandbox / example** | Deployed and running · Sandbox / example-gateway |
| <span class="ol-n">5</span> | **Check status** | Ask Agent Fabric for the deployment status |
| <span class="ol-n">6</span> | **Load the trace again** | Reload the trace |
| <span class="ol-n">7</span> | **Full height** | Full height: the trace takes the whole panel |
| <span class="ol-n">8</span> | **Back to the network** | Return to the network canvas |
| <span class="ol-n">9</span> | **Broker** | Broker: The broker that handles the message, and its gateway request. Click to choose its colour. |
| <span class="ol-n">10</span> | **Agent** | Agent: A2A calls to agents. Click to choose its colour. |
| <span class="ol-n">11</span> | **LLM** | LLM: Calls to a language model (OpenAI, Gemini, Bedrock, Azure…). Click to choose its colour. |
| <span class="ol-n">12</span> | **MCP** | MCP: MCP tool calls (tools/call). Click to choose its colour. |
| <span class="ol-n">13</span> | **Error** | Error: A span that failed, whatever it calls. Click to choose its colour. |
| <span class="ol-n">14</span> | **Running** | Show only the running deployments |
| <span class="ol-n">15</span> | **Deployed** | The broker deployed to your gateway |
| <span class="ol-n">16</span> | **Local** | The broker running on this machine (Run locally, Docker) |
| <span class="ol-n">17</span> | **Use another URL** | Chat with a broker at a different URL |
| <span class="ol-n">18</span> | **Copy URL** | Copy the broker URL |
| <span class="ol-n">19</span> | **Authentication** | Authentication: none |
| <span class="ol-n">20</span> | **Show raw JSON for every reply** | Show the raw A2A JSON under each reply |
| <span class="ol-n">21</span> | **New conversation** | New conversation (new context) |
| <span class="ol-n">22</span> | **Share this broker** | Share this broker: A²D sessions (invite people by email, see their feedback here) or a web chat app (opens a dialog) |
| <span class="ol-n">23</span> | **Full height** | Full height: the chat takes the whole panel |
| <span class="ol-n">24</span> | **Collapse the chat** | Collapse the chat (the left side keeps the space) |
| <span class="ol-n">25</span> | **Live progress is on** | Live progress is on: you see each step of the broker as it happens. Click to turn it off. |
| <span class="ol-n">26</span> | **Send** | Send (Enter) |
| <span class="ol-n">27</span> | **Hide the tracer** | Hide the tracer panel |
| <span class="ol-n">28</span> | **App 1/1** | Tracing with the Agent Fabric connected app · 1 of 1 APIs reachable. Click for details. |

## How to use it

1. Open the tracer at the bottom of the chat.

2. Pick a task on the left.

3. Read the path on the **Graph** (or **Tree**, **List**); the detail column shows **Story**, **Message**, **Log** and **Raw**.

    <figure markdown>
    ![The tracer with every node minimized](../assets/ui/tracer-mini-light.webp#only-light){ loading=lazy }
    ![The tracer with every node minimized](../assets/ui/tracer-mini-dark.webp#only-dark){ loading=lazy }
    <figcaption>The tracer with every node minimized</figcaption>
    </figure>

## In detail

Click the **Tracer** button on a project's **Deployed and running** box in Projects & Deploy, or the **Tracer** icon under a deployed chat reply. The chat panel opens with the Tracer below the network and the chat. The **Full height** icon at the right end of the Tracer header hides the network and the chat; press it again to bring them back.

- **Tasks** (left): the broker's tasks in the period you pick, newest first, with their nodes, time and tools. Error-only runs are marked in red. Opening a task also shows its span waterfall in the chat's **Trace** view above (top left).
- **Task** (middle): **Graph** draws the broker's `.agent` flow with Octoloom's own cards and the path the task took: numbered hops, and dimmed nodes it didn't reach. **Minimize all** (the workflow icon at the top left of the graph, one node branching to two) turns the cards into icons, as on the flow canvas, so long flows fit; press it again (**Open all**, two linked cards) to bring them back. **Tree** lists the nodes in order (iterations for v1 brokers) and **List** shows every log line.

  - **Detail** (right): **Status** (data sources), **Story** (the conversation, node outputs and failed tools the broker stored), **Message**, **Metadata**, **Log**, **Raw** and **JSON**. The task's Observability spans are in the chat's **Trace** view above, which opens when you open the task.
- **JSON** is the whole task as one document (`octoloom.tracer.task/v1`) or NDJSON, to send to Splunk or Datadog. Credentials are masked.
- Drag the edges of the Tasks and Detail columns to resize them; the arrow buttons hide or show them.
- **Read-only**: the Tracer only reads from Log Search, runtime logs, Object Store and Observability, and never changes anything in your organization. The organization, environment and broker come from the project's deployment. The Agent Fabric connected app makes the calls from VS Code; tokens never reach the webview.
- The **access pill** (for example *App 10/10*) checks each Anypoint API the Tracer uses. When one fails, it names the permission to add to the connected app, or offers to trace with your own Anypoint Code Builder sign-in instead. The choice is remembered per connection.
- Deployed brokers only: local runs have no Anypoint logs.

## Buttons and components

The same text as the in-app **Explain** button (click the floating **i**, then the item).

### Agent Network Tracer

Shows what a deployed broker did for each task: the nodes it ran, the tools and LLMs it called, what failed and why. Read-only: it only reads logs and task state from Anypoint (Log Search, runtime logs, Object Store and Observability spans) and never changes anything in your organization. The organization, environment and broker come from the project's deployment, and the Agent Fabric connected app makes the calls. Three columns: Tasks, the task (Graph, Tree or List) and the detail of what you pick.

**When to use it:** After a chat turn or a failed task on a deployed broker, to see the path it took and where it went wrong. It needs a deployed, running broker: local runs have no Anypoint logs.

<figure markdown>
![The Agent Network Tracer: tasks, the path on the broker graph, the story](../assets/ui/tracer-light.webp#only-light){ loading=lazy }
![The Agent Network Tracer: tasks, the path on the broker graph, the story](../assets/ui/tracer-dark.webp#only-dark){ loading=lazy }
<figcaption>The Agent Network Tracer: tasks, the path on the broker graph, the story</figcaption>
</figure>

**Examples and details:**

- Tracer button on a "Deployed and running" box in Projects & Deploy: opens the chat with the Tracer below it
- Tracer icon under a deployed chat reply: opens that turn's task (logs arrive about 20 seconds after a turn)
- Graph: the broker's .agent flow with the path taken (numbered hops); nodes not reached are dimmed. Tree: the nodes in order; List: every log line
- Click a node or a line, then read it in Message, Metadata or Log (the spans are in the chat's Trace view); Story shows the conversation and node outputs the broker stored
- JSON: the whole task as one document (or NDJSON) for Splunk or Datadog, with credentials masked
- The access pill (App 10/10) checks each Anypoint API; when one fails it names the permission to add to the connected app, or traces with your own Anypoint Code Builder sign-in instead
- Drag the edges of the Tasks and detail columns to resize them; the arrow buttons hide or show them. Full height hides the network and the chat; the full-height icon in the chat header does the opposite (chat only)
- v1 brokers: Mule logs carry no trace id, so the spans are found by time (the [BROKER] span that covers the task) and marked "matched by time"; v2 brokers match by trace id
- Opening a task in the Tasks list also shows its span waterfall in the chat's Trace view (top left); the Full height icon at the right of the Tracer header gives the Tracer the whole panel
- Minimize all (the workflow icon top left of the Graph: one node branching to two) turns every node into its icon so long flows fit; the path taken stays highlighted. Press it again (Open all, two linked cards) to bring the cards back. The choice is kept per broker file
- Large environments: the broker is found among all API Manager instances (every page is read), so it works with hundreds of APIs. Runtime logs and the Object Store are found through the deployment named in the broker's upstream URL (http://<deployment>:8081/<broker>/)
