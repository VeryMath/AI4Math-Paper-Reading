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
- `flow_stability_validation.md`: source-condition comparison, separate mathematical derivation, actual cross-problem reuse, and failed generalizations checked on 2026-10-22.
- `flow_stability_check.py`: direct standard-library computation of the exact ODE examples and bounds in that report.

Only the revised continuous-flow stability card currently has the complete verification and reuse record. Other cards have `promotion.status: candidate`; their extraction status follows the current score rubric. Earlier library-readiness labels are not evidence of mathematical verification.

## Excluded From GitHub

- MinerU `mineru/` folders.
- Local `.env` files and API tokens.

2026-10-22：六张旧单篇卡的 `total_score` 已按既有加权公式和原分项评分重新计算。这只是算术修正，没有新增数学复核，也没有改变验证状态或晋级结论。

后续一致性修正：候选索引同步单篇卡分数；3.9 分高斯平滑卡及报告调整为 `needs_review`。五张单来源合成卡保留来源抽取评分，并明确未重新评分；没有新增数学验证或晋级。
