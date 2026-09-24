# Essentials — Fast Load Memory

*Compressed current state. Read this at the start of every session for instant context.*

Last updated: 2026-09-24

---

## What This Business Does

Moreshet is a documentary production company that takes raw army footage, event recordings, and interviews and edits them into cohesive multi-episode documentary series — starting with the Israeli army (IDF), with material and interviews in Hebrew.

---

## Active Projects

- **Season 2 — IDF in Lebanon (4-5 episodes).** Interview phase done. Interview summarization pipeline is built and validated: `Brain/05-Interviews/Season2-Lebanon/` (raw/transcripts/summaries), skills `transcribe-interview` and `summarize-interview` (now defaults to fewer/longer timestamped entries per 2026-07-23 decision), and a markdown-to-Word converter (`Tools/scripts/summary_md_to_docx.py`, fixed 2026-07-23 — used to leak literal `**` into Word output). Six summaries done so far: Daniel Loria's Al-Khiam and Bint Jbeil interviews, a Givati brigade-commander interview on Ayta/Bint Jbeil (interviewee name still unconfirmed — flagged in the file), Roed Balus (Shaked battalion commander, replacing Loria) on the Zutrim battle, a drone strike that killed the battalion doctor, and the Lahav-3 tunnel in Kfar Arnon, and two interviews with **Or Hadari** (rifle-company commander — was flagged "Adari"/unconfirmed until his second interview self-identified clearly): one on Ayta/the Bint Jbeil kasbah (incl. a friendly-fire incident), one on the Litani-river defense and executing the Lahav-3 tunnel destruction. Note: transcript filename numbers don't reliably track story chronology. Transcripts keep arriving via different paths (Downloads, or dropped straight into the `transcripts/` folder) — check both when told about a new upload. Two more raw interviews (codenamed "Winston") are untouched in `raw/`.

- **"ימים סגולים" (Gaza Project) — broadcaster submission.** A separate, more mature project: a 9-episode documentary on Givati brigade's first 28 days of the Gaza ground maneuver (Swords of Iron). Lives in `Brain/05-Interviews/Gaza Project/` — has a full synopsis, a complete 9-chapter treatment, and an older lower-priority narrative doc. First deliverable, a broadcaster pitch document (`פורמט הגשה.docx`), was drafted 2026-07-23. Open item: the CEO must confirm which real commander names can be listed as participants before this goes out externally — currently a placeholder.

- **Recurring admin — weekly Givati reserve-duty activity report.** The project work runs under a reserve order (01/07/2026 → 01/01/2027, role תחקירן). Givati requires a weekly hours/activity/location report on their scanned form; first one filled 2026-09-24 for 20–26.09. How-to in `Memory/learning-log.md` (2026-09-24).

---

## Key Decisions Already Made

- Interview summary format is a timestamped chronological log by location/event, not a thematic abstract — see `Memory/decisions.md` (2026-07-20).
- Raw footage lives in `Brain/05-Interviews/[Season]/raw/`, gitignored — never in `Memory/`, never committed.

---

## What We Learned Recently

- Real summary format only became clear after seeing the user's manual examples — don't assume a content format, check for existing examples first.
- Local CPU Whisper is too slow to be practical for ~20 interviews; external ASR/transcription tools are the default, Whisper is the fallback.
- Transcripts often don't state the interviewee's name — infer from context, flag it clearly, and confirm with the user before finalizing rather than guessing.

---

## Current State

Interview phase for Season 2 (IDF in Lebanon) is done. The summarization pipeline is built and proven on four real interviews. Open item: confirm the interviewee's name on the Givati brigade-commander summary (currently flagged "שם לאישור"). Next: transcribe and summarize the two Winston interviews, and get Itay's manual review on the AI-generated summaries before scaling to the rest of the ~20 interviews.

**Stakes:** if this pass isn't done well, the project risks being cut by end of August 2026 — roughly a 6-week runway from today.

---

## System Rules

1. **Git rule** — This repo only: `https://github.com/itayvlado-coder/moreshet.git`. No cross-repo operations. Ever.
2. **Tasks** — All tasks go into the task tool. No todo files in this repo.

---

*Full record: `Memory/learning-log.md`, `Memory/decisions.md`, and `Memory/feedback.md`*
