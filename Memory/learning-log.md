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
