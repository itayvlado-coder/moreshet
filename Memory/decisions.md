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

## 2026-07-23 — Interview summaries default to fewer, longer timestamped entries
**Decided:** `Tools/01-skills/summarize-interview.md` now instructs merging continuous action into fewer, wider timestamp-range entries, reversing its original "more, shorter entries" guidance.
**Why:** The CEO asked for longer segments on three summaries in a row (Roed Balus, then explicitly again on Or Hadari's first interview, 2026-07-22 and 2026-07-23) — a clear repeated preference, not a one-off.
**Means:** All future auto-generated interview summaries should default to this style unless told otherwise for a specific summary.

## 2026-07-23 — Real personnel names never go into external-facing documents without explicit sign-off
**Decided:** Any document meant to leave the company (broadcaster submissions, pitches, GTM material) must ship with a placeholder instead of real commander/soldier names, even when those names are already known internally from interview files, until the CEO explicitly confirms them for that specific document.
**Why:** The people named are active/reserve IDF personnel; a broadcaster submission is a real external disclosure, not an internal working file — the bar for including a real name is higher than for an internal interview summary.
**Means:** On the "ימים סגולים" broadcaster pitch (`Brain/05-Interviews/Gaza Project/פורמט הגשה.docx`), the participants field was left as an explicit placeholder rather than filled from the older narrative doc's names. Apply the same rule to any future external-facing document for either project.

## 2026-10-21 — צל״ש interview mapping is organized by event ("תיק אירוע")
**Decided:** The interview list for the Givati citation documentation is one file per battle or event (summary with sourced numbers, recipients, people to locate, the fallen as a separate decision, interview points, contradictions, logistics). No priority column, and no meta notes about our own process.
**Why:** The CEO reviewed a Nahal Oz example and approved it ("מצויין") after three changes. Grouping by event avoids interviewing the same battle twice and lets the photographer batch shoots by unit.
**Means:** Files live in `Brain/05-Interviews/צלשים 7.10/`, numbered 00–08 with whole numbers only, each with a PDF next to it.

## 2026-10-25 — The צל״ש documentation covers 7.10 only, not the ground maneuver
**Decided:** Drop the maneuver. Only 7.10 and the days until the ground maneuver are mapped (67 rows, 56 people in the 24.10 spreadsheet). The maneuver file was deleted.
**Why:** The CEO's call.
**Means:** Ignore the "תמרון – עזה" tab and maneuver-only rows in future spreadsheet versions.

## 2026-10-25 — Claims beyond a narrator's own arena are attributed and flagged, not stated as fact
**Decided:** When one narrator claims wider impact (Atias on brigade 401's deployment, opening route 232, sending a brigadier general to the rear), the file says "לפי אטיאס" and lists the claim in a "טענות שצריך לאמת" table, next to who can confirm it. Source-process mentions (that a detail came from voice recordings) are left out of the documents.
**Why:** Atias's 29-minute account risked making his arenas carry the whole story. The CEO approved splitting Nova from Kissufim and attributing the big claims, then asked to drop the "recordings" wording.
**Means:** Apply the same rule to any future single-narrator material, including Alfasi's voice notes if they arrive.

## 2026-11-17 — Interview corrections go into every layer we own; the personal cards stay untouched
**Decided:** Each interview updates the event files (00–08), the internal force files, the division submission data and PDFs, and the brigade deck in one pass. The personal cards in Drive (owner gizbar1986) are never edited. Their corrections go into "תוספות לכרטיסים" files, which the CEO forwards.
**Why:** The CEO asked for it after the audit showed the deck and submission were weeks behind the interviews.
**Means:** "Done" for an interview means all layers are rebuilt, not only its story files.

## 2026-11-17 — Facts confirmed by the CEO
**Decided:** Maatouk fitted out the brigade commander's Namer alone, so the claim in Algarbli's card is removed. Zilberman is a reserve major (רס״ן מיל׳). The Namer reached Kfar Aza at about 14:00–14:30; the one that took seven anti-tank hits was Golani's.
**Why:** The CEO's confirmation, matching Maatouk's and Fares's interviews.
**Means:** Treat these as settled. Tzabar's entry time and the first-house time are still open: write "אחר הצהריים", not a clock time.

## 2026-11-17 — Battle flows: one map per arena, shown three ways
**Decided:** Each arena gets a battle-flow map (OSM base, numbered events in time order, color per force, hollow marker for an estimated location). It appears as a deck slide, as an animated live page, and in one interactive overview link where clicking an arena opens its flow. There are also click-per-event PowerPoint and Google Slides decks, and a printable four-panel slide per arena.
**Why:** The CEO approved the Kfar Aza example and asked for all arenas, a single shareable link, a print version and Google Slides.
**Means:** Sources are `battle_maps.py`, `build_live.py`, `build_pptx.py`, `build_print.py` and `build_gslides.py` in `הגשה לאוגדה/מצגת חטיבה/`. Yakhini and Mishmar HaNegev have no event file, so they have no map.

## 2026-11-22 — Every interview transcript also goes to Drive as Word
**Decided:** Each צל״ש interview transcript gets a Word copy, `תמלול - <name>.docx`, in the voice-note format: a title, a source line, then one line per segment with `[HH:MM:SS]`. It is uploaded to the Drive folder "תמלולי ראיונות" under "ראיונות מצולמים". The internal notes ("לא להזכיר במצלמה", unclear names) stay in the repo md and are not uploaded. This is done for every new interview without being asked, and the CEO's request counts as standing approval for this upload.
**Why:** The CEO wants the full transcripts, with timestamps, in Drive next to the stories, the same way the voice-note transcripts are.
**Means:** Built by `Tools/scripts/transcript_md_to_docx.js`; the step is in `Tools/01-skills/transcribe-interview.md`. All 16 transcripts from 3.11 to 16.11 were uploaded on 22.11.
