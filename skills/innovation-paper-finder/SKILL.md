---
name: innovation-paper-finder
description: Search for papers that may provide new methods, new theory, sharper bounds, different assumptions, proof techniques, lower bounds, abstractions, or cross-domain transfers for a math research direction. Use when Codex should look beyond nearest-neighbor related work and generate innovation_candidates.json with reasons and risks.
---

# Innovation Paper Finder

## Purpose

Use this skill to find papers that may create new research angles. This is not ordinary related-work retrieval. Search for transferable ideas, proof techniques, sharper assumptions, negative results, and adjacent-domain methods.

## Inputs

- `outputs/<research_project_id>/research_profile.json`
- Optional `candidate_papers.json`, seed papers, or user constraints.

## Workflow

1. Read the research profile and any existing candidate list.
2. Identify innovation routes: new proof technique, sharper bound, weaker assumption, cross-domain transfer, lower bound, alternative formulation, or new abstraction.
3. Use Codex's available search or browsing capability for each route.
4. Prefer primary paper pages and open full text where available.
5. For each candidate, explain why it may help and what research angle it suggests.
6. Record risks such as weak relevance, high reading cost, speculative transfer, or paywalled access.
7. Write `innovation_candidates.json` using `references/schemas.md`.
8. Write `innovation_report.md` with recommended next actions and checkpoint questions.

## Required References

Read only as needed:

- `references/innovation_signals.md`: signal taxonomy and tests.
- `references/schemas.md`: required output fields.

Use the template:

- `assets/innovation_candidates.template.json`

## Output Files

```text
outputs/<research_project_id>/
├── innovation_candidates.json
└── innovation_report.md
```

## Search Rules

- Deliberately search adjacent fields, not only exact keyword neighbors.
- Include at least one route targeting assumptions and one route targeting proof techniques when possible.
- Keep speculative ideas, but label them as speculative.
- Do not download full text unless the user selected the paper or explicitly requested download.
- Do not bypass paywalls.

## Completion Check

Before finishing, confirm:

- `innovation_candidates.json` is valid JSON.
- Every candidate has an innovation signal, possible research angle, risk note, and recommended action.
- The report separates strong leads from speculative leads.
