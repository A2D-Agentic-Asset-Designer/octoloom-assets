# Octoloom skills for building agent networks

Six skills for AI assistants (Claude Code, Cursor and similar). They teach an assistant to design, write, mock, govern, deploy and test MuleSoft Agent Fabric agent networks, the way the Octoloom templates are built.

They are plain Markdown with a short header (`name`, `description`). Octoloom does not need them. They work with any editor.

## The skills

| Skill | Use it to |
|---|---|
| [agent-network-design](agent-network-design.md) | Choose v1 or v2, size and name the network, pick a template to start from |
| [agent-network-v1](agent-network-v1.md) | Write `agent-network.yaml` for an LLM-routed (v1) network and pass the CLI build |
| [agent-network-v2-flows](agent-network-v2-flows.md) | Write `brokers/*.agent` flows: triggers, routers, generators, subagents, orchestrators, executors, echo replies and progress updates |
| [agent-network-a2d-mocks](agent-network-a2d-mocks.md) | Mock agents, MCP servers and the LLM on A²D, then swap to real services |
| [agent-network-governance](agent-network-governance.md) | Add gateway policies, secured connections and check governance rulesets |
| [agent-network-deploy-test](agent-network-deploy-test.md) | Validate, build, publish, deploy, chat over A2A and check replies safely |

Typical order: design, then v1 or v2-flows, then a2d-mocks, then governance if needed, then deploy-test.

## Install

Claude Code:

```sh
# in one project
mkdir -p <project>/.claude/skills
cp -r skills/agent-network-* <project>/.claude/skills/

# for all projects
mkdir -p ~/.claude/skills
cp -r skills/agent-network-* ~/.claude/skills/
```

Each folder keeps its `SKILL.md`. Claude Code loads a skill when its description fits your request.

Other assistants (Cursor, Copilot, Codex and others): point the assistant at the files. For example add a rule or instruction such as "For agent networks, read `skills/agent-network-design/SKILL.md` first and follow the skill that matches the task", or paste the file into the chat.

## Requirements

- `anypoint-cli-v4` with the agent-network plugin, Node.js and Java.
- For publish and deploy: an Anypoint organization with Agent Fabric and a Flex gateway.
- For mocks: an A²D account and API key. Keep keys in environment variables, never in project files.

## Related

- [templates](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/tree/main/templates): the ready-to-run examples (41 in this repo; Octoloom also bundles two Informatica IDMC templates, 43 in total). Index in [templates/index.json](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/blob/main/templates/index.json).
- [tutorials](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/tree/main/tutorials): one tutorial per template, and [getting-started](https://github.com/A2D-Agentic-Asset-Designer/octoloom-assets/blob/main/getting-started.md).
- The [documentation site](https://a2d-agentic-asset-designer.github.io/octoloom-assets/skills/) renders these skills. Octoloom for Agent Fabric (VS Code extension) shows these projects as canvases and builds and deploys them.
