# Download Policy

## Allowed

- Open-access PDFs from arXiv, OpenReview, conference pages, author pages, institutional repositories, or publisher open-access pages.
- User-provided local PDFs.
- Metadata-only records for papers without an open PDF.

## Not Allowed

- Bypassing paywalls.
- Using institutional access automatically.
- Scraping private repositories, shadow libraries, or unofficial mirrors.
- Downloading a PDF when the source URL is ambiguous or not clearly tied to the paper.

## Behavior

- Prefer primary sources.
- Keep `pdf_url` and `source_url` in `metadata.json`.
- Preserve `paper.pdf` exactly as downloaded.
- Do not silently replace existing PDFs.
- If download fails, keep `metadata.json` and record `status: failed`.
