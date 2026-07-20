# Skill: Create a New Skill

*Build a new reusable skill file and add it to the OS.*

---

## When to Use

When you have done the same thing three or more times and want to stop rebuilding it from scratch.

**Trigger:** Tell your COO: "Create a skill for [what you keep doing]."

---

## What This Skill Produces

A complete skill file saved to `Tools/01-skills/[skill-name].md`, ready to use.

---

## How to Run

1. **Name the skill.** Ask if not provided: "What do you want to call this skill? Use a short, descriptive name — e.g. `summarize-article`, `onboard-customer`, `prepare-pitch`."

2. **Understand the job.** Ask:
   - "What triggers this skill — when would you use it?"
   - "What does it take as input?"
   - "What does it produce as output?"
   - "Are there any rules it must follow every time?"

3. **Check for existing overlap.** Scan `Tools/01-skills/` — is there already a skill that does this? If yes, consider extending that skill rather than creating a new one.

4. **Write the skill file** using this structure:
   ```
   # Skill: [Name]
   *One sentence: what this skill does.*
   ## When to Use
   ## What This Skill Produces
   ## How to Run
   ## Rules
   ## Notes (optional)
   ```

5. **Save to** `Tools/01-skills/[skill-name].md`

6. **Update** `Tools/README.md` — add the new skill to the table.

7. **Update** the COO file — add the skill to the Skills list in the COO's `## Skills and Workflows Available` section.

---

## Rules

- Every skill must have a clear trigger (when to use it) and a clear output (what it produces).
- Skills are reusable — write them so any agent can run them, not just the COO.
- Keep it simple. A skill that tries to do three things is three skills.
