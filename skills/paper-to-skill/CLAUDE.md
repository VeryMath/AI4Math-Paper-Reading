# CLAUDE.md

This repository is a coding-agent-neutral AI4Math paper-to-skill workflow.

Claude Code should use the shared Skill layer under `skills/`; do not create a Claude-specific workflow fork.

## Entry Points

- Read `skills/registry.yaml` for phase routing, input/output contracts, and review gates.
- For user-facing PDF or Markdown paper processing, prioritize `skills/paper-to-skill-workflow/SKILL.md`.
- Use `SKILL.md` only as the top-level compatibility entrypoint.
- Follow `AGENTS.md` for the repository contract.

## Operating Boundary

- Accept `paper.pdf` as the default user input; accept `paper.md` when conversion has already happened.
- Preserve the original `paper.pdf` when provided and the full converted `paper.md`.
- Every accepted or review-worthy SkillCard must include `source.paper_md`, `source.start_line`, and `source.end_line`.
- Keep platform-specific behavior thin; improve the shared `skills/` layer first.
