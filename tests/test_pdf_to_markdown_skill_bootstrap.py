import importlib.util
import sys
from pathlib import Path


def _load_bootstrap_module():
    path = Path("skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py")
    spec = importlib.util.spec_from_file_location("pdf_to_markdown_bootstrap", path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_default_output_path_is_current_directory(tmp_path: Path) -> None:
    module = _load_bootstrap_module()
    pdf = tmp_path / "nested" / "paper.pdf"

    assert module.default_output_path(pdf, tmp_path) == tmp_path / "paper_converted" / "paper.md"


def test_write_env_preserves_existing_token(tmp_path: Path) -> None:
    module = _load_bootstrap_module()
    dotenv = tmp_path / ".env"
    dotenv.write_text("MINERU_API_TOKEN=old-token\nMINERU_LANGUAGE=en\n", encoding="utf-8")

    module.write_env_defaults(dotenv, token="new-token")

    text = dotenv.read_text(encoding="utf-8")
    assert "MINERU_API_TOKEN=old-token" in text
    assert "MINERU_API_TOKEN=new-token" not in text
    assert "MINERU_BASE_URL=https://mineru.net" in text
    assert "MINERU_LANGUAGE=en" in text


def test_write_env_adds_token_and_defaults(tmp_path: Path) -> None:
    module = _load_bootstrap_module()
    dotenv = tmp_path / ".env"

    module.write_env_defaults(dotenv, token="abc123")

    text = dotenv.read_text(encoding="utf-8")
    assert "MINERU_API_TOKEN=abc123" in text
    assert "MINERU_BASE_URL=https://mineru.net" in text
    assert "MINERU_MODEL_VERSION=vlm" in text
    assert "MINERU_ENABLE_FORMULA=1" in text


def test_conda_run_command_uses_ai4math_named_environment(tmp_path: Path) -> None:
    module = _load_bootstrap_module()
    script = tmp_path / "pdf_to_markdown.py"
    pdf = tmp_path / "paper.pdf"
    out = tmp_path / "paper.md"
    artifacts = tmp_path / "paper_mineru"
    report = tmp_path / "conversion_report.json"

    assert module.conda_run_command("conda", script, pdf, out, artifacts, report) == [
        "conda",
        "run",
        "-n",
        "ai4math",
        "python",
        str(script),
        str(pdf),
        "--out",
        str(out),
        "--artifacts-dir",
        str(artifacts),
        "--report",
        str(report),
    ]


def test_conda_create_command_uses_ai4math_named_environment() -> None:
    module = _load_bootstrap_module()

    assert module.conda_create_command("conda") == [
        "conda",
        "create",
        "-y",
        "-n",
        "ai4math",
        "python=3.13",
        "pip",
    ]


def test_default_single_conversion_paths_are_grouped(tmp_path: Path) -> None:
    module = _load_bootstrap_module()
    pdf = tmp_path / "paper.pdf"

    paths = module.single_conversion_paths(pdf, tmp_path)

    assert paths.markdown_path == tmp_path / "paper_converted" / "paper.md"
    assert paths.artifacts_dir == tmp_path / "paper_converted" / "mineru"
    assert paths.report_path == tmp_path / "paper_converted" / "conversion_report.json"


def test_batch_conversion_paths_use_outputs_markdown_root(tmp_path: Path) -> None:
    module = _load_bootstrap_module()
    pdf = tmp_path / "papers" / "alpha.pdf"

    paths = module.batch_conversion_paths(pdf, tmp_path)

    assert paths.markdown_path == tmp_path / "outputs_markdown" / "alpha" / "paper.md"
    assert paths.artifacts_dir == tmp_path / "outputs_markdown" / "alpha" / "mineru"
    assert paths.report_path == tmp_path / "outputs_markdown" / "alpha" / "conversion_report.json"


def test_collect_pdf_inputs_accepts_files_and_batch_directories(tmp_path: Path) -> None:
    module = _load_bootstrap_module()
    papers = tmp_path / "papers"
    papers.mkdir()
    alpha = papers / "alpha.pdf"
    beta = papers / "beta.pdf"
    alpha.write_bytes(b"%PDF")
    beta.write_bytes(b"%PDF")
    (papers / "note.txt").write_text("ignore", encoding="utf-8")

    assert module.collect_pdf_inputs([papers], batch=True) == [alpha, beta]


def test_collect_pdf_inputs_rejects_directory_without_batch(tmp_path: Path) -> None:
    module = _load_bootstrap_module()
    papers = tmp_path / "papers"
    papers.mkdir()

    try:
        module.collect_pdf_inputs([papers], batch=False)
    except ValueError as exc:
        assert "--batch" in str(exc)
    else:
        raise AssertionError("Expected directory input without --batch to fail")
