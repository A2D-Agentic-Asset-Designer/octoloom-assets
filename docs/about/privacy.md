# Privacy and security

- The connected-app secret, the A²D API key and the P4A token are stored in VS Code **SecretStorage** (your OS keychain). They are never written to settings or project files.
- Octoloom only talks to the hosts you configure (the Anypoint control plane, A²D and P4A), plus nodejs.org / Adoptium / npm when it installs prerequisites, and once per session the public Visual Studio Marketplace to read the latest Octoloom version (no project or usage data is sent).
- There is no telemetry. The Welcome page statistics are kept in VS Code's global state on your machine.
- Secret variables in `exchange.json` are masked in the UI and are never used to resolve URLs for display. The connectivity test uses them inside the extension host only, to call the endpoint you test (and its OAuth token URL). They are never sent to the webview.
