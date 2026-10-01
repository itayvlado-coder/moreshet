# Essentials — Fast Load Memory

*Compressed current state. Read this at the start of every session for instant context.*

Last updated: 2026-10-02

---

## What This Business Does

Moreshet is a documentary production company that takes raw army footage, event recordings, and interviews and edits them into cohesive multi-episode documentary series — starting with the Israeli army (IDF), with material and interviews in Hebrew.

---

## Active Projects

- **Season 2 — IDF in Lebanon (4-5 episodes).** Interview phase done. Interview summarization pipeline is built and validated: `Brain/05-Interviews/Season2-Lebanon/` (raw/transcripts/summaries), skills `transcribe-interview` and `summarize-interview` (now defaults to fewer/longer timestamped entries per 2026-07-23 decision), and a markdown-to-Word converter (`Tools/scripts/summary_md_to_docx.py`, fixed 2026-07-23 — used to leak literal `**` into Word output). Six summaries done so far: Daniel Loria's Al-Khiam and Bint Jbeil interviews, a Givati brigade-commander interview on Ayta/Bint Jbeil (interviewee name still unconfirmed — flagged in the file), Roed Balus (Shaked battalion commander, replacing Loria) on the Zutrim battle, a drone strike that killed the battalion doctor, and the Lahav-3 tunnel in Kfar Arnon, and two interviews with **Or Hadari** (rifle-company commander — was flagged "Adari"/unconfirmed until his second interview self-identified clearly): one on Ayta/the Bint Jbeil kasbah (incl. a friendly-fire incident), one on the Litani-river defense and executing the Lahav-3 tunnel destruction. Note: transcript filename numbers don't reliably track story chronology. Transcripts keep arriving via different paths (Downloads, or dropped straight into the `transcripts/` folder) — check both when told about a new upload. **2026-10-02:** 15 more summaries arrived, written by a friend on the production outside our pipeline. They are filed per interviewee under `summaries/`: brigade commander **נתנאל שמכה** (5 parts), sayeret commander **עמית** (7), and 52 battalion commander **יול / אור** (3, plus his father). The episode outline (`אאוטליין עונה 2 - לבנון (טיוטה)`) is at **version 5**. It closes the "דפיקה בדלת" and Zutar al-Gharbiya gaps and confirms that Shaked and 52 are separate battalions; it ends with a list of cross-source contradictions for the CEO to settle.

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

Interview phase for Season 2 (IDF in Lebanon) is done. The summarization pipeline is built and proven on four real interviews. Brigade commander identified (נתנאל שמכה); the old "שם לאישור" summary in `summaries/ישן/` is almost certainly his. Outline v5 is the working skeleton. Open items: settle the contradictions listed at the end of the outline; still no material on "הפרד ומשול" (Kunin) or the "הוקי" ambush.

**Stakes:** if this pass isn't done well, the project risks being cut by end of August 2026 — roughly a 6-week runway from today.

---

## System Rules

0. **Classified material** — anything marked סודי/סודי ביותר (e.g. photos of IDF briefing screens) never goes into this repo; it syncs to GitHub.

1. **Git rule** — This repo only: `https://github.com/itayvlado-coder/moreshet.git`. No cross-repo operations. Ever.
2. **Tasks** — All tasks go into the task tool. No todo files in this repo.

---

*Full record: `Memory/learning-log.md`, `Memory/decisions.md`, and `Memory/feedback.md`*
