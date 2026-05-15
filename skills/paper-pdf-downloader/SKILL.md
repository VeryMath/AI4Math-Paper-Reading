---
name: paper-pdf-downloader
description: Download open-access research-paper PDFs selected from reading_plan.json, candidate_papers.json, or innovation_candidates.json. Use when a coding agent should save paper.pdf, metadata.json, and a bilingual download report for confirmed paper IDs without bypassing paywalls, and before PDF-to-Markdown conversion or paper-to-skill extraction.
---

# Paper PDF Downloader

## Purpose

Use this skill to download selected open-access paper PDFs after triage. Keep this skill narrow: `metadata + open PDF URL -> metadata.json + paper.pdf + download_report.md`.

Do not convert PDFs to Markdown here. Use `pdf-to-markdown-converter` after download.

## Inputs

Accept one or more of:

- `outputs/<research_project_id>/reading_plan.json`
- `outputs/<research_project_id>/candidate_papers.json`
- `outputs/<research_project_id>/innovation_candidates.json`
- Optional `outputs/<research_project_id>/human_feedback_state.json`
- Explicit paper IDs supplied by the user.

Default to papers in `download_queue` from `reading_plan.json` only when the user asks to download from the plan. If the user names paper IDs, download only those IDs.

## Workflow

1. Read the input plan or candidate files.
2. If `human_feedback_state.json` exists, read `paper_decisions` and `next_step_directives` before selecting downloads.
3. Resolve each requested paper ID to metadata and `pdf_url`.
4. Confirm each selected paper has an open PDF URL or user-provided local PDF.
5. Do not bypass paywalls, scrape institutional access, or use unofficial mirrors.
6. Download each open PDF into `outputs/<research_project_id>/papers/<paper_id>/paper.pdf`.
7. Write `metadata.json` beside each PDF using `references/schemas.md`.
8. Write a bilingual `download_report.md` in `outputs/<research_project_id>/`.
9. Leave Markdown conversion to `pdf-to-markdown-converter`.

## Scripted Download

Prefer the bundled script for repeatable downloads:

```bash
python skills/paper-pdf-downloader/scripts/download_papers.py \
  --project-dir outputs/<research_project_id> \
  --plan outputs/<research_project_id>/reading_plan.json \
  --paper-id <paper_id> \
  --paper-id <paper_id>
```

To download the first `N` IDs from `download_queue`:

```bash
python skills/paper-pdf-downloader/scripts/download_papers.py \
  --project-dir outputs/<research_project_id> \
  --plan outputs/<research_project_id>/reading_plan.json \
  --from-download-queue \
  --limit N
```

Use `--dry-run` to inspect selected papers without downloading.

## Required References

Read only as needed:

- `references/schemas.md`: metadata and report shape.
- `references/download_policy.md`: open-access and paywall rules.

Use the template:

- `assets/metadata.template.json`

## Output Files

```text
outputs/<research_project_id>/
├── papers/
│   └── <paper_id>/
│       ├── metadata.json
│       └── paper.pdf
└── download_report.md
```

## Download Rules

- Only download when `pdf_url` is openly accessible or the user supplied a local PDF.
- Record `source_url`, `pdf_url`, `downloaded_at`, `status`, and any warnings.
- If the URL does not return PDF bytes, mark the paper as `failed` and explain why.
- Preserve existing `paper.pdf` unless the user explicitly asks to overwrite; use the script's default skip behavior.
- Do not download every candidate by default. Download only confirmed paper IDs or the confirmed `download_queue`.
- Do not download papers marked `skip` or `do_not_download` in `human_feedback_state.json` unless the user explicitly overrides that decision.
- Papers marked `download` or `must_read` by the user may be selected when they also have an open PDF URL or user-provided local PDF.

## Completion Check

Before finishing, confirm:

- Each requested paper has a `metadata.json`.
- Each successful download has a non-empty `paper.pdf` with a PDF header.
- `download_report.md` is bilingual Chinese-English.
- Failed or skipped papers are recorded explicitly.
