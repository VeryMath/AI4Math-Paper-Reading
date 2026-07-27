---
name: ai4math-paper-reading
description: Route AI4Math paper-reading tasks to the appropriate bundled skill package.
---

# AI4Math Paper Reading

Use this repository as a routing layer for mathematical paper-reading
workflows.

## Packages

- `skills/paper-to-skill/`: run the full paper-to-skill workflow, including
  PDF preparation, triage, extraction, and synthesis. Read `SKILL.md` and
  `README.md` before use.
- `skills/math-paper-reading/`: paper-reading assistant modules. Start with
  `SKILL.md`, `README.md`, and `agent_router.md`.
- `skills/after-ocr/`: review formula-heavy OCR Markdown, apply evidence-backed
  local repairs, and maintain complete coverage and audit logs.
- `skills/graph-theory-paper-reading/`: deep-read graph theory papers and
  build structured LaTeX reports and proof trees.

Prefer package-local instructions over this router when running a concrete
workflow.
