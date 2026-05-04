---
name: seed-paper-profiler
description: Build a research-interest profile from a small set of seed math papers, abstracts, or user notes. Use when Codex should infer the user's target domain, core problems, methods, assumptions, proof patterns, technical keywords, negative preferences, and search directions before related-paper retrieval or paper-to-skill extraction.
---

# Seed Paper Profiler

## Purpose

Use this skill to turn a few seed papers into a research-interest profile. Do not summarize the papers as the final product. Extract a profile that can drive retrieval, triage, and later proof-pattern skill mining.

## Inputs

Accept any mix of:

- Markdown papers such as `paper.md`.
- Abstracts, introductions, theorem statements, or user notes.
- Existing extraction reports or SkillCards from seed papers.

When a full `paper.md` is available, preserve source line references for claims used in the profile.

## Workflow

1. Create or reuse `outputs/<research_project_id>/`.
2. Preserve seed inputs under `seed_papers/` when writing artifacts.
3. Read each seed paper for problem setting, mathematical objects, assumptions, methods, proof patterns, evaluation criteria, and open questions.
4. Separate stable interests from one-paper accidents. Mark uncertain inferences as hypotheses.
5. Extract positive interests and negative preferences. Negative preferences include topics the user likely does not want to pursue.
6. Generate search directions covering problem, method, theorem, assumption, application, and adjacent-domain routes.
7. Write `research_profile.json` using the schema in `references/schemas.md`.
8. Write `profile_review.md` with a short checkpoint asking the user to confirm, remove, or emphasize directions.

## Language Policy

For this project, default to bilingual Chinese-English output for user-facing content.

- Write `profile_review.md` in Chinese and English. Use paired sections or paired bullets with `中文:` and `English:`.
- When replying to the user after running the skill, summarize results in Chinese and English.
- Keep JSON keys and enum values in English for machine readability.
- For JSON natural-language fields, English is acceptable, but include `checkpoint_questions_bilingual` when asking the user to confirm the profile.
- Do not translate mathematical terms mechanically when a standard English term is clearer; pair it with a concise Chinese explanation when useful.

## Required References

Read only as needed:

- `references/schemas.md`: required output fields.

Use the template:

- `assets/research_profile.template.json`

## Output Files

```text
outputs/<research_project_id>/
├── seed_papers/
├── research_profile.json
└── profile_review.md
```

## Profiling Rules

- Prefer reusable research intent over paper-specific details.
- Track evidence for important claims when source lines are available.
- Keep `user_interest_hypotheses` explicit; do not present guesses as facts.
- Generate queries that can be used by Codex search or browsing tools.
- Include `checkpoint_questions` that help the user correct the direction before retrieval begins.

## Completion Check

Before finishing, confirm:

- `research_profile.json` is valid JSON.
- It includes domain, core problems, methods, assumptions, proof patterns, keywords, search queries, checkpoint questions, and bilingual checkpoint questions.
- `profile_review.md` is bilingual Chinese-English.
- Every high-confidence profile item has either source evidence or a clear note that it came from user-provided context.
