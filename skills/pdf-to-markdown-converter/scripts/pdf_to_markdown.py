"""Standalone MinerU PDF to Markdown converter.

This module is extracted from the earlier PaperDive implementation but does not
depend on Agno, databases, or the Assistant project layout.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import sys
import time
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import httpx


@dataclass(frozen=True)
class ConversionPaths:
    output_dir: Path
    markdown_path: Path
    artifacts_dir: Path
    report_path: Path


def _find_dotenv(start: Path | None = None) -> Path | None:
    current = (start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for directory in (current, *current.parents):
        candidate = directory / ".env"
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def _parse_dotenv_value(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value


def load_dotenv_file(path: str | Path | None = None) -> Path | None:
    """Load .env values into os.environ without overriding existing values."""
    dotenv_path = Path(path).expanduser().resolve() if path is not None else _find_dotenv()
    if dotenv_path is None or not dotenv_path.exists():
        return None

    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip()
        if not key or key in os.environ:
            continue
        os.environ[key] = _parse_dotenv_value(raw_value)
    return dotenv_path


def _block_to_text(block: dict[str, Any]) -> str:
    block_type = block.get("type")
    parts: list[str] = []

    def add(value: Any) -> None:
        if value is None:
            return
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str) and item.strip():
                    parts.append(item.strip())

    if block_type in {"text", "equation", "header", "footer", "page_number", "aside_text", "page_footnote"}:
        add(block.get("text"))
    elif block_type == "table":
        add(block.get("table_caption"))
        add(block.get("table_body"))
        add(block.get("table_footnote"))
    elif block_type == "image":
        add(block.get("image_caption"))
        add(block.get("image_footnote"))
    elif block_type == "code":
        add(block.get("code_caption"))
        add(block.get("code_body"))
    elif block_type == "list":
        add(block.get("list_items"))
        add(block.get("text"))
    else:
        add(block.get("text"))

    return "\n".join(parts).strip()


def _pick_markdown_member(names: list[str]) -> Optional[str]:
    for name in names:
        if name == "full.md" or name.endswith("/full.md"):
            return name
    return None


def _pick_content_list_member(names: list[str]) -> Optional[str]:
    primary = [
        name
        for name in names
        if name.endswith("_content_list.json") and not name.endswith("_content_list_v2.json")
    ]
    if primary:
        return min(primary, key=len)
    fallback = [
        name
        for name in names
        if name.endswith("content_list.json") and "v2" not in name.lower()
    ]
    if fallback:
        return min(fallback, key=len)
    return None


def _content_list_to_markdown(blocks: list[dict[str, Any]], total_pages: int) -> str:
    if total_pages <= 0:
        return ""

    buckets: list[list[str]] = [[] for _ in range(total_pages)]
    last_page = total_pages - 1
    for block in blocks:
        if not isinstance(block, dict):
            continue
        try:
            page_idx = int(block.get("page_idx", 0))
        except (TypeError, ValueError):
            page_idx = 0
        page_idx = max(0, min(last_page, page_idx))
        text = _block_to_text(block)
        if text:
            buckets[page_idx].append(text)

    pages: list[str] = []
    for idx, chunks in enumerate(buckets, start=1):
        page_text = "\n\n".join(chunks).strip()
        if page_text:
            pages.append(f"---Page {idx}---\n\n{page_text}")
    return "\n\n".join(pages)


def parse_mineru_zip_to_markdown(zip_bytes: bytes, total_pages: int) -> str:
    """Parse a MinerU result ZIP into Markdown, preferring full.md."""
    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
        names = zf.namelist()
        markdown_member = _pick_markdown_member(names)
        if markdown_member:
            return zf.read(markdown_member).decode("utf-8")

        content_member = _pick_content_list_member(names)
        if not content_member:
            return ""
        raw = zf.read(content_member)

    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        return ""
    return _content_list_to_markdown(data, total_pages)


def default_artifacts_dir(pdf_path: str | Path, output_path: str | Path) -> Path:
    """Default directory for the full MinerU result folder."""
    output = Path(output_path).expanduser()
    return output.parent / "mineru"


def default_conversion_dir(pdf_path: str | Path, cwd: str | Path) -> Path:
    pdf = Path(pdf_path).expanduser()
    return Path(cwd).expanduser() / f"{pdf.stem}_converted"


def build_conversion_paths(pdf_path: str | Path, cwd: str | Path) -> ConversionPaths:
    output_dir = default_conversion_dir(pdf_path, cwd)
    return ConversionPaths(
        output_dir=output_dir,
        markdown_path=output_dir / "paper.md",
        artifacts_dir=output_dir / "mineru",
        report_path=output_dir / "conversion_report.json",
    )


def extract_mineru_zip(zip_bytes: bytes, output_dir: str | Path) -> Path:
    """Extract the full MinerU result ZIP into output_dir.

    Rejects path traversal entries instead of trusting ZIP member names.
    """
    target_dir = Path(output_dir).expanduser().resolve()
    target_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(io.BytesIO(zip_bytes), "r") as zf:
        for member in zf.infolist():
            member_name = member.filename
            if not member_name or member_name.endswith("/"):
                continue
            destination = (target_dir / member_name).resolve()
            if target_dir != destination and target_dir not in destination.parents:
                raise ValueError(f"Unsafe ZIP member path: {member_name}")
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(zf.read(member))

    return target_dir


def _contains_mineru_source_file(artifacts_dir: Path) -> bool:
    if not artifacts_dir.exists():
        return False
    for path in artifacts_dir.rglob("*"):
        if not path.is_file():
            continue
        name = path.name
        if name == "full.md" or name.endswith("content_list.json"):
            return True
    return False


def smoke_check_conversion(
    markdown_text: str,
    artifacts_dir: str | Path,
    *,
    min_markdown_chars: int = 500,
) -> list[str]:
    warnings: list[str] = []
    artifacts = Path(artifacts_dir)
    if not markdown_text.strip():
        warnings.append("markdown_empty")
    elif len(markdown_text.strip()) < min_markdown_chars:
        warnings.append(f"markdown_chars_below_{min_markdown_chars}")
    if not artifacts.exists():
        warnings.append("mineru_artifacts_missing")
    elif not _contains_mineru_source_file(artifacts):
        warnings.append("mineru_full_md_or_content_list_missing")
    return warnings


def write_conversion_report(
    report_path: str | Path,
    *,
    input_pdf: str | Path,
    output_md: str | Path,
    artifacts_dir: str | Path,
    markdown_text: str,
    warnings: list[str],
    converter: str = "MinerU",
    conda_env: str = "ai4math",
) -> Path:
    report = {
        "input_pdf": str(input_pdf),
        "output_md": str(output_md),
        "artifacts_dir": str(artifacts_dir),
        "converter": converter,
        "conda_env": conda_env,
        "markdown_chars": len(markdown_text),
        "status": "success",
        "warnings": warnings,
    }
    path = Path(report_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def run_mineru_extract_file(
    pdf_path: Path,
    *,
    token: str,
    base_url: str = "https://mineru.net",
    model_version: str = "vlm",
    language: str = "ch",
    is_ocr: bool = True,
    enable_formula: bool = True,
    enable_table: bool = True,
    poll_interval_sec: float = 4.0,
    poll_timeout_sec: float = 1800.0,
    upload_timeout_sec: float = 600.0,
) -> bytes:
    """Upload a PDF to MinerU and return the result ZIP bytes."""
    base = base_url.rstrip("/")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }
    file_name = pdf_path.name
    body: dict[str, Any] = {
        "files": [
            {
                "name": file_name,
                "data_id": pdf_path.stem[:120],
                "is_ocr": is_ocr,
            }
        ],
        "model_version": model_version,
        "language": language,
        "enable_formula": enable_formula,
        "enable_table": enable_table,
    }

    batch_id = ""
    timeout = httpx.Timeout(poll_timeout_sec + 60.0, connect=30.0)
    with httpx.Client(timeout=timeout) as client:
        response = client.post(f"{base}/api/v4/file-urls/batch", headers=headers, json=body)
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") != 0:
            raise RuntimeError(f"MinerU upload URL request failed: {payload}")

        data = payload.get("data") or {}
        batch_id = str(data.get("batch_id", ""))
        upload_urls = data.get("file_urls") or []
        if not batch_id or not upload_urls:
            raise RuntimeError("MinerU did not return batch_id and upload URL")

        upload_response = httpx.put(
            upload_urls[0],
            content=pdf_path.read_bytes(),
            timeout=httpx.Timeout(upload_timeout_sec, connect=60.0),
        )
        if upload_response.status_code != 200:
            raise RuntimeError(
                f"MinerU upload failed HTTP {upload_response.status_code}: {upload_response.text[:300]}"
            )

        deadline = time.monotonic() + poll_timeout_sec
        while time.monotonic() < deadline:
            result_response = client.get(
                f"{base}/api/v4/extract-results/batch/{batch_id}",
                headers=headers,
            )
            result_response.raise_for_status()
            result_payload = result_response.json()
            if result_payload.get("code") != 0:
                raise RuntimeError(f"MinerU result query failed: {result_payload}")

            result_data = result_payload.get("data") or {}
            raw_results = result_data.get("extract_result")
            if isinstance(raw_results, dict):
                results = [raw_results]
            elif isinstance(raw_results, list):
                results = raw_results
            else:
                results = []

            chosen = next((item for item in results if item.get("file_name") == file_name), None)
            if chosen is None and results:
                chosen = results[0]
            if chosen is None:
                time.sleep(poll_interval_sec)
                continue

            state = chosen.get("state", "")
            if state == "done":
                zip_url = chosen.get("full_zip_url")
                if not zip_url:
                    raise RuntimeError("MinerU completed but did not return full_zip_url")
                for attempt in range(3):
                    try:
                        zip_response = httpx.get(
                            zip_url,
                            timeout=httpx.Timeout(600.0, connect=60.0),
                            follow_redirects=True,
                        )
                        zip_response.raise_for_status()
                        return zip_response.content
                    except (httpx.ConnectError, httpx.ProxyError) as exc:
                        if attempt < 2:
                            time.sleep(2**attempt)
                            continue
                        raise RuntimeError(f"MinerU result download failed after retries: {exc}") from exc
            if state == "failed":
                raise RuntimeError(f"MinerU parsing failed: {chosen.get('err_msg', 'unknown')}")

            time.sleep(poll_interval_sec)

    raise TimeoutError(f"MinerU parsing timed out after {poll_timeout_sec}s, batch_id={batch_id}")


def _pdf_page_count(pdf_path: Path) -> int:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is required. Install with: pip install pymupdf") from exc

    doc = fitz.open(pdf_path)
    try:
        return len(doc)
    finally:
        doc.close()


def get_markdown_from_pdf(
    pdf_path: str | Path,
    *,
    token: str,
    base_url: str = "https://mineru.net",
    model_version: str = "vlm",
    language: str = "ch",
    is_ocr: bool = True,
    enable_formula: bool = True,
    enable_table: bool = True,
    poll_interval_sec: float = 4.0,
    poll_timeout_sec: float = 1800.0,
    upload_timeout_sec: float = 600.0,
    artifacts_dir: str | Path | None = None,
) -> str:
    """Convert a local PDF to Markdown through MinerU."""
    path = Path(pdf_path).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"PDF file does not exist: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"PDF path is not a file: {path}")

    total_pages = _pdf_page_count(path)
    if total_pages == 0:
        return ""

    zip_bytes = run_mineru_extract_file(
        path,
        token=token,
        base_url=base_url,
        model_version=model_version,
        language=language,
        is_ocr=is_ocr,
        enable_formula=enable_formula,
        enable_table=enable_table,
        poll_interval_sec=poll_interval_sec,
        poll_timeout_sec=poll_timeout_sec,
        upload_timeout_sec=upload_timeout_sec,
    )
    if artifacts_dir is not None:
        extract_mineru_zip(zip_bytes, artifacts_dir)
    return parse_mineru_zip_to_markdown(zip_bytes, total_pages)


def _env_flag(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def main(argv: list[str] | None = None) -> int:
    load_dotenv_file()

    parser = argparse.ArgumentParser(description="Convert a PDF to Markdown through MinerU.")
    parser.add_argument("pdf", help="Input PDF path")
    parser.add_argument(
        "--out",
        help="Output Markdown path. Defaults to ./<pdf-stem>_converted/paper.md.",
    )
    parser.add_argument(
        "--artifacts-dir",
        help="Directory to save the full MinerU result folder. Defaults to ./<pdf-stem>_converted/mineru.",
    )
    parser.add_argument(
        "--report",
        help="Path for conversion_report.json. Defaults to ./<pdf-stem>_converted/conversion_report.json.",
    )
    parser.add_argument("--token", default=os.getenv("MINERU_API_TOKEN", ""), help="MinerU API token")
    parser.add_argument("--base-url", default=os.getenv("MINERU_BASE_URL", "https://mineru.net"))
    parser.add_argument("--model-version", default=os.getenv("MINERU_MODEL_VERSION", "vlm"))
    parser.add_argument("--language", default=os.getenv("MINERU_LANGUAGE", "ch"))
    parser.add_argument("--no-ocr", action="store_true", help="Disable OCR mode")
    parser.add_argument("--disable-formula", action="store_true", help="Disable formula extraction")
    parser.add_argument("--disable-table", action="store_true", help="Disable table extraction")
    args = parser.parse_args(argv)

    token = args.token.strip()
    if not token:
        parser.error("MinerU token is required. Set MINERU_API_TOKEN or pass --token.")

    pdf_path = Path(args.pdf).expanduser().resolve()
    default_paths = build_conversion_paths(pdf_path, Path.cwd())
    out_path = Path(args.out).expanduser().resolve() if args.out else default_paths.markdown_path
    artifacts_dir = (
        Path(args.artifacts_dir).expanduser().resolve()
        if args.artifacts_dir
        else default_paths.artifacts_dir
    )
    report_path = (
        Path(args.report).expanduser().resolve()
        if args.report
        else default_paths.report_path
    )

    markdown = get_markdown_from_pdf(
        args.pdf,
        token=token,
        base_url=args.base_url,
        model_version=args.model_version,
        language=args.language,
        is_ocr=(not args.no_ocr) and _env_flag("MINERU_IS_OCR", True),
        enable_formula=(not args.disable_formula) and _env_flag("MINERU_ENABLE_FORMULA", True),
        enable_table=(not args.disable_table) and _env_flag("MINERU_ENABLE_TABLE", True),
        artifacts_dir=artifacts_dir,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")
    warnings = smoke_check_conversion(markdown, artifacts_dir)
    write_conversion_report(
        report_path,
        input_pdf=pdf_path,
        output_md=out_path,
        artifacts_dir=artifacts_dir,
        markdown_text=markdown,
        warnings=warnings,
    )
    for warning in warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
