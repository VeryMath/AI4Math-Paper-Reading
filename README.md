<div align="center">

# AI4Math · Paper Reading

Structured workflows for reading mathematical papers, extracting proof
dependencies, and turning papers into reusable AI4Math skills.

[中文说明](README.zh-CN.md) · [Contributors](CONTRIBUTORS.md) · [Skill packages](#skill-packages) · [Quick start](#quick-start) · [Security model](#security-and-scope)

![version](https://img.shields.io/badge/version-0.1.0-blue)
![skills](https://img.shields.io/badge/skills-2-2ea44f)
![license](https://img.shields.io/badge/license-MIT-green)

</div>

## What This Repository Is

This repository is the AI4Math home for paper-reading skills. It does not try
to be a single monolithic agent. Instead, each package under `skills/` owns a
focused workflow, its own README, and the agent instructions needed to run it.

Use the root page as the public map, then open the package that matches your
task.

## Skill Packages

| Package | Use it for | Start here |
| --- | --- | --- |
| [`paper-to-skill`](skills/paper-to-skill/) | Run the full paper-to-skill workflow: PDF preparation, paper triage, proof-pattern extraction, and cross-paper synthesis. | [`README`](skills/paper-to-skill/README.md) · [`SKILL`](skills/paper-to-skill/SKILL.md) |
| [`math-paper-reading`](skills/math-paper-reading/) | Read papers deeply, extract theorem dependencies, build proof pathways, and manage local reference notes. | [`README`](skills/math-paper-reading/README.md) · [`SKILL`](skills/math-paper-reading/SKILL.md) · [`router`](skills/math-paper-reading/agent_router.md) |

## Quick Start

Clone the repository and choose a package:

```bash
git clone https://github.com/VeryMath/AI4Math-Paper-Reading.git
cd AI4Math-Paper-Reading
```

For reusable skill extraction, start with:

```text
skills/paper-to-skill/SKILL.md
```

For structured paper reading, start with:

```text
skills/math-paper-reading/agent_router.md
```

## Repository Layout

```text
AI4Math-Paper-Reading/
├── README.md
├── README.zh-CN.md
├── SKILL.md
└── skills/
    ├── paper-to-skill/
    └── math-paper-reading/
```

Package-local examples are illustrative fixtures. Derived outputs from private
papers should stay outside git unless they are intentionally sanitized examples.

## Validation

There is no root build step. When changing a package, validate its `SKILL.md`
and README links, then run any package-local tests or scripts described by that
package. If you use Codex's local skill validator, run it against the changed
package directory.

## Security and Scope

Do not commit private papers, unpublished notes, local databases with personal
annotations, API keys, `.env` files, or generated caches. Keep public examples
small, source-attributed, and safe to redistribute.
