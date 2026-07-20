# Skill: Transcribe Interview

*Turns a raw interview video/audio file into a text transcript using local Whisper — nothing leaves the machine.*

---

## When to Use

You have a raw interview video/audio file in `Brain/05-Interviews/[Season]/raw/` and need a text transcript before it can be summarized.

**Trigger:** Tell your COO: "Transcribe [filename]" or "Transcribe everything in raw/ for [Season]."

---

## How to Run It

For a single file (Hebrew interview, e.g.):

```bash
whisper "Brain/05-Interviews/Season2-Lebanon/raw/01-cohen-battalion-commander.mp4" \
  --language Hebrew \
  --model medium \
  --output_format txt \
  --output_dir "Brain/05-Interviews/Season2-Lebanon/transcripts"
```

- `--model medium` balances speed and accuracy on a laptop. Use `small` if it's too slow, `large` if accuracy matters more than time.
- `--language Hebrew` skips language auto-detection and improves accuracy.
- Output filename matches the input's base name — keep raw/transcript/summary filenames aligned (see `Brain/05-Interviews/README.md`).

To batch an entire folder, loop over every file in `raw/` and run the same command per file.

---

## Rules

- **Spot-check the first transcript** against the actual audio before trusting a whole batch — Hebrew accuracy varies by audio quality and accent.
- Transcripts are committed to git (`Brain/05-Interviews/**/transcripts/`); raw video is not (too large, gitignored).
- If a transcript looks badly garbled, re-run with `--model large` before giving up on it.

---

## Notes

Whisper and ffmpeg run locally (installed via Homebrew + pip during setup). No internet upload of footage required.
