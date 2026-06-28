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
    merged_skill_card: merged_skill_cards/<skill_name>.yaml
review_queue:
  - cluster_id: string
    reason: string
```

## Merged SkillCard additions

Merged SkillCards should preserve the existing `paper-to-skill-extractor` SkillCard shape and add:

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
```
