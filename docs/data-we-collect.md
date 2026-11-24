<span class="ol-pill">About</span>

# Data we collect

Octoloom can send **anonymous usage counts** to help improve the extension: which actions run, whether they work, and on which versions. This page lists every event and every property. Nothing else is sent. The public [Usage](usage.md) page shows the totals.

## How it works

- **Off when VS Code telemetry is off.** Octoloom sends through VS Code's own telemetry logger, so VS Code's `telemetry.telemetryLevel` always wins.
- **Its own switch.** The setting `agentNetwork.telemetry.enabled` turns Octoloom's usage counts off, whatever VS Code's setting is.
- **Anonymous.** Events carry VS Code's anonymous machine id and no person profile. They are not linked to an Anypoint, A²D, P4A or IDMC account.
- **Small.** At most 100 events per VS Code session; the daily ping and each command at most once per day.
- **Only fixed values.** Every property is a fixed value, a yes/no or a range. Free text can't be sent: the extension drops it before sending.

## Events

| Event | Why | Properties |
|---|---|---|
| `activate` | Octoloom started (once per VS Code session). | common properties only |
| `heartbeat` | The machine used Octoloom today (at most once per UTC day), with which connections are set up. | `anypoint`: connected to Agent Fabric (boolean)<br>`a2d`: connected to A²D (boolean)<br>`p4a`: connected to P4A (boolean)<br>`idmc`: connected to Headless IDMC (boolean) |
| `build` | Build ran: success or failure, network style, how many policies (as a range) and whether it is governed. | `outcome`: result (enum)<br>`style`: v1 (Probabilistic) or v2 (Deterministic) (enum)<br>`policies`: number of policies as a range (enum)<br>`governed`: project has governance (boolean) |
| `validate` | Validate ran: success, failure or cancelled. | `outcome`: result (enum) |
| `publish` | Publish to Exchange ran: success or failure. | `outcome`: result (enum) |
| `deploy` | Deploy ran: success, failure or cancelled, and whether it also published. | `outcome`: result (enum)<br>`autopublish`: deploy also published (boolean) |
| `governance` | A governance check ran: conforms, violations or error, and how many rulesets (as a range). | `outcome`: result (enum)<br>`rulesets`: number of rulesets as a range (enum) |
| `create` | A project was created: network style and the template id from the public catalog (or blank). | `style`: v1 (Probabilistic) or v2 (Deterministic) (enum)<br>`template`: catalog template id, blank, or other (enum) |
| `feature` | An Octoloom command was used (at most once per command per UTC day). Only the command id. | `id`: contributed Octoloom command id (enum) |
| `error` | A guarded action failed: the action and the error class name (for example deploy:SourceError), never the message. | `action`: the action that failed (enum)<br>`code`: action:ErrorClass (enum) |

Every event also carries these common properties:

| Property | Value |
|---|---|
| `extVersion` | Octoloom version (semver only) |
| `vscodeVersion` | VS Code version (semver only) |
| `os` | win, mac, linux or other |
| `uiKind` | desktop or web |
| `remoteName` | none, ssh, wsl, container, codespaces or other (never the host name) |
| `country` | derived by PostHog from the IP address, which is then discarded |

## Never collected

- names of projects, agents, brokers or files
- file paths, file contents or project files
- URLs, host names, gateway or environment names
- organization ids, user names or e-mail addresses
- API keys, tokens or credentials
- error messages or stack traces
- chat messages or prompts
- the IP address (discarded after the country lookup) and anything finer than the country
- a user profile: events are anonymous (no person profiles)

## Where the data goes

- **Processor:** PostHog Cloud **EU** (servers in the EU). The project discards the IP address after the country lookup and keeps no person profiles.
- **Retention:** raw events for **1 year**. After that only monthly aggregates are kept (counts, no machine ids).
- **Public numbers:** the [Usage](usage.md) page shows only totals, and countries or other breakdowns only when they cover at least **5 machines**; smaller groups are shown as *Other*.

## Turn it off

- In VS Code: **Settings → Telemetry → Telemetry Level → off** (`"telemetry.telemetryLevel": "off"`), which turns off telemetry of all extensions; or
- only for Octoloom: `"agentNetwork.telemetry.enabled": false` in your settings (search **@tag:telemetry** in the Settings editor).

## Deletion

To have the events of your machine deleted, open an issue on [octoloom-assets](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/issues/new?title=Telemetry%20deletion%20request) titled *Telemetry deletion request*. **Don't post your machine id in public**: the maintainers reply with a private way to send it. Details of the process follow the project decision (octoloom #324, pending).
