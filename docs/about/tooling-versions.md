# Tooling versions

Octoloom tests each new version of the Agent Fabric CLI plugin before users get it (#250). New installs and repairs always use the tested (pinned) versions.

| Tool | Minimum | Tested | Octoloom installs |
|---|---|---|---|
| Agent Fabric CLI plugin (`mulesoft-anypoint-cli-agent-fabric-plugin`) | 1.5.0 | 1.6.1 | 1.6.1 |
| anypoint-cli-v4 (`anypoint-cli-v4-public`) | 1.6.0 | 1.6.28 | 1.6.28 |
| Node.js | 22.12 (22.23.4 for plugin 1.6) | 22.x and 24.x | 22.23.4 |
| Java | 17 | 17 | Temurin 17 |

Below the minimum, Tooling warns and a failed CLI command names the outdated tool as the likely cause; newer than tested is shown as *untested* and still runs. Installing the plugin from Tooling also changes your own `anypoint-cli-v4` setup, because plugins belong to the CLI on your `PATH`.
