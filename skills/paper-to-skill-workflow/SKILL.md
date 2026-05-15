---
name: paper-to-skill-workflow
description: Run the complete AI4Math paper-to-skill workflow from a user-provided PDF or Markdown paper. Use when a coding agent should preserve the original paper, convert PDF to paper.md when needed, extract proof-pattern SkillCandidates and SkillCards with line evidence, and optionally route reviewed cards into cross-paper synthesis.
---

# Paper To Skill Workflow

## Purpose

Use this skill as the default user-facing entrypoint. A user should be able to provide a `paper.pdf` and an output directory, then receive reusable `proof_pattern` SkillCandidates, SkillCards, and a review report.

If the user already provides `paper.md`, skip conversion and run extraction directly. Still keep the workflow-level artifact structure.

## Inputs

Accept:

- `paper.pdf` as the primary user input.
- `paper.md` when the paper has already been converted.
- Optional `metadata.json`.
- Optional `human_feedback_state.json`.
- Optional output directory such as `outputs/<research_project_id>/papers/<paper_id>/`.

## Default Flow

```text
paper.pdf
  -> pdf-to-markdown-converter
  -> paper.md
  -> paper-to-skill-extractor
  -> skill_candidates.json + skill_cards/*.yaml + report.md
```

For already-converted papers:

```text
paper.md
  -> paper-to-skill-extractor
  -> skill_candidates.json + skill_cards/*.yaml + report.md
```

## Workflow

1. Choose or create an output paper directory. Prefer `outputs/<research_project_id>/papers/<paper_id>/` when the user is running a project, otherwise use a clear local output folder derived from the input filename.
2. Preserve the original `paper.pdf` when a PDF is provided.
3. If the input is PDF, use `pdf-to-markdown-converter` to create `paper.md`, `mineru/`, and `conversion_report.json`.
4. Treat the full `paper.md` as the source for line-referenced extraction evidence.
5. If `human_feedback_state.json` exists, pass it through to the extraction step.
6. Use `paper-to-skill-extractor` to produce `skill_candidates.json`, `skill_cards/*.yaml`, and `report.md`.
7. In the final response, tell the user which artifacts were written and whether any candidates need review.
8. If the user asks to synthesize across papers, route accepted or review-worthy SkillCards to `cross-paper-skill-synthesizer`.

## Review Gates

- Ask before downloading PDFs from the network.
- Ask before installing or changing dependencies for PDF conversion.
- Ask before accepting unsafe mathematical generalizations.
- Ask before merging or generalizing SkillCards across papers.

## Completion Check

Before finishing, confirm:

- The original `paper.pdf` is preserved when provided.
- The full `paper.md` exists.
- `skill_candidates.json` is valid JSON.
- Each accepted or review-worthy SkillCard has `source.paper_md`, `source.start_line`, and `source.end_line`.
- `report.md` separates accepted, needs-review, and rejected candidates.
