# paper-to-skill

[English](README.md) | 简体中文

`paper-to-skill` 是一个独立的 coding-agent skill，用来把论文转换成可复用的 SkillCards、proof-pattern candidates、method maps 和 review reports。
它不是论文摘要器；核心目标是保留原始论文，带 source references 抽取可迁移推理模式，并生成可由人类 review 或整理入库的 artifacts。

## 这个 Skill 做什么

这个独立 Skill 帮助 coding agent：

- 保留输入的 `paper.pdf` 或 `paper.md`；
- 需要时把 PDF 转成 Markdown；
- 抽取 proof patterns、theoretical-analysis routines、algorithmic methods 和 reusable SkillCards；
- 把 source lines 引回转换后的论文文本；
- 在需要时把多篇论文综合成紧凑的 method map。

当你希望把论文变成可检查、可复用的研究方法 artifacts 时，可以直接使用它。

## 安装 / 加载

在你的 coding-agent 环境里 clone 或打开这个 skill 仓库，然后让 coding agent 读取：

```text
AGENTS.md
SKILL.md
skills/registry.yaml
```

如果目标 agent 支持本地 Skill discovery，可以把本仓库或相关 concrete Skill folder
安装或软链接到它的 Skill 路径，然后按需 reload 或 restart。Codex、Claude、Gemini
和 OpenCode 的薄 adapter 分别见 `.codex/INSTALL.md`、`CLAUDE.md`、`GEMINI.md`
和 `.opencode/INSTALL.md`。

## 快速开始

```text
Use this repository's paper-to-skill workflow.

Read:
- AGENTS.md
- SKILL.md
- skills/registry.yaml
- skills/paper-to-skill-workflow/SKILL.md

Input:
/absolute/path/to/paper.pdf

Output:
outputs/<research_project_id>/papers/<paper_id>/

Goal:
保留 paper.pdf，转换生成 paper.md，基于 source line references 抽取
SkillCandidates、SkillCards 和 report.md。
```

如果已经有 `paper.md`，可以跳过 PDF 转换，直接进入抽取阶段。

## 如何交互使用

推荐使用 checkpoint 循环：

```text
论文或研究目标 -> phase routing -> 计划 -> approve / revise / reject / skip
                -> 获批转换、抽取、检索或综合
                -> 证据报告 -> 下一轮 checkpoint
```

`approve` 表示执行下一步，`revise` 表示先修改计划或研究重点，`reject` 表示停止当前路线，
`skip` 表示跳过当前阶段。Agent 必须保留原始 PDF 和完整 Markdown；accepted 或
needs-review 的 SkillCard 必须带 `source.paper_md`、`source.start_line` 和
`source.end_line`。

## Skill Chain

- `seed-paper-profiler`：根据种子论文生成研究画像。
- `related-paper-retriever`：检索直接相关论文。
- `innovation-paper-finder`：寻找可能带来新方法或证明想法的论文。
- `paper-triage-ranker`：把候选论文排成阅读计划。
- `paper-pdf-downloader`：只下载确认开放获取的 PDF。
- `pdf-to-markdown-converter`：把 PDF 转成 Markdown。
- `paper-to-skill-workflow`：面向用户的一篇论文端到端工作流。
- `paper-to-skill-extractor`：从单篇 `paper.md` 抽取 proof-pattern Skills。
- `cross-paper-skill-synthesizer`：跨论文聚合和泛化 SkillCards。

## 输出

默认输出放在：

```text
outputs/<research_project_id>/
```

结构化 JSON、YAML 和报告只是索引和 review artifacts，不替代原始论文和完整 `paper.md`。
