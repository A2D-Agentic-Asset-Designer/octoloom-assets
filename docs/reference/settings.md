# Settings

| Setting | Default | Description |
|---|---|---|
| `agentNetwork.theme` | `auto` | Color mode of all Octoloom views (auto, light, dark) |
| `agentNetwork.showWelcome` | `true` | Open the Octoloom Welcome page when VS Code starts |
| `agentNetwork.autoOpenCanvas` | `true` | Open the canvas when a workspace with one project opens |
| `agentNetwork.keepOctoloomCanvas` | `true` | Keep the Octoloom canvas when another extension (Anypoint Code Builder for v1 networks) replaces it with its own canvas and the YAML text right after you open `agent-network.yaml` |
| `agentNetwork.useVariablesForUrls` | `true` | Put asset URLs into `exchange.json` variables instead of hard-coding them |
| `agentNetwork.anypointHost` | `anypoint.mulesoft.com` | Agent Fabric control plane host |
| `agentNetwork.a2dBaseUrl` | `https://www.a2d-ai.com` | A²D base URL |
| `agentNetwork.p4aBaseUrl` | `https://www.p4a.ai` | P4A base URL |
| `agentNetwork.cliPath` | *(auto)* | Path to `anypoint-cli-v4`; empty means detect or install |
| `agentNetwork.javaHome` | *(auto)* | Java 17+ home for builds; empty means detect or install |
| `agentNetwork.tracer.debugLog` | `false` | Agent Network Tracer: log every Anypoint call (method, path, status, timing, answer shape; never tokens or contents) to the *Agent Network Tracer* output |
| `agentNetwork.tracer.debugLogFile` | *(empty)* | Also append the Tracer debug log to this file |
