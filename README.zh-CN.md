# ai4math-paper-skills

[English](README.md) | 简体中文

本中文 README 聚焦安装、交互和 AI4Math 角色；完整维护细节见英文 README。

`ai4math-paper-skills` 是 AI4Math auto research 的论文到 Skill 工作流模块。
它不是论文摘要器，而是让 coding agent 从论文中抽取可迁移的证明套路、理论分析套路和
方法结构，生成可复核、可入库的 Skill Card。

## AI4Math 角色

这个 Skill 是 AI4Math 体系里的文献到方法抽取层。当论文需要转化为可复用 SkillCards、
proof-pattern candidates、method maps 或 research profiles，并继续交给发现、证明、优化、
复现等 Skill 使用时，优先用它。

## 交接

上游通常是 `paper.pdf`、`paper.md`、seed papers 或用户对研究方向的反馈。下游可以交给
`discover-math-problems` 生成新猜想，交给 `agentic-rethlas-proving` 测试 proof pattern，
交给优化 Skills 使用抽取出的优化方法，或交给计算复现 Skill 运行论文代码和实验。

## 安装 / 加载

优先从当前仓库 checkout 使用。让 coding agent 读取：

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
