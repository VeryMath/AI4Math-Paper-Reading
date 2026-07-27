from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    "after-ocr": ("Dong Yuan", "df5110e2bdf2271cd373542bb094e63a0ce24770d1e56c19991de817dbf58b4c"),
    "graph-theory-paper-reading": (
        "Zhuojie Tu",
        "e66fe2d8f3074a2dc5b6a51605f6a29a8be826278b76eefec3369c7a86f52208",
    ),
}
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".txt"}


def frontmatter_keys(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise AssertionError(f"Missing YAML frontmatter: {path}")
    return {
        line.split(":", 1)[0].strip()
        for line in match.group(1).splitlines()
        if line and not line.startswith((" ", "\t"))
    }


class CourseSkillTests(unittest.TestCase):
    def test_package_shape_and_provenance(self) -> None:
        for package, (contributor, sha256) in PACKAGES.items():
            with self.subTest(package=package):
                root = ROOT / "skills" / package
                for relative in (
                    "README.md",
                    "SKILL.md",
                    "LICENSE",
                    "PROVENANCE.yaml",
                    "NORMALIZATION.md",
                ):
                    self.assertTrue((root / relative).is_file(), f"Missing {package}/{relative}")
                self.assertEqual({"name", "description"}, frontmatter_keys(root / "SKILL.md"))
                provenance = (root / "PROVENANCE.yaml").read_text(encoding="utf-8")
                self.assertIn(contributor, provenance)
                self.assertIn(sha256, provenance)
                self.assertIn("license: MIT", provenance)

    def test_packages_have_no_machine_local_paths_or_secret_placeholders(self) -> None:
        forbidden = re.compile(r"/Users/|/home/|[A-Za-z]:\\\\|API[_ -]?KEY|SECRET|TOKEN")
        for package in PACKAGES:
            root = ROOT / "skills" / package
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                    with self.subTest(path=path):
                        self.assertIsNone(forbidden.search(path.read_text(encoding="utf-8")))

    def test_mineru_is_an_opt_in_dependency(self) -> None:
        root = ROOT / "skills" / "graph-theory-paper-reading"
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        readme = (root / "README.md").read_text(encoding="utf-8")
        self.assertIn("取得用户明确", skill)
        self.assertIn("explicit user approval", readme)


if __name__ == "__main__":
    unittest.main()
