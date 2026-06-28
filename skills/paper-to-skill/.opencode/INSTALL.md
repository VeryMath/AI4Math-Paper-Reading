# OpenCode Loading Notes

This repository is a coding-agent-neutral AI4Math paper-to-skill workflow. The shared Skill layer lives under `skills/`.

## Use

1. Read `AGENTS.md` for the repository contract.
2. Read `skills/registry.yaml` for phase routing, input/output contracts, and review gates.
3. For user-facing PDF or Markdown paper processing, start from `skills/paper-to-skill-workflow/SKILL.md`.
4. Treat `SKILL.md` as a top-level compatibility entrypoint, not as a separate workflow.

## Boundary

Do not fork platform-specific behavior into `.opencode/`. Improve the shared Skill layer under `skills/` first.
