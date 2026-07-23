# Decisions

*Strategic choices that have been made. The system never revisits settled questions.*

---

## How to Use

When you make a significant decision — about direction, positioning, tools, team, product — log it here.

Include:
- What was decided
- Why it was decided (the reasoning that was good at the time)
- What it means going forward

**Format:**
```
## [Date] — [Decision title]
**Decided:** [What was chosen]
**Why:** [The reasoning]
**Means:** [What changes going forward]
```

---

## Decisions

## 2026-07-20 — Interview summary format: timestamped chronological log
**Decided:** Interview summaries (`Tools/01-skills/summarize-interview.md`) follow a chronological, timestamped log format — segmented by location/event name, each entry starting with an MM:SS-MM:SS range, referencing video/segment numbers — matching the style of the original manually-produced examples. Not a thematic "core essence + tags" abstract.
**Why:** This is the format the editor actually needs to jump to the right minute of footage; it matches how the manual examples (סיכום ראיון עמית ברק, סיכום ערן זאגל) were already built.
**Means:** Every future auto-generated summary (Whisper or external ASR) should match this structure. Output as both `.md` and `.docx` (via `Tools/scripts/summary_md_to_docx.py`) to match the existing Word-based workflow.

## 2026-07-20 — Raw footage lives in Brain/05-Interviews, never in Memory or git
**Decided:** Raw interview video files live in `Brain/05-Interviews/[Season]/raw/`, gitignored. Transcripts and summary cards (in the same season folder) are committed to git.
**Why:** `Memory/` is reserved for small, compressed state files per the system's own convention; raw video (multi-GB files) doesn't belong there and would break git if committed (files far exceed practical repo size).
**Means:** Any new raw footage the user drops in should go straight into this structure, not into `Memory/`.

## 2026-07-23 — Real personnel names never go into external-facing documents without explicit sign-off
**Decided:** Any document meant to leave the company (broadcaster submissions, pitches, GTM material) must ship with a placeholder instead of real commander/soldier names, even when those names are already known internally from interview files, until the CEO explicitly confirms them for that specific document.
**Why:** The people named are active/reserve IDF personnel; a broadcaster submission is a real external disclosure, not an internal working file — the bar for including a real name is higher than for an internal interview summary.
**Means:** On the "ימים סגולים" broadcaster pitch (`Brain/05-Interviews/Gaza Project/פורמט הגשה.docx`), the participants field was left as an explicit placeholder rather than filled from the older narrative doc's names. Apply the same rule to any future external-facing document for either project.
