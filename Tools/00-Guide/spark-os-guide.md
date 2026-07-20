# Spark OS — Complete Guide

*Everything you need to set up and run your AI operating system. Read this once. Your COO handles the rest.*

Built by Spark AI — Roee Barak | roeebarak@gmail.com

---

## What Is Spark OS?

Spark OS is an AI-native business operating system built on Claude Code.

It is not a chatbot. It is not a tool you open and ask questions to. It is a system — a structured folder on your computer that your AI reads at the start of every session. The system knows your business, remembers what it learns, and gets smarter every time you use it.

At the center of the system is your COO — an AI agent you name and configure. They run the system, build your team, execute tasks, and close the loop at the end of every session. You are the CEO. You direct. They execute.

---

## What You Need

Install all four before your first session:

**1. Claude** — the AI brain
- Go to `claude.ai` and create an account
- Upgrade to Pro ($20/mo) — the free plan is not enough
- Upgrade to Max ($100/mo) when you are using it every day

**2. Claude Code** — your command center
- Go to `claude.ai/code` and download the Mac desktop app
- Sign in with your Claude account
- This is where you talk to your AI team

**3. GitHub** — your cloud vault
- Go to `github.com` and create a free account
- Create a new private repository — name it something like `yourname-os`
- Copy the repository URL — you will need it in your first session
- This is where your system is backed up and versioned

**4. Obsidian** — your knowledge browser (optional but recommended)
- Go to `obsidian.md` and download the free app
- After setup, open your OS folder as a vault
- Lets you browse your system visually, like a wiki

---

## Setup — Step by Step

### Before your first session

**1. Set up your folder**

- Create a new folder anywhere on your Mac. Name it `YourName-OS`.
- Open the zip file you received.
- Open the extracted folder called "Spark AI System v0."
- Select everything inside (Cmd+A), copy it, and paste into your YourName-OS folder.

Your folder should contain:
```
YourName-OS/
├── CLAUDE.md
├── Core/
├── Memory/
├── Agents/
├── Brain/
├── GTM/
└── Tools/
```

**2. Choose a name for your COO**

Before opening Claude Code, decide on a name. This is the name you will type every single day. Pick something that feels like a real person you trust.

Write it down. You will use it in the next step.

**3. Create your GitHub repo**

- Go to `github.com`
- Click New Repository
- Name it `yourname-os`, set to Private
- Copy the repository URL — it looks like: `git@github.com:yourusername/yourname-os.git`

---

### Your first session

1. Open Claude Code
2. Click **Open folder** and select your YourName-OS folder
3. Type: `/setup`

The first thing the system asks: "What name do you want to give me?" Give your COO a name. From that moment, they guide you through everything.

**Phase 1 — Name your COO**

The system asks for a name. Pick something that feels like a real person you trust. This is what you will type every day to start your session. The COO renames itself and you are off.

**Phase 2 — They interview you, they write everything**

Your COO asks you questions about your business. Answer in your own words — no jargon needed. They fill in all three Core files:
- `Core/project-brief.md` — what your business does
- `Core/voice-dna.md` — how your brand sounds
- `Core/icp-profile.md` — who your ideal customer is

You review everything. You refine until it feels right.

**Phase 3 — They write your CLAUDE.md**

The system's constitution. This is what your AI reads at the start of every future session. Your COO builds it from your Core files.

**Phase 4 — They fill your Memory**

Your COO writes `Memory/essentials.md` — the fast-load summary of your business. The other Memory files (learning log, decisions, feedback) start empty. They earn entries as real work happens.

**Phase 5 — They connect to GitHub**

Give your COO the repo URL you created. They run the git setup — init, connect, first commit, push. Your system is backed up.

**Phase 6 — System is live**

Setup is done. Your AI knows your business. What do you need?

From this point on, every session starts with: `hi [your COO name]`

---

## How Every Session Works

Every time you open Claude Code from your OS folder, the system reads:

1. `CLAUDE.md` — the constitution. What the business is, who the team is, what the rules are.
2. `Core/` — all three files. Identity, voice, customer.
3. `Memory/` — all four files. Essentials, learning log, decisions, feedback.
4. `Agents/README.md` — who is on the team.

After reading, your AI is fully loaded. It knows your business. It knows what was decided. It knows what was learned last time. It picks up where you left off.

**You do not re-explain yourself. The system already knows.**

Then you work. When the session is over, you close the loop.

---

## The Loop — How the System Gets Smarter

The loop is the most important habit in the system. It is what separates a tool you use once from a system that compounds over time.

At the end of every meaningful session, tell your COO: **"Close the loop."**

They will go through this checklist:

| Question | If yes, update |
|----------|---------------|
| Did we learn something that should inform future sessions? | `Memory/learning-log.md` |
| Was a strategic choice made that is now locked? | `Memory/decisions.md` |
| Did any external signal come in — customer feedback, content result, market observation? | `Memory/feedback.md` |
| Has the current state of the business meaningfully changed? | `Memory/essentials.md` |
| Did a strong communication pattern emerge that should become a standing rule? | `Core/voice-dna.md` |

Then they commit all changes and push to GitHub.

**If nothing meaningful happened in a session — the COO says "nothing to log." That is fine. No invented entries.**

Closing the loop takes 5 minutes. Skip it and the system stays flat. Do it and the system compounds.

---

## Your Skills

Skills are reusable tasks your COO can run on your behalf. They live in `Tools/01-skills/`.

| Skill | What It Does |
|-------|--------------|
| `setup-system` | First-session OS build — runs automatically |
| `brief-post` | Create a brief for a LinkedIn post |
| `research-post` | Research a post topic in depth |
| `write-post` | Write the post from brief and research |
| `quality-check` | Final review before any content is approved |
| `content-repurpose` | Turn one piece of content into multiple formats |
| `research-brief` | Quick structured research on any topic |
| `create-new-skill` | Build a new skill and add it to the OS |
| `create-new-agent` | Build a new agent and add them to the team |
| `create-new-workflow` | Build a new workflow and wire it to a slash command |

**How to use a skill:** Tell your COO — "Run the [skill name] skill on [input]." Or just describe what you need and they will pick the right skill.

---

## Your Workflows

Workflows chain multiple skills into a single command. They live in `Tools/02-workflows/`.

### `/content [topic]` — LinkedIn Post Workflow

Type `/content` followed by a topic in Claude Code. Example:

```
/content why most founders build before they sell
```

The workflow runs four steps in sequence:
1. **Brief** — turns your topic into a specific, opinionated angle. Stops for your approval.
2. **Research** — gathers facts, examples, and a personal angle from you.
3. **Write** — produces one strong draft using your voice DNA.
4. **Quality check** — reviews mechanics, voice, substance, and audience fit before presenting as final.

You get a finished, approved post. You directed the angle. The system did the work.

---

## How to Grow Your System

Your system starts small. That is intentional. Add to it as real needs emerge.

**Adding a new agent:**
Tell your COO: "I need an agent who [does X]. Their name is [Name] and they communicate [how]."
Your COO builds the file, adds them to the team roster, and updates CLAUDE.md.

**Adding a new skill:**
Tell your COO: "I keep doing [X]. Can we make it a skill?"
If you have done it three or more times, it is ready to become a skill.

**Adding a new workflow:**
Tell your COO: "Create a workflow for [multi-step process]. The command should be /[name]."
Your COO builds the workflow file and the slash command.

**Adding a new GTM channel:**
Ask your COO to create a subfolder in `GTM/` — for a newsletter, LinkedIn system, outbound, or anything else.

---

## The Memory Files — What Goes Where

This is the most common question. Here is the routing:

| What happened | Where it goes |
|---------------|---------------|
| You noticed a pattern in how your business works | `learning-log.md` |
| Something failed and you learned why | `learning-log.md` |
| You made a strategic choice — positioning, direction, product | `decisions.md` |
| A customer said something worth keeping | `feedback.md` |
| A post or email performed unusually well or poorly | `feedback.md` |
| A market trend or competitor move worth tracking | `feedback.md` |
| The state of the business has meaningfully changed | `essentials.md` |
| A communication pattern should become a permanent rule | `voice-dna.md` |
| A task or to-do | Your task tool — NOT in this repo |

---

## Troubleshooting

**My COO does not seem to know my business.**
Check that CLAUDE.md is complete — it should have no placeholder text. If it still has `[YOUR BUSINESS NAME]` style text, the setup was not completed. Type "hi [name]" and say: "Run setup — our Core files are not filled in yet."

**I typed a slash command and nothing happened.**
Make sure you are in the right folder. The `.claude/commands/` folder must be inside your OS folder. If it is there, try: "Run the /content workflow on [topic]" as plain text.

**The COO is writing to the wrong file.**
Tell them explicitly: "That is a decision, not a learning. It goes in decisions.md." The routing rules in CLAUDE.md will guide them, but you can always override.

**I lost my folder / changed computers.**
If you set up GitHub in your first session, all your files are backed up. Clone your repo:
`git clone git@github.com:yourusername/yourname-os.git`
Open the cloned folder in Claude Code. Your system is restored.

**I want to add a new agent but do not know where to start.**
Tell your COO: "I want to add a [role name]. Help me think through what they need." They will ask the right questions and build it.

---

## What This System Is Not

- It is not magic. The quality of your Core files determines the quality of everything the system produces. Take time in setup.
- It is not a task manager. Use a dedicated tool (Todoist, Linear, Notion) for tasks and to-dos.
- It is not a replacement for your judgment. You are the CEO. You make the calls. The system executes.
- It is not complete on day one. It grows with you. The more you use it, the smarter it gets.

---

## Questions

Roee Barak — roeebarak@gmail.com

If you get stuck, describe exactly what you typed and what happened. I will help you get unstuck.
