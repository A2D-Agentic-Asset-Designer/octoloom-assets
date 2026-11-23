# Requirements

- **VS Code 1.82** or newer.
- For build, publish and deploy (no need to install anything yourself; Octoloom does it on first use or with **Install / Repair**):
  - **Node.js ≥ 22.12**. Octoloom uses yours if it is recent enough, otherwise it installs a portable copy from nodejs.org.
  - **Java 17+**. Octoloom uses `JAVA_HOME` / `agentNetwork.javaHome`, otherwise it installs a portable Temurin 17 from Adoptium.
  - **anypoint-cli-v4** with the **Agent Fabric plugin**, installed into the extension's private storage.
- For **Run locally** (v2 only): **Docker Desktop**, running.

Portable installs stay inside the extension's storage folder and do not change your system `PATH`.
