# agent-skills-graft

One vault of agent assets (skills today; agents / commands / rules / plugins next),
grafted onto every agent platform I use — Claude Code, Codex, Cursor, OpenCode, pi —
from a declarative profile instead of by hand.

```
skills/                  # the vault: SKILL.md folders (agentskills.io format)
profiles/global.yaml     # what goes where, machine-wide
profiles/projects/*.yaml # per-project grafts (Phase 2)
src/graft/               # the `graft` CLI (Python, uv)
docs/DESIGN.md           # architecture, research, roadmap
```

## Install

```bash
uv sync                      # dev: then `uv run graft ...`
uv tool install -e .         # or: put `graft` on PATH
```

## Use

```bash
graft status                 # diff profile vs. disk, changes nothing
graft apply --dry-run        # show the plan
graft apply                  # symlink vault skills, `npx skills add` external ones
graft apply --prune          # also remove vault symlinks no longer declared
graft import ~/.codex/skills # adopt loose skills into the vault + profile
graft platforms              # where each platform reads global skills from
graft skills                 # what is in the vault
```

Vault skills are **symlinked** straight into each platform's skills directory, so an edit
in `skills/` is live everywhere. External skills (`source: owner/repo`) are not vendored;
`graft` delegates to [`npx skills add`](https://github.com/vercel-labs/skills), which keeps
its own lock file.

Nothing is ever deleted: real directories that `graft` replaces are moved to
`~/.local/share/graft/backup/<timestamp>/`.

## Profile format

```yaml
targets: [claude-code, codex, cursor, opencode, universal]

skills:
  searching-github-projects: { to: [codex, cursor] }   # vault skill
  mcp-builder: { to: "*" }                             # every target
  frontend-design:                                     # external
    source: anthropics/skills
    to: [cursor, claude-code]
```

See [docs/DESIGN.md](docs/DESIGN.md) for the full design and roadmap.
