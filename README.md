# paper-to-skill

Chinese guide: [README.zh-CN.md](README.zh-CN.md)

`paper-to-skill` is a standalone coding-agent skill for turning papers into reusable SkillCards, proof-pattern candidates, method maps, and review reports. It is not a paper summarizer: the goal is to preserve the source paper, extract reusable reasoning patterns with source references, and produce artifacts that a human can review or curate.

## What This Skill Does

This standalone skill helps a coding agent:

- preserve an input `paper.pdf` or `paper.md`;
- convert PDF to Markdown when needed;
- extract proof patterns, theoretical-analysis routines, algorithmic methods, and reusable SkillCards;
- cite source lines back to the converted paper text;
- synthesize multiple papers into a compact method map when requested.

Use it directly when you want a paper turned into inspectable, reusable research-method artifacts.

## Current Direction

The current direction is a human-in-the-loop automatic research workflow:

```text
seed papers
  -> seed-paper-profiler
  -> human_feedback_state.json
  -> related-paper-retriever + innovation-paper-finder
  -> paper-triage-ranker
  -> paper-pdf-downloader
  -> pdf-to-markdown-converter
  -> paper-to-skill-extractor
  -> cross-paper-skill-synthesizer
  -> domain method map + merged SkillCards
```

核心原则：

- Use the active coding agent as the research reasoning and extraction engine.
- Accept `paper.pdf` as the simplest user input.
- Do not rely on external LLM APIs for extraction.
- Preserve every original `paper.pdf` when provided and every converted `paper.md`.
- Every extracted Skill must keep source line references.
- Keep each Skill narrow: retrieval, triage, download, conversion, extraction, and synthesis are separate responsibilities.

## Installation / Loading

### One-line Agent Install

Copy this to your coding agent:

```text
Please install the `paper-to-skill` skill from https://github.com/VeryMath/AI4Math-Paper-Reading.git (branch: kn-Xu). Read `.agent.md`, install the declared Skill entrypoint, verify that `$paper-to-skill` is discoverable, and tell me whether I need to restart the agent.
```

If you already have this skill repository locally, replace the repository URL
with the local folder path. The coding agent should handle cloning, linking,
configuration, reload/restart checks, and verification.

## Quick Start

Give a coding agent a PDF and an output directory:

```text
Use this repository's paper-to-skill workflow.

Read:
- AGENTS.md
- skills/registry.yaml
- skills/paper-to-skill-workflow/SKILL.md

Input:
/absolute/path/to/paper.pdf

Output:
outputs/<research_project_id>/papers/<paper_id>/

Goal:
Preserve the PDF, convert it to paper.md, then extract proof_pattern SkillCandidates,
SkillCards, and report.md with source line references back to paper.md.
```

If you already have `paper.md`, use the same workflow and provide the Markdown file as input. The workflow skips PDF conversion and runs extraction directly.

## How To Interact

Use a checkpoint loop:

```text
paper or research goal -> phase routing -> plan -> approve / revise / reject / skip
                       -> approved conversion, extraction, retrieval, or synthesis
                       -> evidence report -> next checkpoint
```

Use `approve` to run a proposed step, `revise` to update the plan or research
focus, `reject` to stop the path, and `skip` to move past a phase. The agent
should preserve original PDFs and Markdown, cite source lines for accepted or
review-worthy SkillCards, and ask before downloads, broad retrieval expansion,
or final library insertion decisions.

## Skill Chain

| Skill | Input | Output | Responsibility |
| --- | --- | --- | --- |
| `seed-paper-profiler` | seed papers, abstracts, notes | `research_profile.json` | infer research interest profile |
| `related-paper-retriever` | `research_profile.json` | `candidate_papers.json` | find directly related papers |
| `innovation-paper-finder` | `research_profile.json` | `innovation_candidates.json` | find papers with possible new methods or proof ideas |
| `paper-triage-ranker` | candidate lists | `reading_plan.json` | rank papers into reading priorities |
| `paper-pdf-downloader` | `reading_plan.json` or selected paper IDs | `papers/<paper_id>/paper.pdf` | download confirmed open-access PDFs only |
| `pdf-to-markdown-converter` | local PDF | `paper.md` | convert PDF to Markdown |
| `paper-to-skill-workflow` | `paper.pdf` or `paper.md` | `paper.md`, `skill_candidates.json`, `skill_cards/*.yaml`, `report.md` | run the user-facing PDF-first workflow |
| `paper-to-skill-extractor` | `paper.md` | `skill_candidates.json`, `skill_cards/*.yaml`, `report.md` | extract single-paper `proof_pattern` Skills |
| `cross-paper-skill-synthesizer` | multiple Skill Cards | `domain_method_map.yaml`, merged Skill Cards | cluster, merge, and generalize across papers |

## Skill Metadata

The repository has a thin root Skill compatibility entrypoint at `SKILL.md`. It points back to the shared Skill layer and does not define a separate workflow.

Use `skills/registry.yaml` as the machine-readable source for Skill routing, phase order, input/output contracts, and review gates. Each Skill folder also has a `manifest.yaml` that declares its entrypoint, expected input artifacts, output artifacts, dependent Skills, risk level, and operations that require human approval.

The default registry entrypoint is `paper-to-skill-workflow`:

```text
paper.pdf -> paper.md -> proof_pattern SkillCandidate / SkillCard / report
```

## Platform Adapters

The shared product is the Skill layer under `skills/`. Platform-specific files are intentionally thin adapters:

- `SKILL.md`: generic top-level Skill entrypoint.
- `AGENTS.md`: repository contract for coding agents that read agent instructions.
- `CLAUDE.md`: Claude Code orientation.
- `GEMINI.md`: Gemini orientation.
- `.codex/INSTALL.md`: Codex loading notes.
- `.opencode/INSTALL.md`: OpenCode loading notes.
- `.cursor/rules/paper-to-skill.mdc`: Cursor rule entrypoint.
- `.github/copilot-instructions.md`: GitHub Copilot coding agent instructions.

All adapters should point back to `skills/registry.yaml` and should not fork workflow behavior.

## Output Layout

Recommended project output layout:

```text
outputs/<research_project_id>/
├── seed_papers/
├── research_profile.json
├── human_feedback_state.json
├── candidate_papers.json
├── innovation_candidates.json
├── reading_plan.json
├── papers/
│   └── <paper_id>/
│       ├── metadata.json
│       ├── paper.pdf
│       ├── paper.md
│       ├── mineru/
│       └── conversion_report.json
├── extractions/
│   └── <paper_id>/
│       ├── paper.md
│       ├── skill_candidates.json
│       ├── skill_cards/
│       └── report.md
├── synthesized_skills/
│   ├── domain_method_map.yaml
│   ├── merged_skill_cards/
│   └── synthesis_report.md
└── workflow_report.md
```

Local trial runs should live under `outputs/<research_project_id>/`, which is intentionally git-ignored.

The complete reproducible example copy lives at:

[examples/auto_research_trial](examples/auto_research_trial)

## Human-in-the-loop Research State

Use `human_feedback_state.json` to keep human feedback inside the workflow instead of leaving it only in chat history.

```text
outputs/<research_project_id>/human_feedback_state.json
```

This file records how the user corrects or redirects the active coding agent's current interpretation of the research direction. The agent can create or update it from natural-language feedback; the user does not need to hand-write JSON.

Minimum fields:

- `focus_updates`: research directions to emphasize.
- `negative_preferences`: topics, paper types, or methods to down-rank.
- `paper_decisions`: user decisions such as `must_read`, `skip`, `download`, or `do_not_download`.
- `skill_decisions`: user decisions on extracted Skill Cards such as `accept`, `revise`, `reject`, or `merge`.
- `next_step_directives`: instructions that later Skills must apply.
- `stage_feedback_log`: chronological record of human feedback and how it should affect the next stage.

Example user feedback:

```text
弱化 heavy-tailed prior 本身，强化 Wasserstein error、coupling bias 和可复用 proof pattern。
后续检索不要找太多纯实验型 flow matching paper。
```

The next Skill should read both the previous machine artifact and `human_feedback_state.json`. In practice:

```text
research_profile.json + human_feedback_state.json -> retrieval
candidate_papers.json + innovation_candidates.json + human_feedback_state.json -> triage
reading_plan.json + human_feedback_state.json -> download / extraction
skill_cards + human_feedback_state.json -> synthesis
```

## Usage Recipes

The README keeps only the first prompt and workflow map. Longer copy-paste
recipes for profiling, retrieval, triage, download, conversion, extraction, and
cross-paper synthesis live in [docs/USAGE_RECIPES.md](docs/USAGE_RECIPES.md).

## Python Environment

The Skill workflow itself does not require a Python package or external LLM API. Python is currently used for helper scripts such as PDF conversion, PDF download, and validation.

Use the shared Conda environment:

```bash
conda create -y -n ai4math python=3.13 pip
conda activate ai4math
python -m pip install -r requirements-dev.txt
```

## Boundaries

`paper-to-skill-workflow` is the user-facing entrypoint:

```text
paper.pdf -> paper.md -> proof_pattern SkillCandidate / SkillCard / report
```

`paper-to-skill-extractor` remains intentionally narrow: it reads `paper.md` and writes proof-pattern extraction artifacts. PDF conversion, retrieval, download, extraction, and synthesis stay in separate Skills so each responsibility can be reviewed and improved independently.

Retrieval Skills do not implement a search engine. They define agent search strategy, relevance criteria, output schema, and human checkpoints.

Download and conversion are explicit, user-confirmed steps. Always preserve the original `paper.pdf` and the full `paper.md`.
