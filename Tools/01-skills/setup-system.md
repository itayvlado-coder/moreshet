# Skill: Setup System

*The first-session skill. Builds the entire OS foundation in one conversation.*

---

## When to Run

This skill runs automatically on the first session — when Core files still contain placeholder text like `[YOUR BUSINESS NAME]`. The COO detects this and starts setup without being asked.

**Manual trigger:** Tell your COO: "Run setup."
**Slash command:** `/setup`

---

## What This Skill Does

Guides the CEO through building every foundational file in one session. The COO asks the questions. The CEO answers. The COO writes everything.

---

## Phase 1 — Name the COO

**Goal:** Give the COO a real name.

COO asks:
> "Before we start — what name do you want to give me? This is the name you will use to talk to me every day."

Once answered:
- Rename `Agents/[YOUR-COO-NAME]-COO.md` to `Agents/[Name]-COO.md`
- Replace all instances of `[YOUR_COO_NAME]` in the file
- Confirm: "From now on I am [Name]. Let's build your OS."

---

## Phase 2 — Core Files

**Goal:** Fill in project-brief.md, voice-dna.md, and icp-profile.md through conversation.

### project-brief.md questions

Ask these one at a time. Write the answer into the file as you go.

1. "What does your business do? Describe it like you would to a smart friend who has never heard of it."
2. "What problem does it solve — and why does that problem matter right now?"
3. "What makes you different? What do you have that a competitor cannot easily copy?"
4. "Who is your primary customer? Describe them specifically — their job, their situation, what they struggle with."
5. "How do you make money? What do customers pay for and how much?"
6. "Write one sentence that captures what you do, who you do it for, and why it matters."

After the last answer: write and save the complete `Core/project-brief.md`. Show it to the CEO and ask: "Does this feel right? Anything to change?"

### voice-dna.md questions

1. "Think of someone whose communication style you admire — a person, a brand, a writer. What do you like about how they communicate?"
2. "Give me four words that describe how your brand should sound."
3. "What are 2-3 things you never want your brand to say or sound like?"
4. "Do you write formally or casually? Long sentences or short?"

Write and save `Core/voice-dna.md`. Show it. Ask for changes.

### icp-profile.md questions

1. "Who is your ideal customer — job title, situation, what stage of life or business are they in?"
2. "What does their typical day look like? What are they stressed about?"
3. "What have they already tried before finding you? What did not work?"
4. "What does success look like to them — what would make them say it was worth it?"
5. "What makes them hesitate? What is their #1 objection?"

Write and save `Core/icp-profile.md`. Show it. Ask for changes.

---

## Phase 3 — CLAUDE.md

**Goal:** Write the system's constitution.

Using everything from Phase 2 and the git repo URL, write and save `CLAUDE.md`. Replace all placeholder values.

Ask: "What is your GitHub repo URL?" — then fill in the git rule.

Show the completed CLAUDE.md. Ask for any changes.

---

## Phase 4 — Memory/essentials.md

**Goal:** Auto-fill the fast-load memory file.

Using Core files and everything from the conversation, write `Memory/essentials.md`:
- What this business does (1-2 sentences from the brief)
- Active projects (ask: "What are you working on right now?")
- System rules (from CLAUDE.md)
- Current state (ask: "Where are you in the business right now — what is the next milestone?")

The learning-log, decisions, and feedback files stay empty. They earn entries as real work happens.

---

## Phase 5 — GitHub

**Goal:** Connect the OS to the cloud vault.

Ask: "Do you have a GitHub repo ready? If yes, give me the URL."

If yes: run the git setup (init, remote add, first commit, push).
If no: walk them through creating one at github.com — new repository, private, copy the URL — then run the git setup.

Confirm: "Your OS is now backed up to GitHub. Every future session closes the loop there."

---

## Phase 6 — Done

Say:

> "Setup is complete. Here is what we built:
> - Your Core: [business name], [voice], [customer]
> - Your Memory: essentials loaded
> - Your CLAUDE.md: written
> - GitHub: connected
>
> The system knows your business. What do you want to work on first?"

---

## Notes

Do not rush Phase 2. The quality of the Core files determines the quality of everything the system produces from this point forward. Take the time to get them right.
