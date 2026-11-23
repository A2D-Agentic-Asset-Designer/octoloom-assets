# Requirements

- **VS Code 1.82** or newer.
- For build, publish and deploy (no need to install anything yourself; Octoloom does it on first use or with **Install / Repair**):
  - **Node.js ≥ 22.12**. Octoloom uses yours if it is recent enough, otherwise it installs a portable copy from nodejs.org.
  - **Java 17+**. Octoloom uses `JAVA_HOME` / `agentNetwork.javaHome`, otherwise it installs a portable Temurin 17 from Adoptium.
  - **anypoint-cli-v4** with the **Agent Fabric plugin**, installed into the extension's private storage.
- For **Run locally** (v2 only): **Docker Desktop**, running.

Portable installs stay inside the extension's storage folder and do not change your system `PATH`.


<figure markdown>
![Setup & Connect → Tooling checks every requirement and installs what is missing](../assets/ui/setup-connect-light.webp#only-light){ loading=lazy }
![Setup & Connect → Tooling checks every requirement and installs what is missing](../assets/ui/setup-connect-dark.webp#only-dark){ loading=lazy }
<figcaption>Setup & Connect → Tooling checks every requirement and installs what is missing</figcaption>
</figure>
