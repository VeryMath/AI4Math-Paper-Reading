---
name: paper-to-skill-extractor
description: Extract reusable mathematical research skills from Markdown papers, especially proof-pattern skills such as descent lemmas, inequality relaxations, telescoping bounds, error decompositions, Lyapunov arguments, concentration bounds, Galerkin/Cea arguments, Aubin-Nitsche duality, and Lax-Milgram well-posedness. Use when Codex is asked to turn a math paper, proof, theorem section, convergence analysis, stability analysis, or error analysis into SkillCandidate JSON, SkillCard YAML, or a paper-to-skill report without relying on external LLM APIs.
---

# Paper To Skill Extractor

## Overview

Use this skill to extract reusable mathematical research methods from papers. Do not summarize the paper. Extract transferable methods that an agent could later call on a different research task.

## Inputs

Accept:

- A Markdown paper such as `paper.md`.
- Optional `human_feedback_state.json` from the same research project.

## Workflow

1. Preserve the input paper exactly as `paper.md` in the output directory when writing artifacts.
2. If `human_feedback_state.json` exists, read `focus_updates`, `negative_preferences`, `skill_decisions`, and `next_step_directives` before selecting evidence spans.
3. Read the full paper or the user-specified section. Track 1-based line numbers from the Markdown source.
4. Identify high-value evidence spans: theorem statements, lemmas, propositions, assumptions, proofs, convergence analysis, stability analysis, error analysis, generalization bounds, lower bounds, and appendix proofs.
5. For each span, decide whether it contains a reusable `proof_pattern`. Reject paper-specific conclusions, background exposition, related work, and experiment results.
6. Extract `SkillCandidate` objects with source evidence, reusable intent, inputs, outputs, assumptions, core steps, trigger keywords, limitations, score, and confidence.
7. Generalize away paper-specific names such as "our algorithm", "Assumption 2", "Theorem 3", and local notation while preserving necessary mathematical conditions.
8. Score each candidate with the rubric. Mark it as `accepted_candidate`, `needs_review`, or `rejected`.
9. Write one Skill Card YAML per accepted or review-worthy candidate, plus `skill_candidates.json` and `report.md`.
10. In `report.md`, explain how human feedback changed evidence selection, scoring, or rejection decisions.
11. Verify every generated skill has source line references back to `paper.md`.

## Required References

Read these only as needed:

- `references/extraction_protocol.md`: detailed extraction workflow and rejection rules.
- `references/proof_pattern_taxonomy.md`: first-pass taxonomy of proof patterns and trigger cues.
- `references/quality_rubric.md`: scoring formula and status thresholds.
- `references/schemas.md`: required output fields.

## Output Files

Use this structure unless the user specifies another output directory:

```text
outputs/<paper_id>/
├── paper.md
├── skill_candidates.json
├── skill_cards/
│   └── <skill_name>.yaml
└── report.md
```

Use the templates in `assets/` for artifact shape:

- `assets/skill_candidate_template.yaml`
- `assets/skill_card_template.yaml`
- `assets/report_template.md`

## Extraction Rules

Only extract a method when it satisfies all of these:

- It can transfer to another paper, proof, or math research task.
- It has clear inputs and outputs.
- It has identifiable assumptions or applicability conditions.
- It has operational core steps that an agent could follow.
- It can be tested, checked, or reviewed.

Do not extract:

- A theorem result that is only true for this paper's model.
- A broad contribution statement without operational steps.
- Literature review, background motivation, implementation notes, or experiments.
- A proof step whose missing assumptions make it mathematically unsafe unless it is marked `needs_review`.

When `human_feedback_state.json` exists:

- Prioritize proof patterns named in `focus_updates` or `next_step_directives`.
- Down-rank candidates that match `negative_preferences`.
- Apply user `skill_decisions` such as `accept`, `revise`, `reject`, or `merge` when re-running extraction.
- Never accept an unsafe generalization only because the user expressed interest; mark it `needs_review`.

## Completion Check

Before finishing, confirm:

- `paper.md` is preserved.
- `skill_candidates.json` is valid JSON.
- Each Skill Card has `source.paper_md`, `source.start_line`, and `source.end_line`.
- The report separates accepted, needs-review, and rejected candidates.
- At least one note explains any mathematical risk or uncertainty.
