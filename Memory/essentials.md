# Essentials — Fast Load Memory

*Compressed current state. Read this at the start of every session for instant context.*

Last updated: 2026-07-20

---

## What This Business Does

Moreshet is a documentary production company that takes raw army footage, event recordings, and interviews and edits them into cohesive multi-episode documentary series — starting with the Israeli army (IDF), with material and interviews in Hebrew.

---

## Active Projects

- **Season 2 — IDF in Lebanon (4-5 episodes).** Interview phase done. Interview summarization pipeline is now built and validated: `Brain/05-Interviews/Season2-Lebanon/` (raw/transcripts/summaries), skills `transcribe-interview` and `summarize-interview`, and a markdown-to-Word converter (`Tools/scripts/summary_md_to_docx.py`). Two real summaries done so far — Daniel Loria's Al-Khiam and Bint Jbeil interviews (videos #1 and #3 of 3). Video #2 (Loria) is being transcribed externally by Itay. Two more raw interviews (codenamed "Winston") are untouched in `raw/`.

---

## Key Decisions Already Made

- Interview summary format is a timestamped chronological log by location/event, not a thematic abstract — see `Memory/decisions.md` (2026-07-20).
- Raw footage lives in `Brain/05-Interviews/[Season]/raw/`, gitignored — never in `Memory/`, never committed.

---

## What We Learned Recently

- Real summary format only became clear after seeing the user's manual examples — don't assume a content format, check for existing examples first.
- Local CPU Whisper is too slow to be practical for ~20 interviews; external ASR/transcription tools are the default, Whisper is the fallback.

---

## Current State

Interview phase for Season 2 (IDF in Lebanon) is done. The summarization pipeline is built and proven on two real interviews. Next: finish Loria's video #2, transcribe and summarize the two Winston interviews, and get Itay's manual review on the AI-generated summaries before scaling to the rest of the ~20 interviews.

**Stakes:** if this pass isn't done well, the project risks being cut by end of August 2026 — roughly a 6-week runway from today.

---

## System Rules

1. **Git rule** — This repo only: `https://github.com/itayvlado-coder/moreshet.git`. No cross-repo operations. Ever.
2. **Tasks** — All tasks go into the task tool. No todo files in this repo.

---

*Full record: `Memory/learning-log.md`, `Memory/decisions.md`, and `Memory/feedback.md`*
