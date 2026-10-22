# paper-to-skill

[English](README.md) | 简体中文

`paper-to-skill` 帮助 coding agent 把论文转换成 reusable SkillCards、proof-pattern candidates、method maps 和 review reports。

它不是论文摘要器：核心目标是保留 source material，抽取可迁移推理模式，并让 source references 可 review。

VeryMath 的正式维护位置是 [AI4Math-Paper-Reading](https://github.com/VeryMath/AI4Math-Paper-Reading/tree/main/skills/paper-to-skill)。AI4Math-Skill-Library 同时收录此包；改进在 VeryMath 包维护，原个人仓库保留作历史参考。

SkillCard 现在记录数学依赖、独立检查、失败案例和跨问题复用。抽取分数只表示候选质量；入库还需要核对假设、独立数学论证、成功复用和失败边界。已有卡片缺少这些记录时，只能算未验证候选。可参考[流稳定性实际检查](examples/auto_research_trial/flow_stability_validation.md)。

## 适合什么任务

当你有这些输入或需求时使用：

- 需要变成结构化 method artifacts 的 `paper.pdf` 或 `paper.md`；
- 需要抽取的 proof patterns、theoretical-analysis routines 或 algorithmic methods；
- 需要综合成紧凑 method map 的多篇论文；
- 需要回指到转换后论文文本的 source-line references。

## 会产出什么

Agent 应保留原始论文，必要时创建 `paper.md`，抽取 SkillCandidates 和 SkillCards，并写带 source references 的 `report.md`。

## 安装

把下面这句话发给你的 coding agent：

```text
请帮我安装 `paper-to-skill` package，链接是：https://github.com/VeryMath/AI4Math-Paper-Reading.git，分支：main，子目录：skills/paper-to-skill。请读取 `.agent.md`，安装其中声明的 Skill entrypoint，验证 `$paper-to-skill` 可用，并告诉我是否需要重启 agent。
```

如果你已经有这个 skill 仓库的本地文件夹，把链接换成本地路径即可。clone、link、配置、reload/restart 检查和验证都交给 coding agent 处理。

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
