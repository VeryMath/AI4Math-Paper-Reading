# PDF to Markdown Converter Usage

This skill is self-contained. It uses bundled scripts instead of the project-level component.

## Command

Run from the directory where the user wants `.env` and the Markdown output:

```bash
python skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py input.pdf
```

Default output:

```text
./<input-pdf-stem>_converted/
├── paper.md
├── mineru/
└── conversion_report.json
```

Explicit output:

```bash
python skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py input.pdf --out paper.md
```

Explicit artifacts folder:

```bash
python skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py input.pdf --out paper.md --artifacts-dir paper_mineru
```

Explicit report path:

```bash
python skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py input.pdf --out paper.md --artifacts-dir paper_mineru --report conversion_report.json
```

Batch conversion:

```bash
python skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py papers/ --batch
```

Batch output:

```text
./outputs_markdown/<input-pdf-stem>/
├── paper.md
├── mineru/
└── conversion_report.json
```

## Behavior

The bootstrap script:

1. Creates or reuses the named Conda environment `ai4math`.
2. Installs `scripts/requirements.txt` into `ai4math`.
3. Checks current `.env` or shell environment for `MINERU_API_TOKEN`.
4. If no token exists, prompts interactively for the MinerU API key.
5. Writes `.env` in the current working directory without overwriting existing values.
6. Runs the bundled `pdf_to_markdown.py`.
7. Writes Markdown to `./<input-pdf-stem>_converted/paper.md` by default.
8. Extracts the complete MinerU result ZIP into `./<input-pdf-stem>_converted/mineru/` by default.
9. Writes `conversion_report.json` with output paths, Markdown character count, status, and smoke-check warnings.

## Environment

Python packages are installed into:

```text
conda env: ai4math
```

Required:

```text
MINERU_API_TOKEN
```

Defaults written when absent:

```text
MINERU_BASE_URL=https://mineru.net
MINERU_MODEL_VERSION=vlm
MINERU_LANGUAGE=ch
MINERU_IS_OCR=1
MINERU_ENABLE_FORMULA=1
MINERU_ENABLE_TABLE=1
```

## Non-Interactive Mode

Use `--non-interactive` in automation. It fails if no token is configured.

## Smoke-Check Warnings

The converter does not reject weak OCR automatically. It records warnings in `conversion_report.json` and prints them to stderr. Current warnings include empty Markdown, Markdown below 500 characters, missing MinerU artifacts, or missing `full.md` / `content_list.json` in the extracted MinerU folder.
