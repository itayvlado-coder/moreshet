# Workflow: LinkedIn Content

*Full LinkedIn post creation from topic to approved draft — brief, research, write, quality check.*

---

## Trigger

Slash command: `/content [topic]`

Example: `/content why most founders build before they sell`

---

## Input

A topic or angle provided by the CEO. Can be:
- A sentence describing the idea ("why most founders over-engineer before getting customers")
- A question worth exploring ("is AI making business operators more or less strategic?")
- A recent observation ("I noticed our best-performing posts all start with a failure")
- A one-word theme ("focus") — COO will ask a clarifying question to sharpen the angle

---

## Steps

### Step 1 — Brief
Run `Tools/01-skills/brief-post.md`

- Read `Core/voice-dna.md` and `Core/icp-profile.md`
- Turn the input topic into a specific, opinionated angle
- Produce a one-page brief
- **Show the brief to the CEO and get approval before proceeding**
- If the CEO wants to adjust the angle — revise and confirm before moving to Step 2

### Step 2 — Research
Run `Tools/01-skills/research-post.md`

- Using the approved brief, gather specific facts, examples, counterarguments
- Ask the CEO: "Do you have a personal experience or story that connects to this?"
- Produce the research note
- Do not show the research note unless the CEO asks — proceed directly to Step 3

### Step 3 — Write
Run `Tools/01-skills/write-post.md`

- Using the approved brief and research note, write the full post
- Follow all voice rules from `Core/voice-dna.md`
- Produce one strong draft — not multiple options
- Show the draft to the CEO

### Step 4 — Quality Check
Run `Tools/01-skills/quality-check.md`

- Review the draft against voice, mechanics, substance, and audience criteria
- Return a verdict: APPROVED or REVISE
- If REVISE: list specific changes, revise the post, run quality check again
- If APPROVED: present the final post clearly labeled as ready to publish

---

## Output

A final post labeled:

```
FINAL — [topic]
Status: APPROVED

[full post text]

Word count: [X]
```

---

## Rules

- Step 1 (brief) requires CEO approval before continuing. Never skip this gate.
- Never write without an approved brief and completed research.
- Quality check runs on every post. No exceptions.
- If the CEO wants to change direction mid-workflow — stop, revise the brief, restart from Step 2.
- The goal is one excellent post, not speed.

---

## Notes

As you build more skills and agents, this workflow can be extended — a dedicated Copywriter agent for Step 3, a Gatekeeper agent for Step 4. For now, the COO runs all steps.
