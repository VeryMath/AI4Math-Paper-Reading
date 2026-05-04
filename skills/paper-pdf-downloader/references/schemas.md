# Paper PDF Downloader Schemas

## `metadata.json`

```json
{
  "paper_id": "string",
  "title": "string",
  "authors": ["string"],
  "year": "string",
  "venue": "string",
  "source_url": "string",
  "pdf_url": "string",
  "downloaded_at": "YYYY-MM-DDTHH:MM:SSZ",
  "status": "downloaded | skipped_existing | failed | metadata_only",
  "paper_pdf": "paper.pdf",
  "source_quality": "primary | author_copy | metadata_only | secondary",
  "download_warnings": ["string"],
  "next_step": "convert_to_markdown | inspect_metadata | request_user_pdf"
}
```

## `download_report.md`

Write the report in Chinese and English. Include:

- selected source file and selection rule;
- downloaded papers;
- skipped existing papers;
- failed papers and reasons;
- next command for `pdf-to-markdown-converter`.
