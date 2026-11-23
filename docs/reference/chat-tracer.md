# Chat, Share and Tracer

Talk to a deployed broker, share it and see what it did.

## Broker chat

Talk to a deployed broker (or one running locally) the way a client would: send a message, read the reply, and see which agents and tools it used. While it waits, the chat shows that the broker is working and never looks stuck. Replies of a deployed broker carry a trace icon that opens its distributed trace.

**When to use it:** After a deploy or a local run, to try the network end to end before anyone else uses it.

**Examples:**

- Pick the broker at the top of the chat, type a question and press Enter
- Skills of the broker appear as chips above the message box; click one to start from it
- Open the trace icon under a reply to see every call it made
- Fold the chat into a rail with the chevron in its header; click the rail to bring it back
- While the broker works, its bubble says so and counts the seconds: "Working on it… 12 s", and after 10 s "Still working, not stuck". A v2 (A2A 1.0) broker also streams its updates, each listed with its time and its own words, e.g. "17:59:24 Working Looking up the practitioner record..."
- The Live button left of Send turns these broker updates on or off (red when on). v1 (A2A 0.3) brokers answer in one go, so it is greyed out there; the bubble still shows that the broker is working

## Agent Network View

The Network tab of the chat, read-only. With no reply picked it is the whole network drawn like the network canvas: brokers, agents, MCP servers, LLMs, their connections and policies, with no editing. Once you pick a reply (trace icon under a deployed reply, or a task in the Agent Network Tracer) it shows that reply as a sequence diagram: You, the broker, then each agent, MCP server and LLM it called, with one request and one response arrow per call, numbered (1), (2), … in time order. It uses the same trace lookup as the Trace waterfall, so nothing new is called in your organization.

**When to use it:** To see how the network is built while you chat, and to follow one reply hop by hop: who called whom, what was sent, what came back and how long it took.

**Examples:**

- The canvas always fits its section, also when you drag the splitter or resize the panel; zoom with the bar at the bottom (Fit brings the fitted view back). The sequence has the same zoom bar: Fit follows the section, your own zoom is kept per project
- Full screen (the maximize icon in the left header) gives the whole panel to the network, the sequence or the trace; the chat and the Tracer come back with the same icon
- Click a broker card to chat with it. Drag cards, minimize one with its icon tile or collapse it with its chevron; Minimize all and Auto layout are top left. The layout is kept per project
- Pick the trace icon under a deployed reply, then Network: the reply as a sequence of calls
- Click an arrow: the call with its step numbers, e.g. (6) → (7), its span, status and HTTP code, duration, start offset and span id, then the log lines with the request and the response (message text, tool input and output, the stored tool calls of a v2 broker)
- Gateway router hops and Mule flow spans are not drawn: their calls belong to the agent, MCP server or LLM above them. A failed call is drawn in the error colour
- The network icon in the sequence header goes back to the whole network; the pulse icon on the canvas shows the picked reply again
- Switch to Trace for the same reply as a span waterfall. The trace is loaded once and kept while the chat is open, so switching between Network and Trace is instant; the refresh icon in the section header loads it again

## Trace of a chat reply

The distributed trace of one deployed chat reply, shown on the left of the chat instead of the network: a waterfall with one row per span (gateway request, broker, LLM calls, A2A calls to agents, MCP tool calls), nested by parent span id, each bar on a shared time axis and coloured like its box on the canvas. Read-only: it uses the same task lookup as the Agent Network Tracer (Log Search for the trace id, then the Observability span search). v1 broker logs carry no trace id: their trace is the broker span that covers the reply, marked "matched by time".

**When to use it:** After a reply, to see which calls the broker made for that message, in what order, how long each took and which one failed. It needs a deployed, running broker: local runs have no spans.

**Examples:**

- Trace icon (pulse line, no text) under a deployed reply: shows that reply's trace on the left. The Tracer icon next to it opens the task in the Agent Network Tracer
- Open a task in the Agent Network Tracer's task list: its spans show here too, so the list drives this view
- Network | Trace above the left column switches between the network and the trace; the reply shown is kept per conversation
- Click a span: kind, entity, status and HTTP code, duration, start offset, span and parent ids
- The legend above the waterfall says what each colour is (Broker, Agent, LLM, MCP, Router, Other, Error), only for the kinds in this trace. Hover a name for what it covers; click it to choose your own colour. Reset colours brings back the defaults. Your colours are saved on this machine only
- Spans arrive about 20 seconds after a reply: a young reply with no spans is checked again after 10, 20 and 40 seconds; refresh checks again at any time
- Full height icon in the trace header: the waterfall takes the whole panel; press it again for the chat
- Collapse the left side (chevron in the network bar) or the chat (chevron at the end of the chat header) to a thin rail; click the rail to expand it. The Tracer collapses to its header

## Chat authentication

How the broker chat authenticates to a broker behind a gateway policy (JWT Validation, Client ID Enforcement, Basic) or with anonymous access off. Set per broker and per target (deployed or local) with the shield button in the chat header. Secrets and tokens are kept in VS Code Secret Storage on this machine, never in the project, exchange.json or the chat history, and they are never sent to the webview. The same credentials let the project status read the agent card of a protected broker: saving or clearing them checks the deployment again, so the light goes from blue (needs credentials) to green, and the broker row shows a "saved" shield.

**When to use it:** The chat answers HTTP 401 or 403, or the broker policies ask for credentials. The method the policies suggest is preselected.

**Examples:**

- Bearer token: paste an access token (JWT) you already have
- User sign-in: authorization code + PKCE in your browser. Register http://127.0.0.1:33418/callback (public client / native) at Entra ID, Okta, Auth0 or Keycloak. Tokens refresh by themselves; Sign out forgets them
- Client credentials: token URL, client ID and secret of an app registration (machine to machine), e.g. Entra https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token with scope api://<app-id>/.default
- OAuth2 password: user name and password for a client that only allows the password grant (Keycloak "Direct Access Grants"), e.g. https://<keycloak-host>/realms/<realm>/protocol/openid-connect/token with scope openid. Both the password and the client secret stay in Secret Storage. Prefer User sign-in when your identity provider allows it
- Client ID: client_id and client_secret headers for the Client ID Enforcement policy. The key icon in the Authentication header opens the broker in Exchange, where Request access gives you both
- API key header or Basic for brokers behind a custom key or basic authentication
- Clear removes the settings and the stored secret for the broker
- Limits: client-credentials tokens are kept 5 minutes (a 401 gets a new one); the ID token is shown, not verified; the project status uses cached tokens only and never signs in by itself; changing the method forgets the old secret

## Share: A²D sessions and local portal

The Share icon in the broker chat header, after New conversation, opens the Share dialog for the chat's broker on its A²D sessions tab; the Local portal tab is one click away. Sharing is not in Projects & Deploy. Broker credentials: none, bearer token and Basic always work; with an A²D that has Octoloom chat sessions also Client ID (as its own headers), a custom API key header and OAuth2 client credentials, while an older A²D sends Client ID as Basic. A²D doesn't encrypt them at rest yet, so use a test client app scoped to the broker. Creating, ending and removing an A²D session are confirmed in the dialog itself: send opens a review of the session, broker, invited people, expiry and credentials, where send creates it and close goes back; end and remove show a confirmation strip on the session row. Local portal generates a standalone web chat project for one broker: a small Node server (no dependencies) and a chat page, plus a Dockerfile and a README with deploy steps. The page looks like Octoloom's chat: the mascot, skill cards, bubbles and the reply state. Visitors sign in with a shared passcode; Octoloom shows it once and writes only its scrypt hash into the portal's .env. The server calls the broker over A2A with the credentials method saved in the chat (shield button), so the secret stays on the server and never reaches the browser. Follow-up questions keep the broker conversation. The Broker URL list offers the Anypoint deployment, the local run (only reachable while the portal runs on this machine) or any other URL. A project can have several portals, each with its own folder, passcode and local port. The portal checks itself: node server.mjs --check (and the same checks at startup) tests the settings, the broker, its agent card, the token and the credentials and prints a fix for each problem; the page has a Status panel with the checks, versions and recent events (never messages), and a failed reply says what went wrong with a reference that is also in the server log. Each portal records the Octoloom version that generated it; when Octoloom is newer, its box offers Update (same broker, title, passcode and .env). A²D sessions share a deployed broker as an A²D exploratory session of the Octoloom chat type: the people you invite by email verify themselves with a code on an Octoloom-styled page, then chat in the Octoloom chat window hosted by A²D, keep their conversation going across follow-up questions, and mark replies and the session passed, failed or in progress with a comment. The session always expires (1 to 90 days, no 'never'). Its row opens or copies the link, invites more people, extends, ends it or removes it from A²D, all with small icons. Opened, it shows the results stored in A²D, refreshed every minute: who was invited, verified and submitted, every passed, failed or in-progress mark with its comment (new ones are marked new), each visitor's Submit, and every conversation; Continue in the chat loads a visitor's conversation into this chat window so you can carry it on with the same context. An older A²D without the Octoloom chat type falls back to its exploratory tester (the row says A²D tester); the marks and comments testers set there show the same way once A²D returns them. Use a dedicated test client app for the broker credentials; supported: no credentials, a bearer token, Basic, or Client ID sent as Basic.

**When to use it:** When colleagues should chat with a broker without VS Code or Octoloom, and you can't install a Slack or Teams app: run it here to try it, then deploy the folder to any Node host or container service. Everyone who chats uses the same broker credentials, so share the passcode only with people who may see what the broker returns.

**Examples:**

- Chat with incident_broker, click Share in the chat header, then Local portal: the form has that broker and its Anypoint URL
- incident_broker → "Incident Assistant": Generate portal, copy the passcode, Run locally, open http://localhost:3000
- Deploy the folder to Render, Fly.io, Cloud Run or Azure App Service: set BROKER_URL, PORTAL_PASSCODE_HASH and the BROKER_* secret on the host
- A broker behind Client ID Enforcement: turn on "Write the saved secret into .env" for a local run, set BROKER_CLIENT_SECRET on the host
- Generate again with New passcode to lock out everyone who had the old one
- Two portals for one broker: incident-response-chatportal-1 on Anypoint for colleagues (hosted), -2 on the local run for your own tests on localhost:3001
- Delete (trash) moves a portal folder to the Trash after asking; Forget (×) only takes it off the list
- A colleague says it is not working: ask for Copy report from the Status panel, or run node server.mjs --check in the portal folder
- Portal box says Generated with Octoloom 0.9.24: Update, then redeploy the folder
- Share icon (opens on A²D sessions): 14 days, invite two colleagues by email, Create session, then copy the link
- Open the session row: 2 of 3 verified, 6 passed, 2 failed and 1 in progress, with the comments and each conversation with its turns
- A tester's conversation stopped at input-required: Continue in the chat and answer the broker yourself
- A session for business testers is ending: extend it by 7 days from its row, or end it now and remove it from A²D later

## Why a call failed

When Octoloom cannot load from Agent Fabric, A²D, P4A, Headless IDMC or an MCP server, the red line says what failed in one sentence and the info (i) button after it shows why: the HTTP status, the request (method and URL), selected response headers such as x-request-id, the response body, the network cause (for example ENOTFOUND, ECONNREFUSED, a certificate error or a timeout) and what to check. Copy details puts the whole text on the clipboard for the administrator of that system. Passwords, tokens, session IDs and secrets are masked in the URL and the body.

**When to use it:** When the Assets palette shows an error or a partial failure (for example IDMC composite MCP servers), before asking anyone for help.

**Examples:**

- ENOTFOUND mcp.dm-xx…: the host does not resolve: check the pod or region and your VPN
- HTTP 401 with error.message "Invalid session": connect again in Setup & Connect
- HTTP 403: the connected app or user lacks a role or scope
- SELF_SIGNED_CERT_IN_CHAIN: a corporate proxy intercepts TLS (NODE_EXTRA_CA_CERTS)

## Agent Network Tracer

Shows what a deployed broker did for each task: the nodes it ran, the tools and LLMs it called, what failed and why. Read-only: it only reads logs and task state from Anypoint (Log Search, runtime logs, Object Store and Observability spans) and never changes anything in your organization. The organization, environment and broker come from the project's deployment, and the Agent Fabric connected app makes the calls. Three columns: Tasks, the task (Graph, Tree or List) and the detail of what you pick.

**When to use it:** After a chat turn or a failed task on a deployed broker, to see the path it took and where it went wrong. It needs a deployed, running broker: local runs have no Anypoint logs.

**Examples:**

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
