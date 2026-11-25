# Known limitations

- **Code view colours**: VS Code does not pass its editor syntax colours to webviews, so the Code view takes them from theme colours that are available (keys can look close to the text colour in some themes), and YAML numbers and booleans have the same colour as other values. For the exact colours of your theme, use **Open in text editor**.
- **CLI credentials**: Build, Publish, Deploy and Run locally pass the connected app from Setup & Connect to anypoint-cli-v4 (in the process environment). Without a connection the CLI falls back to its own `anypoint-cli-v4 conf client_id` / `client_secret` or `ANYPOINT_CLIENT_ID` / `ANYPOINT_CLIENT_SECRET`. Variables exported in a terminal don't reach VS Code started from the Dock, so *"No authentication mechanism was provided"* means: connect to Agent Fabric in Setup & Connect.
- **Anypoint Code Builder installed**: for v1 networks, ACB closes the editor that opens `agent-network.yaml` and opens its own canvas and the YAML text. Octoloom closes those two tabs again for a few seconds after it opens its canvas, so you may see a short flicker. To use the ACB canvas, use *Reopen Editor With… → API YAML Canvas Viewer*, or set `agentNetwork.keepOctoloomCanvas` to `false`.
- **Governance**:
  - Agent Fabric rulesets are downloaded from Exchange by the CLI the first time: connect to Agent Fabric once. After that they are cached (`~/.anypoint_deps`) and work without a connection.
  - Rulesets of your organization are listed through Exchange and validated from their downloaded YAML (read-only).
  - Your own P4A rulesets need a P4A token; otherwise add the ruleset YAML as a local file. P4A community rulesets are read from their public GitHub source.
  - **Fix** changes `agent-network.yaml` (and `exchange.json` for secrets) only when you press it. Findings that need a decision stay suggestions, and so do v1 brokers' authorization findings (v1 has no `interfaces.a2a.authorization`).
  - P4A MCP server rulesets (*MCP Server Safety* / *Usability*) are written for MCP server specs. In `agent-network.yaml` the governance CLI 1.1.3 can still report tool findings after the fix (annotations, `additionalProperties`, `outputSchema`; even existing descriptions). *Fix all* skips these rules and they don't trigger the "still reported" warning. A single Fix still writes the keys; the finding is then marked *fixed, still reported* and the fix is not offered again.
  - Tested with the governance CLI plugin 1.1.3.
- **Chat authentication**:
  - Client-credentials tokens are kept for 5 minutes (the token's `expires_in` is not read); a 401 fetches a new one once.
  - The user name shown after sign-in comes from the ID token, which is not verified. It is for display only.
  - User sign-in needs the redirect URI `http://127.0.0.1:<port>/callback` registered at your identity provider. The OAuth2 password grant is legacy: prefer User sign-in where the provider allows it.
  - The project status light uses cached tokens only. It never signs in or retries a password by itself, so a protected broker can show *Needs credentials* until you chat once.
- **Chat progress**: step-by-step lines appear only for brokers that put a status message in their working updates. The v2 templates do: before each step, their flow sends a *working* Reply that says what comes next (for example *Checking return eligibility with the Orders MCP...*). In your own flows, add a **Reply** with Task state *working* and a next step. v1 brokers (A2A 0.3) don't stream and can't be asked for their task, so they show the elapsed time only. The chat portal and A²D sessions don't stream yet.
- **Chat portal** (first release):
  - One shared passcode, no user accounts, and everyone uses the same broker credentials: the broker can't tell visitors apart. Share the passcode only with people who may see what the broker returns. Company sign-in (OIDC) is planned.
  - Brokers whose chat uses user sign-in or the OAuth2 password grant need a client-credentials or client ID method for the portal (set `BROKER_AUTH` in its `.env`).
  - Replies arrive when the broker finishes (no streaming). A portal on the local run's URL (`localhost`) works only while it runs on the same machine.
- **Agent Network Tracer**:
  - Logs reach Anypoint about 20 seconds after a turn; a young task with no lines yet is checked again by itself.
  - The span tree follows `parent_span_id`. A span whose parent is not in the result is nested by timing. Up to 2000 spans per trace are read.
  - With a shared connected app, everyone using it sees the task content and LLM reasoning the app can read.
  - The task filter, *Errors only* and the Local / UTC switch are not in this first release; times are local.
- **Run locally with an LLM** (anypoint-cli agent-network plugin 1.5.0 and 1.6.1, the tested version as of November 2026): brokers that call an LLM fail locally with *"An internal error occurred"*; the agent-graph log shows OpenAI answering `401 Incorrect API key provided: placehol…`. The CLI writes `apiKey: REDACTED_INERT_PLACEHOLDER` into the local egress gateway's LLM policy, and in our tests the local egress gateway did not apply that outbound policy at all, so the real key never reaches the LLM. This is in the CLI, and Octoloom does not change the CLI's generated files. **Use Deploy** (cloud) for brokers that call an LLM; the network, agents and MCP servers still start locally. Octoloom tests each new plugin version first; see [Tooling versions](#tooling-versions) for the tested one.
  - **Manual workarounds tried, none worked** (tested on 2026-11-11 with a v2 use-case template, Flex Gateway `latest` and plugin 1.5.0 on macOS; other templates, gateway versions, LLM providers and operating systems not tested): an env-var reference `apiKey: ${SECURE_OPENAI_APIKEY}` in `.deployment/local/egress/config/apis/<llm>-connection.yaml`, the literal key in that binding, and the real key as `OPENAI_API_KEY` on the agent-graph container. Every edit of `.deployment/local` is also overwritten by the next run or `--watch` rebuild. Never commit `.deployment/` if you put a key in it.

<a id="meet-the-octoloomies"></a>
