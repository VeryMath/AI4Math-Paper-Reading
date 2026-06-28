import io
import importlib.util
import json
import os
import sys
import zipfile
from pathlib import Path

import pytest


def _load_converter_module():
    path = Path("skills/pdf-to-markdown-converter/scripts/pdf_to_markdown.py")
    spec = importlib.util.spec_from_file_location("pdf_to_markdown_converter", path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_converter = _load_converter_module()

build_conversion_paths = _converter.build_conversion_paths
default_artifacts_dir = _converter.default_artifacts_dir
default_conversion_dir = _converter.default_conversion_dir
extract_mineru_zip = _converter.extract_mineru_zip
get_markdown_from_pdf = _converter.get_markdown_from_pdf
load_dotenv_file = _converter.load_dotenv_file
parse_mineru_zip_to_markdown = _converter.parse_mineru_zip_to_markdown
smoke_check_conversion = _converter.smoke_check_conversion
write_conversion_report = _converter.write_conversion_report


def _zip_bytes(entries: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, content in entries.items():
            zf.writestr(name, content)
    return buf.getvalue()


def test_parse_mineru_zip_prefers_full_markdown() -> None:
    zip_data = _zip_bytes(
        {
            "paper/full.md": b"# Title\n\nFull markdown with $x^2$.",
            "paper_content_list.json": json.dumps(
                [{"type": "text", "page_idx": 0, "text": "fallback"}]
            ).encode("utf-8"),
        }
    )

    assert parse_mineru_zip_to_markdown(zip_data, total_pages=1) == "# Title\n\nFull markdown with $x^2$."


def test_parse_mineru_zip_falls_back_to_content_list_with_page_markers() -> None:
    zip_data = _zip_bytes(
        {
            "paper_content_list.json": json.dumps(
                [
                    {"type": "text", "page_idx": 0, "text": "Page one text"},
                    {"type": "equation", "page_idx": 0, "text": "$a=b$"},
                    {"type": "text", "page_idx": 1, "text": "Page two text"},
                ]
            ).encode("utf-8")
        }
    )

    assert parse_mineru_zip_to_markdown(zip_data, total_pages=2) == (
        "---Page 1---\n\nPage one text\n\n$a=b$\n\n"
        "---Page 2---\n\nPage two text"
    )


def test_default_artifacts_dir_uses_grouped_output_directory(tmp_path: Path) -> None:
    pdf = tmp_path / "papers" / "my-paper.pdf"
    output = tmp_path / "my-paper_converted" / "paper.md"

    assert default_artifacts_dir(pdf, output) == tmp_path / "my-paper_converted" / "mineru"


def test_default_conversion_dir_uses_pdf_stem(tmp_path: Path) -> None:
    pdf = tmp_path / "papers" / "paper.pdf"

    assert default_conversion_dir(pdf, tmp_path) == tmp_path / "paper_converted"


def test_build_conversion_paths_for_single_pdf_default(tmp_path: Path) -> None:
    pdf = tmp_path / "paper.pdf"

    paths = build_conversion_paths(pdf, tmp_path)

    assert paths.output_dir == tmp_path / "paper_converted"
    assert paths.markdown_path == tmp_path / "paper_converted" / "paper.md"
    assert paths.artifacts_dir == tmp_path / "paper_converted" / "mineru"
    assert paths.report_path == tmp_path / "paper_converted" / "conversion_report.json"


def test_extract_mineru_zip_saves_full_result_folder(tmp_path: Path) -> None:
    zip_data = _zip_bytes(
        {
            "paper/full.md": b"# Full",
            "paper/images/figure.png": b"fake-image",
        }
    )
    out_dir = tmp_path / "paper_mineru"

    extracted = extract_mineru_zip(zip_data, out_dir)

    assert extracted == out_dir
    assert (out_dir / "paper" / "full.md").read_text(encoding="utf-8") == "# Full"
    assert (out_dir / "paper" / "images" / "figure.png").read_bytes() == b"fake-image"


def test_extract_mineru_zip_rejects_path_traversal(tmp_path: Path) -> None:
    zip_data = _zip_bytes({"../escape.txt": b"nope"})

    with pytest.raises(ValueError, match="Unsafe ZIP member"):
        extract_mineru_zip(zip_data, tmp_path / "paper_mineru")


def test_smoke_check_warns_for_short_markdown_and_missing_mineru_files(tmp_path: Path) -> None:
    artifacts = tmp_path / "mineru"
    artifacts.mkdir()

    warnings = smoke_check_conversion("too short", artifacts)

    assert "markdown_chars_below_500" in warnings
    assert "mineru_full_md_or_content_list_missing" in warnings


def test_smoke_check_accepts_full_markdown_artifact(tmp_path: Path) -> None:
    artifacts = tmp_path / "mineru" / "paper"
    artifacts.mkdir(parents=True)
    (artifacts / "full.md").write_text("# Full", encoding="utf-8")

    warnings = smoke_check_conversion("x" * 600, tmp_path / "mineru")

    assert warnings == []


def test_write_conversion_report_records_outputs_and_warnings(tmp_path: Path) -> None:
    report_path = tmp_path / "conversion_report.json"
    pdf = tmp_path / "paper.pdf"
    md = tmp_path / "paper_converted" / "paper.md"
    artifacts = tmp_path / "paper_converted" / "mineru"

    write_conversion_report(
        report_path,
        input_pdf=pdf,
        output_md=md,
        artifacts_dir=artifacts,
        markdown_text="abc",
        warnings=["markdown_chars_below_500"],
    )

    data = json.loads(report_path.read_text(encoding="utf-8"))
    assert data["input_pdf"] == str(pdf)
    assert data["output_md"] == str(md)
    assert data["artifacts_dir"] == str(artifacts)
    assert data["converter"] == "MinerU"
    assert data["conda_env"] == "ai4math"
    assert data["markdown_chars"] == 3
    assert data["status"] == "success"
    assert data["warnings"] == ["markdown_chars_below_500"]


def test_get_markdown_from_pdf_rejects_missing_pdf(tmp_path: Path) -> None:
    missing = tmp_path / "missing.pdf"

    with pytest.raises(FileNotFoundError, match="PDF file does not exist"):
        get_markdown_from_pdf(missing, token="token")


def test_load_dotenv_file_sets_missing_values_without_overriding(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dotenv = tmp_path / ".env"
    dotenv.write_text(
        "\n".join(
            [
                'MINERU_API_TOKEN="from-dotenv"',
                "MINERU_LANGUAGE=en",
                "MINERU_BASE_URL=https://example.test",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.delenv("MINERU_API_TOKEN", raising=False)
    monkeypatch.setenv("MINERU_LANGUAGE", "zh")
    monkeypatch.delenv("MINERU_BASE_URL", raising=False)

    loaded = load_dotenv_file(dotenv)

    assert loaded == dotenv
    assert os.environ["MINERU_API_TOKEN"] == "from-dotenv"
    assert os.environ["MINERU_LANGUAGE"] == "zh"
    assert os.environ["MINERU_BASE_URL"] == "https://example.test"
