# Learning Log

*What the system has learned. Add an entry whenever a session produces a strong insight, pattern, or finding worth keeping.*

---

## How to Use

After every significant session, ask: did we discover something that should shape future sessions?

If yes, log it here. Keep entries short and specific — written so a future version of you can act on it without needing the original context.

**Format:**
```
## [Date] — [Short title]
[What was learned. Specific. Actionable.]
```

---

## Log

## 2026-07-20 — Real summary format is a timestamped log, not a thematic abstract
When we first designed the interview-summarization skill, the assumption was a "core essence + thematic tags" abstract. The real manual examples (Memory/summaries → moved to Brain/05-Interviews) showed the actual format needed: a chronological log segmented by location/event name, with MM:SS-MM:SS timestamp ranges per entry, referencing video/segment numbers. Always check for real examples before designing a content format from assumptions — the assumed format was structurally wrong even though the individual facts would have been correct.

## 2026-07-20 — External ASR transcripts work as well as (or better than) local Whisper
Local Whisper on this Intel Mac (CPU-only, no GPU) took over an hour to transcribe a single ~16-minute Hebrew interview with the "medium" model — impractical for ~20 interviews. An externally-transcribed VTT file (uploaded by the user) worked immediately and produced a usable, timestamped Hebrew transcript. Going forward, prefer external transcription tools when available; only fall back to local Whisper (`Tools/01-skills/transcribe-interview.md`) when no faster option exists. Any transcript format works as long as timestamps are preserved (SRT/VTT/JSON — not plain unstamped text).

## 2026-07-22 — New transcripts don't always arrive the same way, and the interviewee is often unnamed
Two more interviews were summarized this session, and neither arrived the way the pipeline assumed: one VTT showed up in `~/Downloads` (had to be copied into `Brain/05-Interviews/Season2-Lebanon/transcripts/` manually), the other was dropped directly into that transcripts folder without ever touching Downloads. When told "I uploaded a transcript," check both locations (and sort by mtime) rather than assuming one path. Separately, the ASR transcripts frequently never state the interviewee's name or rank on tape — it has to be inferred from context (who reports to whom, who they say they replaced, self-introduction attempts caught mid-take). When identity is inferred rather than stated, mark it clearly in the summary file (both a header note and a naming placeholder if unsure) and ask the user to confirm before treating the name as final — never silently commit to a guessed name.

## 2026-07-22 — User asked for longer, fewer timestamped chunks in one summary
`Tools/01-skills/summarize-interview.md` currently says to err toward more, shorter entries. On the "רועד בלוס" summary, the CEO explicitly asked to try longer segments instead. Treated as a one-off adjustment for that summary, not yet a rule change to the skill file — only one data point so far. Watch for this being requested again on future summaries; if it repeats, promote it to `Memory/decisions.md` and update the skill file's guidance.

## 2026-07-23 — `summary_md_to_docx.py` leaked literal `**` into Word output
The script's body-paragraph branch never parsed inline `**bold**` markdown — it just wrote the raw characters into the run, so every emphasized quote in a summary showed literal asterisks in the delivered `.docx`. This affected three files already sent to the CEO before it was caught (found by chance while reading a paragraph back to debug something else, not by a deliberate check). Fixed by splitting on `**` and toggling bold per segment (`add_run_with_inline_bold`), then regenerated and re-sent the affected files. Actionable: after any change to this script — or before trusting its output on a new document type — read a paragraph back via python-docx (or render to PDF if LibreOffice is available) rather than assuming the conversion matches the source markdown.

## 2026-07-23 — A later interview resolved an earlier one's unconfirmed identity — and filename numbers don't track story order
The company commander flagged as "אדרי"/"unconfirmed" in an earlier summary turned out, in a second interview from the same person, to self-identify clearly twice: **אור הדרי**. Went back and corrected the identity note in the earlier summary file rather than leaving it stale, without renaming the file itself (it had already been delivered to the CEO — renaming would break that reference). Separately: the second interview's transcript filename carried a "002" suffix, but it was chronologically the *first* of his two interviews — the numbered one came first in the story, the unnumbered one was the follow-up. Don't assume a filename's number reflects chronological/story order; check the content itself.

## 2026-07-23 — A second, more mature project exists: "Gaza Project" / "ימים סגולים"
Discovered `Brain/05-Interviews/Gaza Project/` — a separate, further-along project from Season 2 (Lebanon): a 9-episode documentary on Givati brigade's first 28 days of the ground maneuver in Gaza during Swords of Iron. It already has a full synopsis (`סינופסיס ימים סגולים.docx` — this is where the series title "ימים סגולים" comes from), a complete 9-chapter treatment (`טריטמנט.docx.md`), and an older, denser narrative doc (`מורשת גבעתי חרבות ברזל- צפון הרצועה_ (2).docx`) that the CEO explicitly said is outdated and should carry the least weight — use it only to fill gaps, and defer to the newer treatment/synopsis on any conflict. This project moved to submission stage first: a broadcaster pitch document (`פורמט הגשה.docx`) was drafted this session.
