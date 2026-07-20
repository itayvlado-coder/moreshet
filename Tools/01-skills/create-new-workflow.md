# Skill: Create a New Workflow

*Build a new multi-step workflow and wire it to a slash command.*

---

## When to Use

When a task has multiple distinct steps that always run in the same order and benefit from being triggered as one command. A workflow is a sequence of skills with a single entry point.

**Trigger:** Tell your COO: "Create a workflow for [process]."

---

## What This Skill Produces

1. A workflow file saved to `Tools/02-workflows/[workflow-name].md`
2. A slash command file saved to `.claude/commands/[command-name].md`
3. Updated `Tools/README.md`

---

## How to Run

1. **Define the workflow.** Ask if not already clear:
   - "What is the trigger — when would you run this?"
   - "What does the user input at the start?"
   - "What are the steps, in order?"
   - "What does the final output look like?"

2. **Map the skills.** For each step — does a skill already exist for it? If yes, reference it. If no, note that a new skill needs to be built first (use `create-new-skill`).

3. **Write the workflow file** using this structure:
   ```
   # Workflow: [Name]
   *One sentence: what this workflow does end to end.*
   ## Trigger
   ## Input
   ## Steps (ordered)
   ## Output
   ## Rules
   ```

4. **Write the slash command file** at `.claude/commands/[name].md`:
   ```
   You are running the [workflow name] workflow.
   Input: $ARGUMENTS
   Read Tools/02-workflows/[workflow-name].md and execute it step by step.
   Do not skip steps. Do not ask for confirmation between steps unless you need clarification.
   ```

5. **Save both files.** Update `Tools/README.md`.

---

## Rules

- A workflow is a sequence of existing skills. Build the skills first, then the workflow.
- The slash command should be short and memorable: `/content`, `/research`, `/review`
- Workflows are for repeatable multi-step processes. One-off sequences go to the COO directly.
- Always include a rule about what happens if a step fails or needs human input.
