# Skill: Summarize Interview

*Turns one interview transcript into a timestamped summary log — the editor reads this to find exactly which minute of footage covers which moment of the story, without rewatching the whole interview.*

Format is based on real examples in `Memory/summaries/` (e.g. `סיכום ראיון עמית ברק.docx`, `סיכום ערן זאגל- C1090.docx`). Match this structure — do not use a generic "core essence / thematic tags" abstract.

---

## When to Use

You have a transcript in `Brain/05-Interviews/[Season]/transcripts/` and need a timestamped breakdown the editor can scan to find footage for a specific scene or event.

**Trigger:** Tell your COO: "Summarize [filename]" or "Summarize everything in transcripts/ for [Season]."

---

## What This Skill Produces

One file per interview, saved to `Brain/05-Interviews/[Season]/summaries/סיכום [interviewee name].md`, in Hebrew, structured like this:

```markdown
# סיכום ראיון [שם המרואיין] [תפקיד/יחידה אם ידוע]

## [שם המקום/האירוע הראשון]: (סרטון [מספר] אם רלוונטי)

[MM:SS]-[MM:SS] — [תיאור תמציתי של מה שקורה/מה שנאמר בקטע הזה. כלול עובדות (מה קרה, מי היה מעורב, החלטות מבצעיות) וגם רגש/פרשנות אישית אם המרואיין מביע אותם.]

[MM:SS]-[MM:SS] — [...]

## [שם המקום/האירוע הבא]:

[MM:SS]-[MM:SS] — [...]

## רגע אישי (אם יש)

[MM:SS]-[MM:SS] — [רגעים בעלי משקל רגשי מיוחד מסומנים בנפרד, בדיוק כמו בדוגמאות]
```

Key structural rules pulled from the real examples:
- **Segment by place/event name**, not by generic chapter number — use the same place names that appear in `Brain/טריטמנט.docx.md` when the interview covers a known chapter (e.g. הבופור, הליטני, יוחמור, הזעותרים, עיינתא).
- **Every entry starts with a timestamp range** (`MM:SS-MM:SS`), taken from the transcript/video, not invented.
- **Reference the video/segment number** when the interview spans multiple files (e.g. `סרטון 001`, `סרטון 003`, or a shot code like `C1090`).
- **Mix fact and feeling** — what operationally happened, and what the interviewee felt or thought at the time, in the same entry when the transcript gives both.
- **Flag standout personal/emotional moments** explicitly (the examples do this — "רגע אישי לאירוע", "מילות גבורה") so the editor knows where the emotional high points are, not just the factual ones.

---

## How to Run It

1. Read the full transcript before writing anything — do not summarize from a partial read.
2. Identify the natural chapter breaks by place/event, in chronological order.
3. Within each chapter, write timestamped entries — err toward more, shorter entries over fewer, long ones. The editor needs to jump to a specific minute, not read a paragraph to find it.
4. Cross-check place/event names against `Brain/טריטמנט.docx.md` so naming stays consistent across interviews covering the same operation.
5. Check other summaries already in the same `summaries/` folder — if two interviews describe the same event, that's useful for the editor to know, but don't force an "overlap" section if the real examples don't have one; just make sure place/event naming matches so the overlap is visible by scanning filenames/headers.

---

## Rules

- **No invented timestamps, quotes, or events** — if the audio/transcript is unclear at a point, say so rather than guessing.
- Write in Hebrew, matching the register of the examples — plain, direct, present-tense-leaning narration.
- Keep entries scannable — this is an edit log, not prose to be read start to finish.

---

## Notes

Run `transcribe-interview` first if the transcript doesn't exist yet.

After writing the `.md` summary, convert it to `.docx` (matching the original examples' style — bold RTL title/headers, plain RTL body) with:

```bash
python3 Tools/scripts/summary_md_to_docx.py \
  "Brain/05-Interviews/[Season]/summaries/סיכום [שם].md" \
  "Brain/05-Interviews/[Season]/summaries/סיכום [שם].docx"
```
