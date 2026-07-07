# Agent instructions

Follow **`CLAUDE.md`** in this repository for all engineering standards, skill routing,
default delivery stacks, and definition of done.

## Cursor

Skills are synced into Cursor via:

```bash
./scripts/sync-cursor-skills.sh --scope both
```

After syncing, Cursor discovers skills from `.cursor/skills/` (this repo) and
`~/.cursor/skills/` (global). Read the relevant `SKILL.md` before acting when a skill
covers the task.
