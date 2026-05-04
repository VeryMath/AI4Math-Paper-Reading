"""Bootstrap PDF to Markdown conversion in the current working directory.

This script is intentionally stdlib-only. It creates or reuses the named Conda
environment `ai4math`, installs this skill's requirements there, creates `.env`
in the current directory if needed, and then runs the bundled MinerU converter.
"""

import argparse
import getpass
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


CONDA_ENV_NAME = "ai4math"

ENV_DEFAULTS = {
    "MINERU_BASE_URL": "https://mineru.net",
    "MINERU_MODEL_VERSION": "vlm",
    "MINERU_LANGUAGE": "ch",
    "MINERU_IS_OCR": "1",
    "MINERU_ENABLE_FORMULA": "1",
    "MINERU_ENABLE_TABLE": "1",
}


@dataclass(frozen=True)
class ConversionPaths:
    markdown_path: Path
    artifacts_dir: Path
    report_path: Path


def default_output_path(pdf_path: Path, cwd: Path) -> Path:
    return single_conversion_paths(pdf_path, cwd).markdown_path


def single_conversion_paths(pdf_path: Path, cwd: Path) -> ConversionPaths:
    output_dir = cwd / f"{pdf_path.stem}_converted"
    return ConversionPaths(
        markdown_path=output_dir / "paper.md",
        artifacts_dir=output_dir / "mineru",
        report_path=output_dir / "conversion_report.json",
    )


def batch_conversion_paths(pdf_path: Path, cwd: Path) -> ConversionPaths:
    output_dir = cwd / "outputs_markdown" / pdf_path.stem
    return ConversionPaths(
        markdown_path=output_dir / "paper.md",
        artifacts_dir=output_dir / "mineru",
        report_path=output_dir / "conversion_report.json",
    )


def collect_pdf_inputs(inputs: list[Path], *, batch: bool) -> list[Path]:
    pdfs: list[Path] = []
    for item in inputs:
        path = item.expanduser().resolve()
        if path.is_dir():
            if not batch:
                raise ValueError(f"Directory input requires --batch: {path}")
            pdfs.extend(sorted(path.glob("*.pdf")))
        elif path.is_file():
            if path.suffix.lower() != ".pdf":
                raise ValueError(f"Input file is not a PDF: {path}")
            pdfs.append(path)
        else:
            raise FileNotFoundError(f"PDF input does not exist: {path}")
    return sorted(dict.fromkeys(pdfs))


def _read_env_keys(dotenv_path: Path) -> set[str]:
    if not dotenv_path.exists():
        return set()
    keys: set[str] = set()
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key = line.split("=", 1)[0].strip()
        if key:
            keys.add(key)
    return keys


def write_env_defaults(dotenv_path: Path, *, token: str | None = None) -> None:
    existing_keys = _read_env_keys(dotenv_path)
    additions: list[str] = []

    if token and "MINERU_API_TOKEN" not in existing_keys:
        additions.append(f"MINERU_API_TOKEN={token}")

    for key, value in ENV_DEFAULTS.items():
        if key not in existing_keys:
            additions.append(f"{key}={value}")

    if not additions:
        return

    dotenv_path.parent.mkdir(parents=True, exist_ok=True)
    prefix = ""
    if dotenv_path.exists() and dotenv_path.read_text(encoding="utf-8").strip():
        prefix = "\n"
    with dotenv_path.open("a", encoding="utf-8") as handle:
        handle.write(prefix + "\n".join(additions) + "\n")


def _load_env_value(dotenv_path: Path, key: str) -> str:
    if key in os.environ and os.environ[key].strip():
        return os.environ[key].strip()
    if not dotenv_path.exists():
        return ""
    for raw_line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        current_key, value = line.split("=", 1)
        if current_key.strip() == key:
            return value.strip().strip("\"'")
    return ""


def ensure_api_key(dotenv_path: Path, *, non_interactive: bool = False) -> None:
    if _load_env_value(dotenv_path, "MINERU_API_TOKEN"):
        write_env_defaults(dotenv_path)
        return

    if non_interactive:
        raise RuntimeError(
            "MINERU_API_TOKEN is missing. Add it to .env or run without --non-interactive."
        )

    token = getpass.getpass("MinerU API key: ").strip()
    if not token:
        raise RuntimeError("MinerU API key is required.")
    write_env_defaults(dotenv_path, token=token)


def conda_create_command(conda_executable: str) -> list[str]:
    return [
        conda_executable,
        "create",
        "-y",
        "-n",
        CONDA_ENV_NAME,
        "python=3.13",
        "pip",
    ]


def conda_run_command(
    conda_executable: str,
    converter_script: Path,
    pdf_path: Path,
    output_path: Path,
    artifacts_dir: Path,
    report_path: Path,
) -> list[str]:
    return [
        conda_executable,
        "run",
        "-n",
        CONDA_ENV_NAME,
        "python",
        str(converter_script),
        str(pdf_path),
        "--out",
        str(output_path),
        "--artifacts-dir",
        str(artifacts_dir),
        "--report",
        str(report_path),
    ]


def _conda_env_exists(conda_executable: str) -> bool:
    result = subprocess.run(
        [conda_executable, "env", "list"],
        check=True,
        capture_output=True,
        text=True,
    )
    return any(line.split() and line.split()[0] == CONDA_ENV_NAME for line in result.stdout.splitlines())


def ensure_conda_env(requirements_path: Path) -> str:
    conda_executable = shutil.which("conda")
    if not conda_executable:
        raise RuntimeError("conda was not found on PATH. Install Anaconda/Miniconda first.")

    if not _conda_env_exists(conda_executable):
        subprocess.run(conda_create_command(conda_executable), check=True)

    subprocess.run(
        [
            conda_executable,
            "run",
            "-n",
            CONDA_ENV_NAME,
            "python",
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements_path),
        ],
        check=True,
    )
    return conda_executable


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Use Conda env ai4math plus local .env to convert a PDF to Markdown with MinerU."
    )
    parser.add_argument("inputs", nargs="+", help="Input PDF path(s), or directories when --batch is set")
    parser.add_argument(
        "--out",
        help="Output Markdown path for a single PDF. Defaults to ./<pdf-stem>_converted/paper.md.",
    )
    parser.add_argument(
        "--artifacts-dir",
        help="Artifacts folder for a single PDF. Defaults to ./<pdf-stem>_converted/mineru.",
    )
    parser.add_argument(
        "--report",
        help="Report path for a single PDF. Defaults to ./<pdf-stem>_converted/conversion_report.json.",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Allow directory input and write outputs under ./outputs_markdown/<pdf-stem>/.",
    )
    parser.add_argument(
        "--non-interactive",
        action="store_true",
        help="Fail instead of prompting when MINERU_API_TOKEN is missing.",
    )
    args = parser.parse_args(argv)

    cwd = Path.cwd()
    skill_scripts_dir = Path(__file__).resolve().parent
    input_paths = [Path(value) for value in args.inputs]
    pdf_paths = collect_pdf_inputs(input_paths, batch=args.batch)
    if not pdf_paths:
        raise FileNotFoundError("No PDF files found.")
    if len(pdf_paths) > 1 and (args.out or args.artifacts_dir or args.report):
        raise ValueError("--out, --artifacts-dir, and --report are only valid for a single PDF.")

    dotenv_path = cwd / ".env"
    ensure_api_key(dotenv_path, non_interactive=args.non_interactive)

    conda_executable = ensure_conda_env(skill_scripts_dir / "requirements.txt")
    for pdf_path in pdf_paths:
        if len(pdf_paths) == 1:
            defaults = single_conversion_paths(pdf_path, cwd)
            output_path = Path(args.out).expanduser().resolve() if args.out else defaults.markdown_path
            artifacts_dir = (
                Path(args.artifacts_dir).expanduser().resolve()
                if args.artifacts_dir
                else defaults.artifacts_dir
            )
            report_path = Path(args.report).expanduser().resolve() if args.report else defaults.report_path
        else:
            paths = batch_conversion_paths(pdf_path, cwd)
            output_path = paths.markdown_path
            artifacts_dir = paths.artifacts_dir
            report_path = paths.report_path

        subprocess.run(
            conda_run_command(
                conda_executable,
                skill_scripts_dir / "pdf_to_markdown.py",
                pdf_path,
                output_path,
                artifacts_dir,
                report_path,
            ),
            check=True,
            cwd=str(cwd),
        )

        print(f"Markdown written to: {output_path}")
        print(f"MinerU artifacts written to: {artifacts_dir}")
        print(f"Conversion report written to: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
