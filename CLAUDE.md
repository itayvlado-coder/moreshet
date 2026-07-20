# Moreshet — AI Operating System

## GIT RULE — NON-NEGOTIABLE

**This repo:** `https://github.com/itayvlado-coder/moreshet.git`

Only Steven works on this repo. No cross-repo operations. Ever.

---

## Session Start Protocol

Read these files at the start of every conversation, in this order:

### 1. Core — who we are
- `Core/project-brief.md` — what the business does, who it serves, how it makes money
- `Core/voice-dna.md` — how we communicate, what we never say
- `Core/icp-profile.md` — who the ideal customer is

### 2. Memory — what we know
- `Memory/essentials.md` — compressed current state, fast-load (read this first)
- `Memory/learning-log.md` — what the system has learned
- `Memory/decisions.md` — strategic choices already made, never revisited
- `Memory/feedback.md` — customer feedback, content signals, market observations

### 3. Team
- `Agents/README.md` — who is on the team and how to invoke them

### 4. Brain — load on demand
Do NOT load Brain files at startup. Load only when relevant to the current task.
- `Brain/04-INBOX/inbox.md` — check if the CEO asks to process the inbox
- `Brain/Templates/` — reference when capturing knowledge

**LAZY LOADING RULE:** Same applies to agent files. Do not read individual agent files at startup. Load the agent file only when explicitly invoked.

---

## The Loop — How This System Gets Smarter

The loop runs at the end of every session that produced real work. When the CEO says "close the loop," "end session," or "wrap up" — execute the full loop protocol below.

### What Goes Where

**`Memory/learning-log.md`** — operational learnings and system discoveries:
- A pattern you noticed in how the business works
- Something that failed and why
- A new approach that worked better than expected
- A rule or principle worth keeping
- A workflow or skill insight

**`Memory/decisions.md`** — strategic choices that are now locked:
- A positioning or direction decision
- A product or GTM choice
- Anything that was deliberated and settled — does not get revisited

**`Memory/feedback.md`** — signals from the outside world:
- What a customer or prospect said
- How a piece of content performed
- A market signal or competitive observation
- Any raw external data worth tracking

**`Memory/essentials.md`** — update only when the current state has meaningfully changed:
- A new active project started
- A key decision that changes what we are doing
- A milestone reached or missed
- A rule that should now be in the fast-load summary

**`Core/voice-dna.md`** — promote only when a strong pattern becomes a standing rule:
- A phrase or format that consistently lands well
- A word or approach to permanently avoid
- Only when it is a pattern, not a one-off

### What Does Not Go in the Loop
- Tasks and to-dos — those go in your task tool, not here
- Raw content drafts — those live in GTM or Brain
- One-off observations that will not matter next week

### The Loop Checklist

When the CEO says to close the loop, run through this in order:

1. **Learning log** — did this session produce an insight worth keeping? If yes, add it.
2. **Decisions** — was any strategic choice made? If yes, log it with reasoning.
3. **Feedback** — did any external signal come in (customer comment, content result, market observation)? If yes, log it.
4. **Essentials** — has the current state of the business changed enough to update the fast-load summary? If yes, update it.
5. **Voice DNA** — did a strong pattern emerge that should become a standing rule? If yes, promote it.
6. **Git** — commit all changes and push to `https://github.com/itayvlado-coder/moreshet.git`

**If nothing meaningful happened in a session — no learning, no decision, no feedback — the loop is "nothing to log." That is fine. Do not invent entries.**

---

## Rules

**TASK MANAGEMENT:** All tasks and to-dos go into your task tool. No todo.md files in this repo.

**GIT LOOP:** Only commit to `https://github.com/itayvlado-coder/moreshet.git`. Never commit to any other repo from this folder.

**NO HALLUCINATED FACTS:** If you are uncertain about something, say so. Do not fill Memory files with guesses.

---

## Your Team

| Agent | Role | Invoke |
|-------|------|--------|
| Steven | COO — builds, organizes, runs the system | `hi Steven` |

*Add agents to this table as you build them.*

---

## Slash Commands

| Command | What It Does |
|---------|--------------|
| `/setup` | First-time OS setup — builds everything from scratch |
| `/content [topic]` | Full LinkedIn post: brief → research → write → quality check |

---

## Need Help?

Type `hi Steven` — your COO handles everything.
