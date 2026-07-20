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
