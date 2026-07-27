# After OCR

`after-ocr` reviews formula-heavy OCR Markdown, identifies likely mathematical
and layout errors, applies evidence-backed local corrections, and records an
auditable coverage log.

## Use

Open [`SKILL.md`](SKILL.md) and choose one delivery mode:

- revise and record;
- audit only; or
- audit a bounded line range.

The candidate scanner and multi-pass log merger are optional accelerators. They
do not replace continuous reading of the requested range.

```bash
python3 scripts/scan_markdown_ocr.py /absolute/path/to/input.md --format markdown
python3 scripts/merge_audit_logs.py pass-a.md pass-b.md --output merged.md
```

## Validation

```bash
python3 -m unittest discover -s tests -v
```

The package uses only the Python standard library.

## Contributor and License

Course contributor: **Dong Yuan**. Released under the repository's MIT
License. See [`PROVENANCE.yaml`](PROVENANCE.yaml) and
[`NORMALIZATION.md`](NORMALIZATION.md) for the course-edition record.
