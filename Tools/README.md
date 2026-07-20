# Tools — Skills and Workflows

Reusable building blocks. Skills are single tasks. Workflows chain skills together with a slash command.

---

## Structure

```
Tools/
├── 01-skills/      ← Individual reusable tasks
└── 02-workflows/   ← Multi-step sequences with slash commands
```

---

## Skills

| Skill | File | What It Does |
|-------|------|--------------|
| Setup System | `setup-system.md` | First-session OS setup — builds everything from scratch |
| Brief a Post | `brief-post.md` | Create a brief for a new LinkedIn post |
| Research a Post | `research-post.md` | Gather facts, examples, angles for a post |
| Write a Post | `write-post.md` | Write the post from brief + research |
| Quality Check | `quality-check.md` | Final review before any content is approved |
| Content Repurpose | `content-repurpose.md` | Turn one piece of content into multiple formats |
| Research Brief | `research-brief.md` | Quick structured research on any topic |
| Create New Skill | `create-new-skill.md` | Build a new skill and add it to the OS |
| Create New Agent | `create-new-agent.md` | Build a new agent and add them to the team |
| Create New Workflow | `create-new-workflow.md` | Build a new workflow and wire it to a slash command |

---

## Workflows

| Workflow | Command | What It Does |
|----------|---------|--------------|
| LinkedIn Content | `/content [topic]` | Brief → Research → Write → Quality Check — full post from topic to approved draft |

---

## Slash Commands

Slash commands live in `.claude/commands/`. Type the command in Claude Code to trigger the workflow.

| Command | Triggers |
|---------|----------|
| `/setup` | First-time OS setup |
| `/content [topic]` | LinkedIn content workflow |

---

## When to Build a New Skill

Build a skill when you have done the same thing three or more times.

Tell your COO: "I keep doing [X]. Can we make it a skill?" — or run `/create-new-skill`.

## When to Build a New Workflow

When a task has multiple steps that always run in the same order. Build the skills first, then chain them.

Tell your COO: "Create a workflow for [process]." — or run `/create-new-workflow`.
