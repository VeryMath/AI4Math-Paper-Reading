---
name: pdf-to-markdown-converter
description: Convert local PDF papers to Markdown using a self-contained MinerU workflow. Use when Codex is asked to turn a PDF into a .md file, prepare Markdown input for paper-to-skill extraction, configure MinerU PDF conversion, create or reuse the ai4math Conda environment, or run PDF-to-Markdown preprocessing. The skill installs dependencies into the named Conda environment ai4math, creates .env in the current working directory, prompts interactively for MINERU_API_TOKEN when missing, and writes Markdown output in the current folder by default.
---

# Pdf To Markdown Converter

## Overview

Use this skill to convert a local PDF into Markdown before paper-to-skill extraction. Keep this skill focused on preprocessing only: `PDF -> Markdown`.

## Workflow

1. Work from the directory where the user wants `.env` and Markdown output.
2. Run the bootstrap script with the target PDF:

```bash
python /Users/conanxu/paper-to-skill/skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py input.pdf
```

3. If `MINERU_API_TOKEN` is missing, let the script prompt for it interactively. Do not ask the user to paste API keys into chat unless they explicitly choose to.
4. By default, the script writes a complete conversion folder:

```text
./<input-pdf-stem>_converted/
├── paper.md
├── mineru/
└── conversion_report.json
```

5. For a custom output name:

```bash
python /Users/conanxu/paper-to-skill/skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py input.pdf --out paper.md
```

6. For a custom MinerU artifacts folder:

```bash
python /Users/conanxu/paper-to-skill/skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py input.pdf --out paper.md --artifacts-dir paper_mineru
```

7. For a batch of PDFs, pass one or more PDF files or directories with `--batch`:

```bash
python /Users/conanxu/paper-to-skill/skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py papers/ --batch
```

Batch output is grouped by PDF stem:

```text
./outputs_markdown/<input-pdf-stem>/
├── paper.md
├── mineru/
└── conversion_report.json
```

## What The Bootstrap Does

- Creates or reuses the named Conda environment `ai4math`.
- Installs bundled requirements into `ai4math`.
- Creates or updates `.env` in the current working directory.
- Preserves existing `.env` values and never overwrites an existing `MINERU_API_TOKEN`.
- Runs the bundled MinerU converter.
- Writes Markdown output in a grouped conversion folder by default.
- Extracts and saves the complete MinerU result ZIP as `mineru/` in the conversion folder.
- Writes `conversion_report.json` with input/output paths, converter metadata, Markdown character count, status, and smoke-check warnings.

## Resources

- `scripts/bootstrap_pdf_to_markdown.py`: stdlib-only setup and runner.
- `scripts/pdf_to_markdown.py`: MinerU PDF-to-Markdown converter.
- `scripts/requirements.txt`: runtime dependencies installed into Conda env `ai4math`.
- `references/usage.md`: detailed command and environment behavior.

## Completion Check

Before finishing a conversion task, confirm:

- Conda environment `ai4math` exists.
- `.env` exists and contains `MINERU_API_TOKEN` or the shell provided it.
- Markdown output file exists in the grouped conversion folder or the requested `--out` path.
- Markdown output is non-empty.
- MinerU artifacts folder exists and contains the extracted result files.
- `conversion_report.json` exists and records any smoke-check warnings.
