---
name: related-paper-retriever
description: Retrieve and structure related math research papers from a research profile using Codex's available search or browsing capability. Use when Codex should find same-problem, same-method, direct-extension, theoretical-background, or benchmark papers, record metadata and relevance reasons, and avoid building a custom retriever or crawler.
---

# Related Paper Retriever

## Purpose

Use this skill to find related papers for a research profile. The skill does not implement a search engine. It instructs Codex how to search, judge relevance, and write structured candidate-paper artifacts.

## Inputs

- `outputs/<research_project_id>/research_profile.json`
- Optional `outputs/<research_project_id>/human_feedback_state.json`
- Optional seed paper metadata, user notes, or existing candidate lists.

## Workflow

1. Read `research_profile.json`.
2. If `human_feedback_state.json` exists, read it before generating queries. Apply `focus_updates`, `negative_preferences`, `paper_decisions`, and `next_step_directives`.
3. Generate or refine search queries across problem, method, theorem, assumption, application, author, and citation routes.
4. Use Codex's available search or browsing capability when retrieval is needed.
5. Prefer primary paper pages, arXiv, OpenReview, conference pages, author pages, and official PDFs.
6. For each candidate, record metadata, URL, PDF URL if openly available, relation type, relevance reason, and reading priority hint.
7. Do not download by default. Mark whether an open PDF was found or whether user-provided PDF access is needed.
8. Write `candidate_papers.json` using `references/schemas.md`.
9. Write `retrieval_report.md` summarizing query routes, coverage gaps, applied human feedback, and checkpoint questions.

## Required References

Read only as needed:

- `references/search_strategy.md`: query routes and relevance tests.
- `references/schemas.md`: required output fields.

Use the template:

- `assets/candidate_papers.template.json`

## Output Files

```text
outputs/<research_project_id>/
├── candidate_papers.json
└── retrieval_report.md
```

## Retrieval Rules

- Search for papers, not blog posts, unless the blog post points to a paper.
- Prioritize primary sources over secondary summaries.
- Treat search results as candidates until triage.
- Record why each paper is related; do not rely only on keyword overlap.
- Up-rank papers matching human `focus_updates` and down-rank papers matching `negative_preferences`.
- Do not re-suggest papers that the user marked `skip` or `do_not_download` unless there is a new reason and the report says so.
- Do not bypass paywalls.
- Download full text only if the user has selected the paper or explicitly requested download, the PDF is openly accessible or user-provided, and the source URL can be recorded.

## Completion Check

Before finishing, confirm:

- `candidate_papers.json` is valid JSON.
- Each candidate has title, year, URL or source note, relation type, relevance reason, and priority hint.
- Download status is explicit for every candidate.
- The report includes unresolved coverage gaps and a user checkpoint.
