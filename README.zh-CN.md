<div align="center">

# AI4Math · 论文阅读

面向数学论文精读、证明依赖拆解与 paper-to-skill 提取的 AI4Math 技能集合。

[English](README.md) · [技能包](#技能包) · [快速开始](#快速开始) · [安全边界](#安全边界)

![version](https://img.shields.io/badge/version-0.1.0-blue)
![skills](https://img.shields.io/badge/skills-2-2ea44f)
![license](https://img.shields.io/badge/license-MIT-green)

</div>

## 这个仓库是什么

这个仓库是 AI4Math 论文阅读方向的技能入口。它不是一个巨大的单体 Agent，而是把不同工作流拆成独立技能包：每个包都有自己的 README、`SKILL.md` 和必要的路由文件。

根 README 负责说明地图；真正执行任务时，请进入对应的 `skills/` 子目录。

## 技能包

| 包 | 适用任务 | 入口 |
| --- | --- | --- |
| [`paper-to-skill`](skills/paper-to-skill/) | 运行完整 paper-to-skill 工作流：PDF 预处理、论文筛选、证明模式抽取和跨论文综合。 | [`README`](skills/paper-to-skill/README.md) · [`SKILL`](skills/paper-to-skill/SKILL.md) |
| [`math-paper-reading`](skills/math-paper-reading/) | 深度阅读论文、提取定理依赖、生成证明路径、维护本地文献笔记。 | [`README`](skills/math-paper-reading/README.md) · [`SKILL`](skills/math-paper-reading/SKILL.md) · [`router`](skills/math-paper-reading/agent_router.md) |

## 快速开始

克隆仓库并选择技能包：

```bash
git clone https://github.com/VeryMath/AI4Math-Paper-Reading.git
cd AI4Math-Paper-Reading
```

如果目标是从论文中提取可复用技能，请从这里开始：

```text
skills/paper-to-skill/SKILL.md
```

如果目标是结构化精读论文，请从这里开始：

```text
skills/math-paper-reading/agent_router.md
```

## 仓库结构

```text
AI4Math-Paper-Reading/
├── README.md
├── README.zh-CN.md
├── SKILL.md
└── skills/
    ├── paper-to-skill/
    └── math-paper-reading/
```

包内 examples 只作为公开示例。由私有论文生成的报告、JSON、笔记和数据库不要提交，除非已经明确脱敏并适合公开发布。

## 验证

这个仓库没有根级构建步骤。修改技能包后，请检查 `SKILL.md`、README 链接和包内说明；如果使用 Codex 本地 skill validator，请对变更的包目录运行验证。

## 安全边界

不要提交私有论文、未公开笔记、带个人标注的本地数据库、API key、`.env` 文件或生成缓存。公开示例应尽量小、来源清楚，并确认可以再分发。
