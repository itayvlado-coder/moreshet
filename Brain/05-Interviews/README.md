# Interviews — Raw Footage → Transcript → Summary Card

Each season/project gets its own folder (e.g. `Season2-Lebanon/`). Inside:

```
Season2-Lebanon/
├── raw/            Drop interview video/audio files here. Not committed to git (too large).
├── transcripts/    Whisper output — one .txt per interview. Committed.
└── summaries/      One "interview card" per interview — committed. This is what the editor reads.
```

## Workflow

1. Drop the video/audio file into `raw/`.
2. Transcribe it (see `Tools/01-skills/transcribe-interview.md`).
3. Summarize the transcript into a card (see `Tools/01-skills/summarize-interview.md`).
4. Editor reviews the cards in `summaries/` to find which interview covers which part of the story.

## Naming Convention

Name files by interviewee + role, e.g. `01-cohen-battalion-commander.mp4` → same base name for transcript and summary. Keeps everything traceable across the three folders.
