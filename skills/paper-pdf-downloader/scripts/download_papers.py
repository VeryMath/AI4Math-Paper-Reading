#!/usr/bin/env python3
"""Download selected open-access paper PDFs from paper-to-skill plans."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def candidates_from_file(path: Path) -> dict[str, dict]:
    data = load_json(path)
    out: dict[str, dict] = {}
    for paper in data.get("papers", []) + data.get("candidates", []):
        pid = paper.get("paper_id")
        if pid:
            out[pid] = paper
    return out


def load_pool(paths: list[Path]) -> dict[str, dict]:
    pool: dict[str, dict] = {}
    for path in paths:
        if path.exists():
            pool.update(candidates_from_file(path))
    return pool


def selected_ids(args: argparse.Namespace, plan: dict | None) -> list[str]:
    ids = list(args.paper_id or [])
    if args.from_download_queue:
        if not plan:
            raise SystemExit("--from-download-queue requires --plan")
        ids.extend(plan.get("download_queue", []))
    if args.limit is not None:
        ids = ids[: args.limit]
    seen: set[str] = set()
    deduped: list[str] = []
    for pid in ids:
        if pid not in seen:
            seen.add(pid)
            deduped.append(pid)
    return deduped


def metadata_for(paper: dict, status: str, warnings: list[str]) -> dict:
    return {
        "paper_id": paper.get("paper_id", ""),
        "title": paper.get("title", ""),
        "authors": paper.get("authors", []),
        "year": paper.get("year", ""),
        "venue": paper.get("venue", ""),
        "source_url": paper.get("url", ""),
        "pdf_url": paper.get("pdf_url", ""),
        "downloaded_at": utc_now(),
        "status": status,
        "paper_pdf": "paper.pdf",
        "source_quality": paper.get("source_quality", "primary"),
        "download_warnings": warnings,
        "next_step": "convert_to_markdown" if status in {"downloaded", "skipped_existing"} else "request_user_pdf",
    }


def write_metadata(paper_dir: Path, meta: dict) -> None:
    paper_dir.mkdir(parents=True, exist_ok=True)
    with (paper_dir / "metadata.json").open("w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
        f.write("\n")


def copy_local_pdf(src: Path, dest: Path, overwrite: bool) -> str:
    if dest.exists() and not overwrite:
        return "skipped_existing"
    shutil.copyfile(src, dest)
    return "downloaded"


def download_pdf(url: str, dest: Path, overwrite: bool, timeout: int) -> tuple[str, list[str]]:
    warnings: list[str] = []
    if dest.exists() and not overwrite:
        return "skipped_existing", warnings

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "paper-to-skill paper-pdf-downloader/0.1",
            "Accept": "application/pdf,*/*",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            content_type = resp.headers.get("Content-Type", "")
    except (urllib.error.URLError, TimeoutError) as exc:
        return "failed", [f"download error: {exc}"]

    if len(data) < 1024:
        return "failed", [f"response too small: {len(data)} bytes"]
    if not data.startswith(b"%PDF"):
        warnings.append(f"response does not start with PDF header; content-type={content_type!r}")
        if "pdf" not in content_type.lower():
            return "failed", warnings

    dest.write_bytes(data)
    return "downloaded", warnings


def render_report(project_dir: Path, selected: list[str], results: list[dict], dry_run: bool) -> None:
    lines = [
        "# Download Report / 下载报告",
        "",
        "中文：本报告记录 `paper-pdf-downloader` 对已确认论文 PDF 的处理结果。未尝试绕过 paywall。",
        "",
        "English: This report records `paper-pdf-downloader` results for confirmed paper PDFs. No paywall bypass was attempted.",
        "",
        f"- Selected / 已选择: {', '.join(selected) if selected else '(none)'}",
        f"- Dry run / 预演: {dry_run}",
        "",
        "## Results / 结果",
        "",
    ]
    for item in results:
        lines.extend(
            [
                f"### {item['paper_id']} - {item.get('title', '')}",
                "",
                f"- 中文：状态 `{item['status']}`；目录 `{item['paper_dir']}`。",
                f"- English: Status `{item['status']}`; folder `{item['paper_dir']}`.",
                f"- PDF URL: {item.get('pdf_url', '')}",
            ]
        )
        if item.get("warnings"):
            lines.append(f"- Warnings / 警告: {'; '.join(item['warnings'])}")
        lines.append("")

    lines.extend(
        [
            "## Next Step / 下一步",
            "",
            "中文：对成功下载的 `paper.pdf` 运行 `pdf-to-markdown-converter`，生成 `paper.md` 后再交给 `paper-to-skill-extractor`。",
            "",
            "English: Run `pdf-to-markdown-converter` on successful `paper.pdf` files, then pass generated `paper.md` files to `paper-to-skill-extractor`.",
            "",
        ]
    )
    (project_dir / "download_report.md").write_text("\n".join(lines), encoding="utf-8")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", required=True, type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--candidates", action="append", type=Path, default=[])
    parser.add_argument("--paper-id", action="append", default=[])
    parser.add_argument("--from-download-queue", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args(argv)

    project_dir = args.project_dir
    plan = load_json(args.plan) if args.plan else None
    pool_paths: list[Path] = []
    if args.plan:
        pool_paths.append(args.plan)
    pool_paths.extend(args.candidates)
    for default_name in ["candidate_papers.json", "innovation_candidates.json"]:
        default_path = project_dir / default_name
        if default_path not in pool_paths:
            pool_paths.append(default_path)
    pool = load_pool(pool_paths)
    ids = selected_ids(args, plan)
    if not ids:
        raise SystemExit("No paper IDs selected. Use --paper-id or --from-download-queue.")

    results: list[dict] = []
    for pid in ids:
        paper = pool.get(pid)
        if not paper:
            results.append({"paper_id": pid, "status": "failed", "paper_dir": "", "warnings": ["paper_id not found"]})
            continue

        paper_dir = project_dir / "papers" / pid
        paper_dir.mkdir(parents=True, exist_ok=True)
        pdf_dest = paper_dir / "paper.pdf"
        pdf_url = paper.get("pdf_url", "")
        warnings: list[str] = []
        status = "metadata_only"

        if args.dry_run:
            status = "metadata_only"
            warnings.append("dry run; no download attempted")
        elif not pdf_url:
            status = "failed"
            warnings.append("missing pdf_url")
        else:
            parsed = urllib.parse.urlparse(pdf_url)
            if parsed.scheme in {"", "file"}:
                local_path = Path(urllib.request.url2pathname(parsed.path if parsed.scheme == "file" else pdf_url))
                if local_path.exists():
                    status = copy_local_pdf(local_path, pdf_dest, args.overwrite)
                else:
                    status = "failed"
                    warnings.append(f"local PDF not found: {local_path}")
            elif parsed.scheme in {"http", "https"}:
                status, warnings = download_pdf(pdf_url, pdf_dest, args.overwrite, args.timeout)
                time.sleep(0.5)
            else:
                status = "failed"
                warnings.append(f"unsupported URL scheme: {parsed.scheme}")

        if status in {"downloaded", "skipped_existing"} and pdf_dest.exists():
            if pdf_dest.stat().st_size == 0:
                status = "failed"
                warnings.append("paper.pdf is empty")
            elif not pdf_dest.read_bytes()[:4] == b"%PDF":
                warnings.append("paper.pdf does not start with PDF header")

        meta = metadata_for(paper, status, warnings)
        write_metadata(paper_dir, meta)
        results.append(
            {
                "paper_id": pid,
                "title": paper.get("title", ""),
                "status": status,
                "paper_dir": str(paper_dir),
                "pdf_url": pdf_url,
                "warnings": warnings,
            }
        )

    render_report(project_dir, ids, results, args.dry_run)
    failed = [r for r in results if r["status"] == "failed"]
    print(json.dumps({"selected": ids, "results": results, "failed": len(failed)}, indent=2, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
