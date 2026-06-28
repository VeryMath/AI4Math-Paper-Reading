# Auto Research Trial Example

This directory is a sanitized end-to-end example of the Codex-native paper-to-skill workflow.

It preserves the full PDF-to-Skill evidence chain while excluding local credentials and MinerU intermediate artifacts.

## Workflow Covered

```text
seed papers
  -> research_profile.json
  -> human_feedback_state.json
  -> candidate_papers.json + innovation_candidates.json
  -> reading_plan.json
  -> paper.pdf downloads
  -> paper.md conversion outputs
  -> single-paper proof_pattern SkillCards
  -> cross-paper synthesized SkillCards
```

## Key Files

- `workflow_report.md`: full step-by-step test-flow record.
- `seed_papers/*/paper.pdf`: original seed PDFs.
- `seed_papers/*/paper.md`: converted seed Markdown papers used for profiling.
- `research_profile.json`: seed-paper interest profile.
- `human_feedback_state.json`: human corrections and directives applied across later Skills.
- `candidate_papers.json`: related-paper candidates.
- `innovation_candidates.json`: innovation-oriented candidates.
- `reading_plan.json`: triage output and download queue.
- `papers/*/paper.pdf`: downloaded PDFs selected from the reading plan.
- `papers/*/paper.md`: converted Markdown papers used for extraction.
- `papers/*/skill_cards/`: single-paper extracted Skill Cards.
- `synthesized_skills/domain_method_map.yaml`: cross-paper method map.
- `synthesized_skills/merged_skill_cards/`: merged library-ready or review-worthy Skill Cards.
- `synthesized_skills/synthesis_report.md`: bilingual synthesis report.

## Excluded From GitHub

- MinerU `mineru/` folders.
- Local `.env` files and API tokens.
