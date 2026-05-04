---
name: paper-triage-ranker
description: Rank candidate research papers into must_read, should_read, maybe_read, and skip groups for a paper-to-skill workflow. Use when Codex should combine related-paper and innovation candidates, judge relevance, novelty, proof-pattern value, reading cost, access status, and produce a reading_plan.json with user confirmation checkpoints.
---

# Paper Triage Ranker

## Purpose

Use this skill to turn candidate paper lists into a reading plan. The output should tell the user what to read first and why, especially for downstream proof-pattern extraction.

## Inputs

- `candidate_papers.json`
- `innovation_candidates.json`
- Optional `research_profile.json`
- Optional user constraints such as time budget or target research question.

## Workflow

1. Load all candidate lists and merge duplicate papers by title, URL, DOI, or arXiv ID.
2. Score each paper for relevance, innovation potential, proof-pattern value, positioning value, reading cost, and access status.
3. Assign each paper to `must_read`, `should_read`, `maybe_read`, or `skip`.
4. For `must_read` and `should_read`, specify what to inspect: abstract, intro, theorem statements, proofs, experiments, related work, or appendices.
5. Mark whether download and Markdown conversion are recommended.
6. Write `reading_plan.json` using `references/schemas.md`.
7. Write `triage_report.md` with a concise reading sequence and checkpoint questions.

## Required References

Read only as needed:

- `references/ranking_rubric.md`: scoring and group assignment guidance.
- `references/schemas.md`: required output fields.

Use the template:

- `assets/reading_plan.template.json`

## Output Files

```text
outputs/<research_project_id>/
├── reading_plan.json
└── triage_report.md
```

## Triage Rules

- Prefer papers that may produce reusable proof-pattern SkillCards.
- Do not let recency dominate if an older paper contains the core theorem or proof method.
- Down-rank papers that are only benchmark or generic background unless positioning requires them.
- Separate reading priority from download status.
- Ask for user confirmation before downloading, converting, or extracting from multiple papers.

## Completion Check

Before finishing, confirm:

- `reading_plan.json` is valid JSON.
- Every candidate is assigned to exactly one group.
- `must_read` and `should_read` entries include reading focus and extraction recommendation.
- The report includes the user checkpoint for final paper selection.
