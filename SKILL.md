---
name: paper-to-skill
description: Use when extracting reusable AI4Math research skills from papers, especially PDF-to-SkillCard workflows, paper triage, PDF preparation, proof-pattern extraction, and cross-paper SkillCard synthesis for a coding-agent-neutral paper-to-skill workflow.
---

# Paper To Skill

This repository is a Skill-first paper-to-skill workflow package for AI4Math auto research. Codex is the reference operator, but the shared Skill layer is intended for any capable coding agent.

## Entry Point

Start user-facing paper-to-skill work from:

```text
skills/paper-to-skill-workflow/SKILL.md
```

Use `skills/registry.yaml` to inspect phase order, review gates, and optional upstream or downstream Skills.

This root `SKILL.md` is not the workflow driver. It is a compatibility entrypoint for platforms that expect one top-level Skill file.

## Operating Boundary

- Accept `paper.pdf` as the default user input; accept `paper.md` when conversion has already happened.
- Preserve the original `paper.pdf` when provided and the full converted `paper.md`.
- Do not require external LLM APIs for extraction; the active coding agent is the extraction engine.
- Keep platform-specific adapters thin and point them back to `skills/registry.yaml` and the shared `skills/` layer.
- Every accepted or review-worthy SkillCard must include `source.paper_md`, `source.start_line`, and `source.end_line`.
- Treat structured JSON, YAML, and reports as indexes or review artifacts, not replacements for the original paper.
- Use human feedback and review decisions as explicit workflow state when available.
