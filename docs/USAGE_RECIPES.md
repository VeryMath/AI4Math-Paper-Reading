# Usage Recipes

Use these prompts with any coding agent that can read files, write artifacts,
and follow the Skill instructions in this repository.

## 0. Process One PDF End-To-End

```text
使用 paper-to-skill-workflow。

请处理下面这篇论文：
/absolute/path/to/paper.pdf

输出到：
outputs/<research_project_id>/papers/<paper_id>/

要求：
1. 保留原始 paper.pdf。
2. 转换生成完整 paper.md。
3. 基于 paper.md 抽取 proof_pattern SkillCandidates 和 SkillCards。
4. 每个 accepted_candidate 或 needs_review SkillCard 必须包含 source.paper_md、source.start_line、source.end_line。
5. 生成 report.md，并区分 accepted_candidate / needs_review / rejected。
```

## 1. Build A Research Profile

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

## 2. Retrieve Related And Innovative Papers

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

## 3. Generate A Reading Plan

```text
使用 paper-triage-ranker。

请基于下面三个文件生成阅读计划：

- outputs/<research_project_id>/research_profile.json
- outputs/<research_project_id>/candidate_papers.json
- outputs/<research_project_id>/innovation_candidates.json
- outputs/<research_project_id>/human_feedback_state.json
```

## 4. Download Confirmed PDFs

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

## 5. Convert PDFs To Markdown

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

## 6. Extract Single-Paper Proof Patterns

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

## 7. Synthesize Across Papers

```text
使用 cross-paper-skill-synthesizer。

请基于多个 paper-to-skill-extractor 输出的 skill_cards 目录，做跨论文聚类、合并和泛化：

- outputs/<research_project_id>/papers/<paper_id_1>/skill_cards
- outputs/<research_project_id>/papers/<paper_id_2>/skill_cards
- outputs/<research_project_id>/human_feedback_state.json

输出到：
outputs/<research_project_id>/synthesized_skills
```
