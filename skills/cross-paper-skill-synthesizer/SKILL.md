---
name: cross-paper-skill-synthesizer
description: Cluster, deduplicate, generalize, and rank proof-pattern SkillCandidates or SkillCards extracted from multiple papers. Use when Codex should synthesize single-paper extractions into a domain method map, merged SkillCards, and a synthesis report for an AI4Math skill library.
---

# Cross Paper Skill Synthesizer

## Purpose

Use this skill after multiple papers have been processed by `paper-to-skill-extractor`. The goal is to build a domain method map and library-ready SkillCards, not to summarize papers.

## Inputs

Accept any mix of:

- `extractions/<paper_id>/skill_candidates.json`
- `extractions/<paper_id>/skill_cards/*.yaml`
- Paper metadata files.
- User notes about which skills should be merged or rejected.

## Workflow

1. Load all SkillCandidates and SkillCards.
2. Preserve source evidence from every paper. Do not drop line references.
3. Cluster candidates by proof pattern, intent, assumptions, inputs, outputs, and core steps.
4. Deduplicate near-identical skills while keeping all source references.
5. Generalize paper-specific notation into reusable method language.
6. Identify conflicts: incompatible assumptions, different conclusions, unsafe generalizations, or missing evidence.
7. Rank clusters for library readiness.
8. Write `domain_method_map.yaml`, merged SkillCards, and `synthesis_report.md`.

## Required References

Read only as needed:

- `references/synthesis_rules.md`: clustering, merging, and safety rules.
- `references/schemas.md`: required output fields.

Use the templates:

- `assets/domain_method_map.template.yaml`
- `assets/merged_skill_card.template.yaml`

## Output Files

```text
outputs/<research_project_id>/synthesized_skills/
├── domain_method_map.yaml
├── merged_skill_cards/
│   └── <skill_name>.yaml
└── synthesis_report.md
```

## Synthesis Rules

- Never remove source evidence when merging.
- Do not generalize beyond the shared assumptions unless marked `needs_human_review`.
- Separate `ready_for_library`, `needs_human_review`, `too_specific`, `duplicate`, and `unsafe_generalization`.
- Keep rejected or unsafe clusters in the report so future reviewers understand the decision.
- Prefer fewer, stronger SkillCards over many thin variants.

## Completion Check

Before finishing, confirm:

- Every merged SkillCard has source references to original `paper.md` files.
- `domain_method_map.yaml` records clusters, representative skills, and statuses.
- The report explains conflicts, risks, and human-review items.
