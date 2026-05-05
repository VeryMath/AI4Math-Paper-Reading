# ai4math-paper-skills

`ai4math-paper-skills` is a Codex-native paper-to-skill workflow module for AI4Math auto research.

本项目不是论文总结器，也不是完整的 auto research 主仓库。它是 AI4Math auto research 的论文 Skill 子模块：让 Codex 从论文中识别可迁移的证明套路、理论分析套路和方法论结构，生成可复核、可入库的 Skill Card。

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

- Use Codex as the research reasoning and extraction engine.
- Do not build a custom search engine in v0.1.
- Do not rely on external LLM APIs in v0.1.
- Preserve every `paper.md` as the source of truth.
- Every extracted Skill must keep source line references.
- Keep each Skill narrow: retrieval, triage, download, conversion, extraction, and synthesis are separate responsibilities.

## Skill Chain

| Skill | Input | Output | Responsibility |
| --- | --- | --- | --- |
| `seed-paper-profiler` | seed papers, abstracts, notes | `research_profile.json` | infer research interest profile |
| `related-paper-retriever` | `research_profile.json` | `candidate_papers.json` | find directly related papers |
| `innovation-paper-finder` | `research_profile.json` | `innovation_candidates.json` | find papers with possible new methods or proof ideas |
| `paper-triage-ranker` | candidate lists | `reading_plan.json` | rank papers into reading priorities |
| `paper-pdf-downloader` | `reading_plan.json` or selected paper IDs | `papers/<paper_id>/paper.pdf` | download confirmed open-access PDFs only |
| `pdf-to-markdown-converter` | local PDF | `paper.md` | convert PDF to Markdown |
| `paper-to-skill-extractor` | `paper.md` | `skill_candidates.json`, `skill_cards/*.yaml`, `report.md` | extract single-paper `proof_pattern` Skills |
| `cross-paper-skill-synthesizer` | multiple Skill Cards | `domain_method_map.yaml`, merged Skill Cards | cluster, merge, and generalize across papers |

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

This file records how the user corrects or redirects Codex's current interpretation of the research direction. Codex can create or update it from natural-language feedback; the user does not need to hand-write JSON.

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

## How To Run With Codex

Use these as Codex instructions.

### 1. Build A Research Profile

```text
使用 seed-paper-profiler。

请基于下面几篇种子论文生成一个研究兴趣画像：

- /absolute/path/to/paper_1.md
- /absolute/path/to/paper_2.md

输出到：
outputs/<research_project_id>

如果用户已经给出方向修正，请同时创建或更新：
outputs/<research_project_id>/human_feedback_state.json
```

### 2. Retrieve Related And Innovative Papers

```text
使用 related-paper-retriever 和 innovation-paper-finder。

请基于：
outputs/<research_project_id>/research_profile.json

如果存在，也必须读取：
outputs/<research_project_id>/human_feedback_state.json

检索相关论文和可能提供创新点的论文，生成：
- candidate_papers.json
- innovation_candidates.json
- bilingual reports
```

### 3. Generate A Reading Plan

```text
使用 paper-triage-ranker。

请基于下面三个文件生成阅读计划：

- outputs/<research_project_id>/research_profile.json
- outputs/<research_project_id>/candidate_papers.json
- outputs/<research_project_id>/innovation_candidates.json
- outputs/<research_project_id>/human_feedback_state.json
```

### 4. Download Confirmed PDFs

```text
使用 paper-pdf-downloader。

请下载 reading_plan.json 里 download_queue 的前 N 篇：

outputs/<research_project_id>/reading_plan.json

如果存在，也必须读取：
outputs/<research_project_id>/human_feedback_state.json
```

Download policy:

- Only download open-access PDFs or user-provided PDFs.
- Do not bypass paywalls.
- Preserve `metadata.json`, `paper.pdf`, and source URLs.

### 5. Convert PDFs To Markdown

```text
使用 pdf-to-markdown-converter。

请把下面 PDF 转成 paper.md：

outputs/<research_project_id>/papers/<paper_id>/paper.pdf

如果存在，保留并传递本项目的人类反馈状态：
outputs/<research_project_id>/human_feedback_state.json
```

Equivalent command:

```bash
python skills/pdf-to-markdown-converter/scripts/bootstrap_pdf_to_markdown.py \
  outputs/<research_project_id>/papers/<paper_id>/paper.pdf \
  --out outputs/<research_project_id>/papers/<paper_id>/paper.md \
  --artifacts-dir outputs/<research_project_id>/papers/<paper_id>/mineru \
  --report outputs/<research_project_id>/papers/<paper_id>/conversion_report.json \
  --non-interactive
```

### 6. Extract Single-Paper Proof Patterns

```text
使用 paper-to-skill-extractor。

请基于下面 paper.md 抽取第一版 proof_pattern Skill Card：

outputs/<research_project_id>/papers/<paper_id>/paper.md

如果存在，也必须读取：
outputs/<research_project_id>/human_feedback_state.json

要求：
1. 输出中英文并列。
2. 每个 Skill 必须包含 source.paper_md、start_line、end_line。
3. 区分 accepted_candidate / needs_review / rejected。
```

### 7. Synthesize Across Papers

```text
使用 cross-paper-skill-synthesizer。

请基于多个 paper-to-skill-extractor 输出的 skill_cards 目录，做跨论文聚类、合并和泛化：

- outputs/<research_project_id>/papers/<paper_id_1>/skill_cards
- outputs/<research_project_id>/papers/<paper_id_2>/skill_cards
- outputs/<research_project_id>/human_feedback_state.json

输出到：
outputs/<research_project_id>/synthesized_skills
```

## Python Environment

The Codex Skill workflow itself does not require a Python package or external LLM API. Python is currently used for helper scripts such as PDF conversion, PDF download, and validation.

Use the shared Conda environment:

```bash
conda create -y -n ai4math python=3.13 pip
conda activate ai4math
python -m pip install -r requirements-dev.txt
```

## Boundaries

`paper-to-skill-extractor` is intentionally narrow:

```text
paper.md -> proof_pattern SkillCandidate / SkillCard / report
```

It does not retrieve papers, download PDFs, convert PDFs, rank candidates, or merge cross-paper Skills. Those responsibilities belong to separate Skills.

Retrieval Skills do not implement a search engine. They define Codex search strategy, relevance criteria, output schema, and human checkpoints.

Download and conversion are explicit, user-confirmed steps. Always preserve the original `paper.pdf` and the full `paper.md`.
