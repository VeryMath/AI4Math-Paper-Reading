# Cross Paper Skill Synthesizer Schemas

## `domain_method_map.yaml`

```yaml
research_project_id: string
created_at: YYYY-MM-DD
source_extractions:
  - paper_id: string
    path: string
clusters:
  - cluster_id: string
    name: string
    proof_pattern_family: string
    representative_skill: string
    status: ready_for_library | needs_human_review | too_specific | duplicate | unsafe_generalization
    source_skill_ids:
      - string
    shared_assumptions:
      - string
    transferable_core:
      - string
    conflicts_or_risks:
      - string
    verification_status: not_run | passed | failed | inconclusive
    reuse_status: not_run | checked_examples | failed | inconclusive
    promotion_status: candidate | ready_for_library | needs_human_review | rejected
    merged_skill_card: merged_skill_cards/<skill_name>.yaml
review_queue:
  - cluster_id: string
    reason: string
```

## Merged SkillCard additions

Merged SkillCards use the complete `paper-to-skill-extractor` SkillCard fields, including dependencies, independent verification, failure cases, reuse evidence, and promotion. Use `description`, `input`, and `output`; do not introduce parallel `summary`, `inputs`, or `outputs` fields. Add:

```yaml
synthesis:
  cluster_id: string
  source_skill_ids:
    - string
  source_papers:
    - paper_id: string
      paper_md: string
      start_line: 0
      end_line: 0
  merge_status: ready_for_library | needs_human_review
  generalization_notes:
    - string
  conflicts_or_risks:
    - string
  conflict_resolutions:
    - issue: string
      source_conditions: [string]
      decision: string
      evidence: string
      status: resolved | unresolved
```

`synthesis.merge_status` and the method map's readiness must agree with `promotion.status`. Only `ready_for_library` maps to ready; all pending or unresolved cases map to `needs_human_review`. Keep `status` for extraction quality. Use real positive line ranges from a representative source in `source`, and preserve all source ranges in `synthesis.source_papers`; `0` and `see synthesis` are not usable line references.
