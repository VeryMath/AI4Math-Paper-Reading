# Paper to Skill Extractor

Codex skill for extracting reusable mathematical research skills from Markdown papers.

This repository is a skill package, not a standalone Python pipeline. Codex itself is the extraction engine. The current focus is proof-pattern mining from `paper.md` files, especially reusable techniques such as descent lemmas, inequality relaxations, telescoping bounds, Lyapunov arguments, concentration bounds, Galerkin/Cea arguments, Aubin-Nitsche duality, Lax-Milgram well-posedness, and geometry-aware sampling analyses.

## What It Produces

For each paper, the skill writes:

```text
outputs/<paper_id>/
├── paper.md
├── skill_candidates.json
├── skill_cards/
│   └── <skill_name>.yaml
└── report.md
```

Each extracted skill includes source line references back to `paper.md`.

## Repository Layout

```text
paper-to-skill-extractor/
├── SKILL.md
├── agents/openai.yaml
├── assets/
│   ├── report_template.md
│   ├── skill_candidate_template.yaml
│   └── skill_card_template.yaml
├── references/
│   ├── extraction_protocol.md
│   ├── proof_pattern_taxonomy.md
│   ├── quality_rubric.md
│   └── schemas.md
└── examples/
    ├── 2510.08929v1/
    └── 2602.05174v1/
```

The `examples/` directory contains generated reports, candidates, and skill cards. It intentionally does not include full paper Markdown files.

## Install

Copy this folder into Codex skills:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R paper-to-skill-extractor "${CODEX_HOME:-$HOME/.codex}/skills/paper-to-skill-extractor"
```

Restart Codex or reload skills if your client requires it.

## Input Format

Cursor users can usually provide a PDF directly and ask the agent to extract skills from it.

Codex users should provide Markdown input for this skill. If your source is a PDF, first convert it to `paper.md`. The recommended workflow is to use this skill together with the [PDF-to-Markdown companion skill](https://github.com/ConanXu-math/pdf-to-markdown-converter).

Typical Codex workflow:

```text
PDF -> pdf-to-markdown-converter -> paper.md -> paper-to-skill-extractor -> skill cards
```

## Usage

Prepare a Markdown paper:

```text
paper.md
```

Then ask Codex to use the skill, for example:

```text
Use paper-to-skill-extractor on paper.md and write outputs to outputs/my-paper.
```

For PDFs in Codex, convert to Markdown first with the [PDF-to-Markdown companion skill](https://github.com/ConanXu-math/pdf-to-markdown-converter).

## Output Quality Rules

The skill is designed to extract reusable proof methods, not paper summaries.

Valid candidates must have:

- clear inputs and outputs;
- explicit assumptions or applicability conditions;
- operational proof steps;
- trigger keywords;
- limitations and mathematical risks;
- source line references to `paper.md`.

Rejected material includes:

- related work and motivation;
- experiments and implementation notes;
- theorem statements without transferable proof method;
- paper-specific conclusions that do not generalize.

## Examples

The included examples were produced from two Markdown papers:

- `2510.08929v1`: mirror flow matching on convex domains.
- `2602.05174v1`: total variation rates for Riemannian flow matching.

See:

```text
examples/2510.08929v1/report.md
examples/2602.05174v1/report.md
```

These examples show the expected artifact shape and scoring style. The original `paper.md` files are omitted from the repository to keep the package small and avoid redistributing full papers.

## License

MIT. See `LICENSE`.
