<div align="center">

# AI4Math · 论文阅读

面向数学论文精读、证明依赖拆解与 paper-to-skill 提取的 AI4Math 技能集合。

[English](README.md) · [贡献者](CONTRIBUTORS.md) · [技能包](#技能包) · [安装](#安装) · [快速开始](#快速开始) · [安全边界](#安全边界)

![version](https://img.shields.io/badge/version-0.1.0-blue)
![skills](https://img.shields.io/badge/skills-4-2ea44f)
![license](https://img.shields.io/badge/license-MIT-green)

</div>

<p align="center">
  如果这个项目对你有帮助，欢迎为仓库点 Star ⭐
  <a href="https://github.com/VeryMath/AI4Math-Paper-Reading"><img alt="GitHub Stars" src="https://img.shields.io/github/stars/VeryMath/AI4Math-Paper-Reading?style=social"></a>
</p>

## 这个仓库是什么

这个仓库是 AI4Math 论文阅读方向的技能入口。它不是一个巨大的单体 Agent，而是把不同工作流拆成独立技能包：每个包都有自己的 README、`SKILL.md` 和必要的路由文件。

根 README 负责说明地图；真正执行任务时，请进入对应的 `skills/` 子目录。

## 技能包

| 包 | 适用任务 | 入口 |
| --- | --- | --- |
| [`paper-to-skill`](skills/paper-to-skill/) | 运行完整 paper-to-skill 工作流：PDF 预处理、论文筛选、证明模式抽取和跨论文综合。 | [`README`](skills/paper-to-skill/README.md) · [`SKILL`](skills/paper-to-skill/SKILL.md) |
| [`math-paper-reading`](skills/math-paper-reading/) | 深度阅读论文、提取定理依赖、生成证明路径、维护本地文献笔记。 | [`README`](skills/math-paper-reading/README.md) · [`SKILL`](skills/math-paper-reading/SKILL.md) · [`router`](skills/math-paper-reading/agent_router.md) |
| [`after-ocr`](skills/after-ocr/) | 通篇审校并修复公式密集型 OCR Markdown，保留覆盖记录和多轮日志。 | [`README`](skills/after-ocr/README.md) · [`SKILL`](skills/after-ocr/SKILL.md) |
| [`graph-theory-paper-reading`](skills/graph-theory-paper-reading/) | 深度阅读图论论文并生成结构化 LaTeX 报告和证明树。 | [`README`](skills/graph-theory-paper-reading/README.md) · [`SKILL`](skills/graph-theory-paper-reading/SKILL.md) |

## 安装

推荐方式是 AI 自动安装：让你的 coding agent 自己 clone 或更新仓库、读取 Skill 说明、安装入口并验证 discovery。

```text
请帮我安装这些 AI4Math Skills。

仓库：https://github.com/VeryMath/AI4Math-Paper-Reading.git
分支：main
Skill 路径：
- skills/paper-to-skill
- skills/math-paper-reading
- skills/after-ocr
- skills/graph-theory-paper-reading

请执行：
1. 本地 clone 或更新仓库。
2. 读取 README.md、SKILL.md、AGENTS.md（如果存在）以及每个目标 Skill 入口。
3. 如果当前环境支持本地 Skill discovery，把每个包含 SKILL.md 的目录链接到本地 skills 目录。
4. 如果某个 Skill 依赖相邻的共享支持目录，请保留这些 sibling 目录。
5. 验证安装后的 Skills 是否可被发现。
6. 告诉我安装路径、是否需要重启 agent，并给我一个测试 prompt。
```

Codex 风格本地 discovery 的手工 fallback：

```bash
git clone https://github.com/VeryMath/AI4Math-Paper-Reading.git
cd AI4Math-Paper-Reading
mkdir -p ~/.codex/skills
ln -s "$PWD/skills/paper-to-skill" ~/.codex/skills/paper-to-skill
ln -s "$PWD/skills/math-paper-reading" ~/.codex/skills/math-paper-reading
ln -s "$PWD/skills/after-ocr" ~/.codex/skills/after-ocr
ln -s "$PWD/skills/graph-theory-paper-reading" ~/.codex/skills/graph-theory-paper-reading
```

如果你的 agent 使用别的本地 Skill 目录，把 `~/.codex/skills` 替换成对应配置路径。

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

OCR 审校或图论专项阅读从这里开始：

```text
skills/after-ocr/SKILL.md
skills/graph-theory-paper-reading/SKILL.md
```

## 仓库结构

```text
AI4Math-Paper-Reading/
├── README.md
├── README.zh-CN.md
├── SKILL.md
└── skills/
    ├── paper-to-skill/
    ├── math-paper-reading/
    ├── after-ocr/
    └── graph-theory-paper-reading/
```

包内 examples 只作为公开示例。由私有论文生成的报告、JSON、笔记和数据库不要提交，除非已经明确脱敏并适合公开发布。

## 验证

运行仓库测试和变更包自己的测试：

```bash
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s skills/after-ocr/tests -v
```

如果使用 Codex 本地 skill validator，请对每个变更包运行验证。

## 安全边界

不要提交私有论文、未公开笔记、带个人标注的本地数据库、API key、`.env` 文件或生成缓存。公开示例应尽量小、来源清楚，并确认可以再分发。
