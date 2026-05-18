# Codex 项目说明文档：AI4Math Skill 仓库与 Paper-to-Skill 模块

## 0. 给 Codex 的总说明

你正在帮助我们开发一个数学科研 AI Skill 仓库中的核心模块。请不要把这个项目理解成普通的论文总结工具。我们的目标是建设一个可复用、可评测、可扩展的数学科研 Skill 仓库，并实现一个依托 Codex 从数学论文中挖掘 Skill 的工作流。

当前阶段的重要决策：

```text
暂时不依赖外部 LLM API。
第一版优先把 Codex 本身作为数学理解与 Skill 抽取执行器。
核心产物不是自动 API 调用，而是一组可复用、可组合的 Codex Skills。
当前主线已经从单篇 paper-to-skill-extractor 扩展为 Codex-native 的人机交互式自动科研工作流。
```

本说明文档分为三层：

1. 课题组整体目标；
2. 我个人负责的模块；
3. 需要你实现的 Codex Skill 优先 MVP。

请优先完成 Codex Skill MVP，不要一开始实现所有工程自动化功能。后续 Python pipeline 可以作为辅助工具逐步补上。

当前已经形成的主链路：

```text
seed papers
        ↓
seed-paper-profiler
        ↓
research_profile.json
        ↓
related-paper-retriever + innovation-paper-finder
        ↓
candidate_papers.json + innovation_candidates.json
        ↓
paper-triage-ranker
        ↓
reading_plan.json
        ↓
paper-pdf-downloader
        ↓
pdf-to-markdown-converter
        ↓
paper-to-skill-extractor
        ↓
single-paper SkillCards
        ↓
cross-paper-skill-synthesizer
        ↓
domain method map + merged SkillCards
```

当前已验证样例：

```text
outputs/auto_research_trial/
```

该样例已经跑通：

```text
研究画像 -> 相关/创新论文候选 -> 阅读计划 -> PDF 下载 -> PDF 转 Markdown
-> 单篇 proof_pattern Skill 抽取 -> 跨论文 Skill 合成
```

---

# 1. 课题组整体目标

我们课题组要建设一个面向数学科研的 AI Skill 仓库，暂定名称为：

```text
ai4math-skills
```

这个仓库不是简单收集 prompt，而是沉淀一批可被数学科研 Agent 调用的标准化能力单元。

整体目标是支持以下场景：

```text
数学论文阅读
数学工具调用
Lean4 / 形式化证明辅助
数值计算与优化
科研方法论自动化
从论文中自动挖掘新的 Skill
```

我们希望最终形成这样的闭环：

```text
数学论文 / 数学任务
        ↓
识别其中的证明、算法、建模、误差分析套路
        ↓
抽象成可复用 Skill
        ↓
写成标准 Skill Card
        ↓
进入 Skill 仓库
        ↓
后续 Agent 在新问题中自动调用这些 Skill
```

也就是说，整个项目的核心不是“让 AI 总结论文”，而是：

```text
让 AI 从论文中提炼可复用的数学科研方法。
```

---

# 2. Skill 仓库中的主要 Skill 类型

当前课题组关注的 Skill 类型包括但不限于：

## 2.1 数学论文阅读类

包括：

```text
论文内容结构分析
更好的论文解读
文献管理助手
相关文献检索
论文证明路径生成
引理 / 定理关系图构建
```

这些 Skill 用于帮助研究者理解论文结构、贡献、证明路线和相关文献脉络。

---

## 2.2 数学工具使用类

包括：

```text
线性规划 LP
混合整数规划 MILP
二阶锥规划 SOCP
半正定规划 SDP
自动建模
SageMath 使用
数学画图工具调用
论文 PDF 转 Markdown
```

这些 Skill 用于让 Agent 在需要计算、建模、可视化或文档转换时调用外部工具。

---

## 2.3 Lean4 相关类

包括：

```text
Infoview 报错的 AI 解读
Lean agent 调用
Lean 检索工具调用
```

这些 Skill 用于支持形式化证明、Lean 代码调试和 theorem search。

---

## 2.4 数值计算与优化基础算子类

包括：

```text
病态指数计算
精确线搜索
近端算子求值
非线性方程求根：二分法、牛顿法、割线法
矩阵计算：LU、Cholesky、SVD、CG、GMRES、特征值计算
预处理技术：Jacobi、ILU、代数多重网格、舒尔补 / 块预处理
逼近与微积分：样条插值、最小二乘、有限差分、高斯积分
ODE：RK4、BDF 刚性求解
PDE / 有限元：网格与空间、弱形式构建、组装与求解
理论诊断：Lyapunov 证明、收敛常数提取、KKT 最优性证书
```

这些 Skill 主要服务于数值计算、优化和 PDE 方向的 Agent 工具调用。

---

## 2.5 科研方法论 Skill

这是我们课题组非常看重的一类。它们不是简单工具，而是数学论文中反复出现的证明套路和理论分析套路。

包括：

```text
模式识别与转化 Skill
下降引理自动推演
势函数 / Lyapunov 构造
经典不等式自动放缩
误差分解骨架提取
裂项相消与全局收敛界
冯·诺依曼稳定性分析
Lax-Milgram 适定性验证
Céa 引理与 Galerkin 正交性
Aubin-Nitsche 对偶技巧
集中不等式自动选择与放缩
一致收敛与泛化界
Delta 方法与渐近正态性
信息论极小极大下界
```

这些 Skill 最适合由 Codex 阅读论文后进行抽象、归纳和结构化，因此也是我个人负责模块的核心来源。

---

## 2.6 人机交互式自动科研工作流 Skill

为了支持用户从少量感兴趣论文出发，逐步完成相关文献发现、创新点发现和 Skill 抽取，paper-to-skill 需要扩展为一组 Codex-native 的人机交互式科研工作流 Skills。

这个方向的关键不是自建检索系统，也不是把整个科研过程黑箱自动化。第一版应利用 Codex 本身可用的检索、阅读、判断和文件操作能力，并通过 Skill 固化：

```text
检索策略
筛选标准
输出 schema
下载边界
人工确认 checkpoint
Skill 抽取与跨论文综合流程
```

推荐工作流：

```text
seed papers
        ↓
seed-paper-profiler
        ↓
research_profile.json
        ↓
related-paper-retriever + innovation-paper-finder
        ↓
candidate_papers.json + innovation_candidates.json
        ↓
paper-triage-ranker
        ↓
reading_plan.json
        ↓
paper-pdf-downloader
        ↓
download selected open-access PDFs
        ↓
pdf-to-markdown-converter
        ↓
paper-to-skill-extractor
        ↓
single-paper SkillCards
        ↓
cross-paper-skill-synthesizer
        ↓
domain method map + merged SkillCards
```

需要新增或保留的 Skills：

```text
seed-paper-profiler
related-paper-retriever
innovation-paper-finder
paper-triage-ranker
paper-pdf-downloader
pdf-to-markdown-converter
paper-to-skill-extractor
cross-paper-skill-synthesizer
```

其中 `paper-to-skill-extractor` 仍然只负责单篇 `paper.md -> proof_pattern SkillCandidate / SkillCard`。不要把检索、排序、下载、跨论文综合职责塞进 extractor。

Skill 职责边界表：

| Skill | 输入 | 输出 | 负责 | 不负责 |
| --- | --- | --- | --- | --- |
| `seed-paper-profiler` | 种子论文、摘要、用户 notes | `research_profile.json` | 研究兴趣画像 | 检索和下载 |
| `related-paper-retriever` | `research_profile.json` | `candidate_papers.json` | 相关论文候选 | 全文下载、最终排序 |
| `innovation-paper-finder` | `research_profile.json` | `innovation_candidates.json` | 创新点/跨领域迁移候选 | 普通相关工作综述 |
| `paper-triage-ranker` | 候选论文列表 | `reading_plan.json` | 阅读优先级和 download_queue | 下载 PDF |
| `paper-pdf-downloader` | `reading_plan.json` 或确认的 paper IDs | `paper.pdf`, `metadata.json` | 下载 open-access PDF | PDF 转 Markdown、绕过 paywall |
| `pdf-to-markdown-converter` | 本地 `paper.pdf` | `paper.md`, `conversion_report.json` | PDF 预处理 | Skill 抽取 |
| `paper-to-skill-extractor` | 单篇 `paper.md` | `skill_candidates.json`, `skill_cards/*.yaml`, `report.md` | 单篇 proof_pattern 抽取 | 检索、下载、跨论文合成 |
| `cross-paper-skill-synthesizer` | 多篇 SkillCards | `domain_method_map.yaml`, merged SkillCards | 聚类、合并、泛化 | 重新阅读全部 PDF 或检索新论文 |

建议统一输出结构：

```text
outputs/<research_project_id>/
├── seed_papers/
├── research_profile.json
├── candidate_papers.json
├── innovation_candidates.json
├── reading_plan.json
├── papers/
│   └── <paper_id>/
│       ├── metadata.json
│       ├── paper.pdf
│       ├── paper.md
│       ├── mineru/
│       ├── conversion_report.json
│       └── notes.md
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

检索类 Skill 的 v0.1 边界：

```text
使用 Codex 可用的 search / browsing 能力。
Skill 只规定检索策略、来源优先级、判断标准和输出格式。
不实现自建搜索引擎、批量爬虫、数据库或外部 LLM API pipeline。
```

下载规则：

```text
检索阶段默认只记录元数据、URL、PDF 链接、摘要和推荐理由。
只有在用户确认 must_read / should_read 或明确要求下载后，才下载全文。
只下载 open-access PDF 或用户有权限访问的论文。
不要绕过 paywall。
必须记录 source_url 和 pdf_url。
下载职责由 `paper-pdf-downloader` 负责；Markdown 转换职责由 `pdf-to-markdown-converter` 负责。
必须保留原始 paper.pdf；转换后的 paper.md 才交给 paper-to-skill-extractor。
```

每一步都应包含人工确认点：

```text
Checkpoint 1: 用户确认 research_profile 是否代表真实兴趣。
Checkpoint 2: 用户确认候选论文范围是否合理。
Checkpoint 3: 用户确认 must_read / should_read 阅读计划。
Checkpoint 4: 用户确认哪些论文下载和转换。
Checkpoint 5: 用户审核单篇 SkillCandidate。
Checkpoint 6: 用户审核跨论文合成 Skill 是否可入库。
```

v0.1 做：

```text
Codex Skill workflow
检索说明
输出 schema
artifact templates
人工 checkpoint
open-access 下载规则
paper.md -> SkillCard
cross-paper synthesis
```

v0.1 不做：

```text
自建搜索引擎
数据库
Web UI
批量爬虫
绕过付费墙
Lean 自动验证
完整 benchmark
外部 LLM API pipeline
```

---

# 3. 我个人负责的任务

我负责的任务是：

```text
从论文中依托 Codex 挖掘 Skill 的机制
```

模块名称暂定为：

```text
paper-to-skill
```

中文名：

```text
论文到 Skill 的 Codex 辅助挖掘机制
```

核心目标：

```text
输入一篇数学论文，让 Codex 按固定流程抽取可复用、可评测、可入库的 Skill Card。
```

这不是普通论文总结器。

普通论文总结器做的是：

```text
论文 → 摘要 / 总结 / 贡献点
```

我要做的是：

```text
论文 → Codex 辅助识别可复用科研方法 → Skill Card → Skill 仓库
```

例如，论文中出现如下证明片段：

```text
By L-smoothness, we derive a one-step descent inequality.
Then we apply Young's inequality to bound the cross term.
Finally, summing over k gives an O(1/T) convergence rate.
```

普通总结会说：

```text
作者证明了算法具有 O(1/T) 收敛率。
```

但 paper-to-skill 应该挖掘出：

```text
Skill 1: 下降引理自动推演
Skill 2: Young 不等式放缩
Skill 3: 裂项相消与全局收敛界
```

---

# 4. 设计原则

## 4.1 必须保留完整 paper.md

数学论文结构解析不可能 100% 准确，因此不要把结构化 JSON 当成唯一真相。

系统必须保留完整 Markdown 原文：

```text
paper.md
```

它是 source of truth。

结构化结果只能作为弱索引：

```text
paper_index.json
```

其中字段应使用：

```json
{
  "type_guess": "proof",
  "confidence": 0.78
}
```

而不是过度自信地写：

```json
{
  "type": "proof"
}
```

---

## 4.2 结构化索引只是导航，不替代原文

推荐输出结构：

```text
outputs/<paper_id>/
├── paper.md
├── paper_index.json
├── conversion_report.json
├── selected_segments.json
├── skill_candidates.json
├── skill_cards/
│   ├── descent_lemma_auto_derivation.yaml
│   ├── young_inequality_relaxation.yaml
│   └── telescoping_convergence_bound.yaml
└── report.md
```

每个 Skill 候选都必须能回溯到原文位置：

```json
{
  "source": {
    "paper_md": "paper.md",
    "start_line": 248,
    "end_line": 316,
    "block_id": "block_0032"
  }
}
```

---

## 4.3 第一版只做 Proof Pattern Mining

MVP 不要一开始做全类型 Skill。

第一版只做：

```text
从 paper.md 中挖掘 proof_pattern 类 Skill
```

优先识别：

```text
下降引理
经典不等式放缩
裂项相消
误差分解
Lyapunov 函数
集中不等式
泛化界
Céa 引理
Aubin-Nitsche
Lax-Milgram
```

暂不做：

```text
OCR
复杂 PDF 版面恢复
未经用户确认的 arXiv / PDF 自动下载
工具调用执行
Lean 验证
完整 benchmark 自动生成
```

---

# 5. 总体 Pipeline

长期目标 pipeline：

```text
PDF / LaTeX / arXiv source / Markdown
        ↓
paper_to_markdown_with_index
        ↓
paper.md
paper_index.json
conversion_report.json
        ↓
segment_selector
        ↓
skill_candidate_miner
        ↓
skill_generalizer
        ↓
skill_scorer
        ↓
skill_deduplicator
        ↓
skill_card_generator
        ↓
skill_cards/
report.md
```

当前 MVP 不以 API 自动化为核心，而是采用 Codex-assisted workflow：

```text
paper.md
  ↓
Codex 读取全文并建立弱结构理解
  ↓
Codex 识别 theorem / lemma / proof / convergence / error analysis 等高价值片段
  ↓
Codex 判断片段中是否存在可复用 proof_pattern
  ↓
Codex 抽取 SkillCandidate
  ↓
Codex 去论文语境化并生成 SkillCard
  ↓
Codex 按质量标准标记 accepted_candidate / needs_review / rejected
  ↓
Codex 输出 skill_cards/*.yaml 与 report.md
```

后续如果有 API，再把这个 Codex 工作流迁移为 `llm_client` 和自动 pipeline。当前不要把 API 作为前置依赖。

---

# 6. 需要实现的工程模块

当前第一优先级是维护和完善 Codex Skill workflow，而不是把流程提前固化成完整 Python pipeline。

当前推荐仓库结构：

```text
paper-to-skill/
│
├── README.md
├── AGENTS.md
├── skills/
│   ├── seed-paper-profiler/
│   ├── related-paper-retriever/
│   ├── innovation-paper-finder/
│   ├── paper-triage-ranker/
│   ├── paper-pdf-downloader/
│   ├── pdf-to-markdown-converter/
│   ├── paper-to-skill-extractor/
│   └── cross-paper-skill-synthesizer/
│
├── examples/
│   ├── inputs/
│   │   └── example_paper.md
│   └── outputs/
│       └── example_paper/
│
└── docs/
    ├── codex_assisted_workflow.md
    └── future_python_pipeline.md
```

其中：

```text
paper-to-skill-extractor 是单篇 proof_pattern 抽取核心。
paper-pdf-downloader 和 pdf-to-markdown-converter 是独立预处理 Skill。
cross-paper-skill-synthesizer 是跨论文方法论地图和可入库 Skill 合成器。
```

Python 工程模块作为第二阶段，可在 Codex Skill workflow 跑通之后再实现。届时建议使用 Python、Pydantic 和 pytest。当前 Python 只作为下载、PDF 转换、验证等 helper scripts。

后续 Python pipeline 参考结构：

推荐仓库结构：

```text
paper-to-skill/
│
├── README.md
├── pyproject.toml
├── AGENTS.md
├── configs/
│   └── pipeline.yaml
│
├── src/
│   └── paper_to_skill/
│       ├── __init__.py
│       ├── main.py
│       │
│       ├── ingestion/
│       │   ├── markdown_loader.py
│       │   ├── latex_to_markdown.py          # v0.2
│       │   ├── pdf_to_markdown.py            # v0.2
│       │   └── cursor_context_adapter.py     # optional
│       │
│       ├── indexing/
│       │   ├── paper_indexer.py
│       │   └── block_detector.py
│       │
│       ├── selection/
│       │   └── segment_selector.py
│       │
│       ├── mining/
│       │   ├── skill_candidate_miner.py
│       │   ├── skill_generalizer.py
│       │   ├── skill_scorer.py
│       │   └── skill_deduplicator.py
│       │
│       ├── generation/
│       │   ├── skill_card_generator.py
│       │   └── report_generator.py
│       │
│       ├── schemas/
│       │   ├── paper_schema.py
│       │   └── skill_schema.py
│       │
│       └── utils/
│           ├── llm_client.py
│           ├── json_repair.py
│           └── line_utils.py
│
├── prompts/
│   ├── mine_skill_candidates.md
│   ├── generalize_skill.md
│   ├── score_skill.md
│   └── generate_skill_card.md
│
├── examples/
│   ├── inputs/
│   │   └── example_paper.md
│   └── outputs/
│       └── example_paper/
│
├── tests/
│   ├── test_indexer.py
│   ├── test_segment_selector.py
│   ├── test_skill_schema.py
│   └── test_skill_deduplicator.py
│
└── docs/
    ├── skill_ontology.md
    ├── pipeline_design.md
    └── evaluation.md
```

---

# 7. MVP 功能要求

## 7.1 输入

`paper-to-skill-extractor` 的 MVP 输入只需要支持：

```text
paper.md
```

用户可以额外指定重点片段，例如：

```text
请重点看第 3 节 convergence proof
请重点看 Lemma 2.1 到 Theorem 2.3
请重点抽取 error analysis / stability analysis 中的 proof_pattern
```

不要把 PDF、OCR、arXiv 下载、检索或跨论文综合职责放进 `paper-to-skill-extractor`。

完整 workflow v0.1 可以通过独立 Skill 完成这些前后置步骤：

```text
paper-pdf-downloader: open-access PDF download
pdf-to-markdown-converter: PDF -> paper.md
cross-paper-skill-synthesizer: multiple SkillCards -> merged SkillCards
```

---

## 7.2 输出

`paper-to-skill-extractor` MVP 输出：

```text
outputs/<paper_id>/
├── paper.md
├── skill_candidates.json
├── skill_cards/
└── report.md
```

其中 `paper_index.json` 和 `selected_segments.json` 是后续 Python 辅助工具的可选输出，不作为第一版前置要求。

---

## 7.3 CLI 命令

第一版不要求实现 CLI。Codex Skill 的典型调用方式是：

```text
请使用 paper-to-skill-extractor 读取 examples/inputs/example_paper.md，
抽取 proof_pattern Skill，并把结果写到 outputs/example_paper。
```

后续 Python pipeline 可以支持：

```bash
python -m paper_to_skill run examples/inputs/example_paper.md --out outputs/example_paper
python -m paper_to_skill index examples/inputs/example_paper.md --out outputs/example_paper
python -m paper_to_skill select outputs/example_paper/paper_index.json --out outputs/example_paper
python -m paper_to_skill mine outputs/example_paper/selected_segments.json --out outputs/example_paper
```

---

# 8. 数据结构要求

以下数据结构和模块要求主要用于约束未来 Python pipeline 的兼容格式。

当前 Phase 0-3 只需要将这些 schema 和规则写入 Codex Skill 的 `references/` 与 `assets/`，不要求实现 Python 代码。

## 8.1 PaperBlock

```python
class PaperBlock(BaseModel):
    block_id: str
    type_guess: str
    title: Optional[str] = None
    start_line: int
    end_line: int
    source_page: Optional[str] = None
    confidence: float
```

---

## 8.2 PaperIndex

```python
class PaperIndex(BaseModel):
    paper_md: str
    blocks: List[PaperBlock]
```

---

## 8.3 SelectedSegment

```python
class SelectedSegment(BaseModel):
    segment_id: str
    source_block_id: str
    type_guess: str
    section: Optional[str] = None
    start_line: int
    end_line: int
    priority: str
    reason: str
    text: str
```

---

## 8.4 SkillCandidate

```python
class SkillCandidate(BaseModel):
    skill_name: str
    zh_name: str
    skill_type: str
    source_span: str
    why_reusable: str
    input: List[str]
    output: List[str]
    assumptions: List[str]
    core_steps: List[str]
    trigger_keywords: List[str]
    limitations: List[str]
    reusability_score: int
    confidence: float
```

---

## 8.5 SkillQuality

```python
class SkillQuality(BaseModel):
    reusability: int
    clarity: int
    generality: int
    verifiability: int
    agent_callability: int
    mathematical_risk: int
    total_score: float
```

---

## 8.6 SkillCard

```python
class SkillSource(BaseModel):
    paper_title: Optional[str] = None
    paper_md: str
    source_blocks: List[str]
    start_line: int
    end_line: int

class SkillCard(BaseModel):
    name: str
    zh_name: str
    category: str
    status: str
    source: SkillSource
    description: str
    input: List[str]
    output: List[str]
    assumptions: List[str]
    core_steps: List[str]
    trigger_keywords: List[str]
    limitations: List[str]
    quality: SkillQuality
```

---

# 9. paper_indexer 要求

`paper_indexer` 负责从 `paper.md` 中建立弱结构索引。

它应该识别：

```text
Title
Abstract
Section
Subsection
Theorem
Lemma
Proposition
Corollary
Assumption
Proof
Algorithm
Equation-like blocks
Appendix
```

MVP 阶段可以使用规则和正则。

示例识别规则：

```text
以 "# " 开头：title
以 "## " 开头：section
包含 "Theorem 1" / "Theorem 2.1"：theorem
包含 "Lemma 1" / "Lemma 2.3"：lemma
包含 "Proof." 或 "Proof:"：proof
包含 "Algorithm 1"：algorithm
包含 "Assumption 1"：assumption
```

注意：识别结果是弱索引，请设置 confidence。

---

# 10. segment_selector 要求

`segment_selector` 从 paper_index.json 中选择高价值片段。

高优先级：

```text
proof
theorem
lemma
proposition
corollary
assumption
algorithm
sections containing:
- convergence
- proof
- error analysis
- stability
- generalization
- lower bound
- appendix proof
```

低优先级：

```text
introduction
related work
experiment
ablation
implementation
references
```

输出 `selected_segments.json`。

---

# 11. Codex Skill 抽取器要求

MVP 阶段不实现 API miner。由 Codex 按 `paper-to-skill-extractor` 的流程直接阅读论文片段并抽取 SkillCandidate。

Codex 抽取器必须执行以下判断：

```text
1. 这段是否是数学证明、理论推导、误差分析、稳定性分析、泛化界或下界证明；
2. 这段是否包含可迁移到其他论文或任务中的方法；
3. 该方法是否有明确输入、输出、适用条件和失败条件；
4. 该方法是否可以被 Agent 在未来任务中主动调用；
5. 该方法是否可以设计测试样例验证。
```

第一版重点识别以下 proof_pattern：

```text
下降引理自动推演
经典不等式放缩
裂项相消与全局收敛界
误差分解骨架提取
Lyapunov / 势函数构造
集中不等式选择与放缩
一致收敛与泛化界
Céa 引理与 Galerkin 正交性
Aubin-Nitsche 对偶技巧
Lax-Milgram 适定性验证
```

后续 Python pipeline 可以保留 mock miner 用于测试，但 mock miner 不是当前路线的核心产物。

---

# 12. skill_generalizer 要求

在当前 MVP 中，泛化由 Codex Skill 执行。`skill_generalizer` 是后续 Python pipeline 的可选模块。

Codex 泛化时必须：

要求：

```text
去掉 paper-specific 表述
保留必要数学假设
明确输入、输出、适用条件、失败条件
```

示例：

```text
For Algorithm 1 under Assumption 2
```

应泛化为：

```text
For a gradient-like iterative algorithm under smoothness assumptions
```

---

# 13. skill_scorer 要求

实现如下评分维度：

```text
reusability
clarity
generality
verifiability
agent_callability
mathematical_risk
```

评分范围 1-5。

总分公式：

```text
quality_score =
0.25 * reusability
+ 0.20 * clarity
+ 0.20 * generality
+ 0.15 * verifiability
+ 0.15 * agent_callability
- 0.05 * mathematical_risk
```

入库建议：

```text
quality_score >= 4.0       accepted_candidate
3.0 <= quality_score < 4.0  needs_review
quality_score < 3.0         rejected
```

---

# 14. skill_deduplicator 要求

去重逻辑：

如果两个 SkillCandidate 的以下字段高度相似，则合并：

```text
skill_name
skill_type
input
output
core_steps
trigger_keywords
```

合并时保留多个 evidence source。

---

# 15. skill_card_generator 要求

每个高质量 Skill 输出一个 YAML 文件：

```text
skill_cards/<skill_name>.yaml
```

示例：

```yaml
name: descent_lemma_auto_derivation
zh_name: 下降引理自动推演
category: proof_pattern
status: accepted_candidate

source:
  paper_title: null
  paper_md: paper.md
  source_blocks:
    - block_0032
  start_line: 248
  end_line: 316

description: >
  给定 L-smooth 目标函数和梯度型迭代格式，自动推导单步下降不等式，
  为后续收敛率证明提供基础。

input:
  - objective_function
  - iteration_rule
  - smoothness_assumption
  - step_size

output:
  - one_step_descent_inequality
  - descent_condition
  - proof_skeleton

assumptions:
  - objective is differentiable
  - objective is L-smooth
  - step size satisfies required upper bound

core_steps:
  - apply smoothness upper bound
  - substitute iteration rule
  - simplify inner product term
  - collect gradient norm terms
  - derive step-size condition

trigger_keywords:
  - L-smooth
  - gradient descent
  - one-step descent
  - convergence proof
  - smooth optimization

limitations:
  - does not directly handle nonsmooth regularizers
  - stochastic variants require additional expectation bounds
  - step-size condition must be checked

quality:
  reusability: 5
  clarity: 5
  generality: 4
  verifiability: 5
  agent_callability: 5
  mathematical_risk: 2
  total_score: 4.65
```

---

# 16. report_generator 要求

每次运行生成：

```text
report.md
```

格式：

```markdown
# Paper-to-Skill Report

## Paper Information

- Input:
- Output directory:
- Number of detected blocks:
- Number of selected segments:

## Extracted Skill Candidates

| Skill | Type | Score | Source | Status |
|---|---|---:|---|---|

## High Confidence Skills

## Needs Review

## Rejected Candidates

## Notes
```

---

# 17. Codex Skill 资源文件要求

第一版请不要把这些内容放在 `prompts/` 下作为 API prompt，而是放进 Codex Skill 的 `references/` 和 `assets/` 中。

推荐文件：

```text
skills/paper-to-skill-extractor/
├── SKILL.md
├── references/
│   ├── extraction_protocol.md
│   ├── proof_pattern_taxonomy.md
│   ├── quality_rubric.md
│   └── schemas.md
└── assets/
    ├── skill_candidate_template.yaml
    ├── skill_card_template.yaml
    └── report_template.md
```

## 17.1 extraction_protocol.md

```text
你是一个数学科研 Skill 挖掘器。

你的任务不是总结论文，而是从论文片段中抽取可以迁移到其他数学科研任务中的 Skill。

请只抽取满足以下条件的方法：
1. 可复用：可以用于其他论文或问题；
2. 有明确输入和输出；
3. 有明确适用条件；
4. 可以被 Agent 调用；
5. 可以设计测试样例验证。

请不要抽取：
1. 只属于本文模型的特殊结论；
2. 纯背景介绍；
3. 没有明确操作步骤的宏观观点；
4. 实验数值结果。

请按结构化 JSON 或 YAML 输出：

[
  {
    "skill_name": "",
    "zh_name": "",
    "skill_type": "proof_pattern | algorithm_pattern | modeling_pattern | tool_usage_pattern | evaluation_pattern",
    "source_span": "",
    "why_reusable": "",
    "input": [],
    "output": [],
    "assumptions": [],
    "core_steps": [],
    "trigger_keywords": [],
    "limitations": [],
    "reusability_score": 1,
    "confidence": 0.0
  }
]

输入可以是完整 paper.md，也可以是用户指定的论文片段。
必须保留 source line references。
```

---

## 17.2 proof_pattern_taxonomy.md

应收录第一版重点抽取的 proof_pattern，包括但不限于：

```text
descent_lemma_auto_derivation
inequality_relaxation
telescoping_convergence_bound
error_decomposition_skeleton
lyapunov_potential_construction
concentration_bound_selection
uniform_convergence_bound
cea_galerkin_orthogonality
aubin_nitsche_duality
lax_milgram_wellposedness
```

每一类应说明：

```text
触发线索
适用条件
输入
输出
典型步骤
常见风险
不要误抽取的情况
```

---

## 17.3 quality_rubric.md

```text
你是一个数学 Skill 质量评估器。

请根据以下维度对 Skill 进行评分，每项 1-5 分：

1. reusability: 能否在其他问题中复用；
2. clarity: 输入输出是否清楚；
3. generality: 是否摆脱原论文特定语境；
4. verifiability: 是否容易设计测试样例；
5. agent_callability: Agent 是否容易判断何时调用；
6. mathematical_risk: 是否容易因遗漏条件导致错误，1 表示风险低，5 表示风险高。

建议：

quality_score >= 4.0       accepted_candidate
3.0 <= quality_score < 4.0  needs_review
quality_score < 3.0         rejected
```

---

## 17.4 schemas.md

```text
记录 SkillCandidate、SkillQuality、SkillCard 的字段要求。
字段定义可以沿用第 8 节。
```

---

# 18. 测试要求

当前 Codex Skill MVP 的测试方式优先采用示例驱动验证，不要求一开始写 pytest。

必须验证：

```text
1. Codex 能读取 example_paper.md；
2. Codex 能从示例 proof 中抽取至少 3 个 proof_pattern；
3. 每个 SkillCandidate 都有 source line references；
4. 每个 SkillCard 都符合模板；
5. report.md 能说明 accepted / needs_review / rejected；
6. Codex 不把论文具体结论误当成 Skill；
7. Codex 不抽取纯背景介绍、实验结果或 related work。
```

后续 Python pipeline 阶段再补 pytest。

建议 pytest 包含：

至少包含：

```text
test_indexer.py
test_segment_selector.py
test_skill_schema.py
test_skill_deduplicator.py
test_end_to_end_mock_pipeline.py
```

测试应验证：

```text
1. paper.md 能被加载；
2. theorem / lemma / proof 能被识别为 PaperBlock；
3. proof block 能被 segment_selector 选中；
4. mock miner 能识别 descent_lemma / inequality / telescoping；
5. SkillCandidate 能通过 Pydantic schema 校验；
6. skill_card_generator 能生成 YAML；
7. end-to-end pipeline 能生成 report.md。
```

---

# 19. 示例 paper.md

请在 `examples/inputs/example_paper.md` 中放入一个最小示例：

```markdown
# Example Optimization Paper

## Abstract

We study a simple gradient descent method for smooth optimization.

## 1 Introduction

This is a toy paper.

## 2 Convergence Analysis

### Theorem 2.1

Assume that f is L-smooth and bounded below. Let x_{k+1} = x_k - eta grad f(x_k), where 0 < eta <= 1/L. Then the method achieves an O(1/T) convergence rate.

### Proof

By L-smoothness of f, we have
f(x_{k+1}) <= f(x_k) + <grad f(x_k), x_{k+1}-x_k> + L/2 ||x_{k+1}-x_k||^2.

Substituting x_{k+1}=x_k-eta grad f(x_k), we obtain
f(x_{k+1}) <= f(x_k) - eta(1-L eta/2)||grad f(x_k)||^2.

Using Young's inequality, we can bound the cross term in the stochastic variant.

Summing over k=0,...,T-1 gives the desired O(1/T) rate.
```

---

# 20. AGENTS.md 要求

请创建一个 `AGENTS.md`，用于告诉 Codex 本仓库的长期规则。

内容应包括：

```markdown
# AGENTS.md

## Project Goal

This repository implements a Codex-assisted paper-to-skill workflow for an AI4Math skill library.

The goal is not to summarize papers, but to extract reusable mathematical research skills from papers.

## MVP Scope

Prioritize the Codex Skill at `skills/paper-to-skill-extractor`.

Only support Markdown input and `proof_pattern` mining in v0.1. The extractor does not retrieve papers, download PDFs, convert PDFs, rank candidates, or synthesize across papers.

The current MVP does not require external LLM APIs. Codex itself is the extraction engine.

PDF download, PDF-to-Markdown conversion, and cross-paper synthesis may exist as separate Codex Skills. Keep those responsibilities outside `paper-to-skill-extractor`.

Do not implement OCR, Lean verification, Web UI, database storage, or full benchmark generation in v0.1.

## Source of Truth

Always preserve the full `paper.md`. Structured files are weak indexes, reports, or generated artifacts, not replacements for the original paper.

Every extracted skill must include source line references back to `paper.md`.

## Engineering Rules

- Encode the extraction workflow as a Codex Skill first.
- Keep schemas and templates explicit.
- Keep future Python automation compatible with the Skill workflow.
- If Python modules are later added, use Pydantic for schemas and pytest for tests.
- Do not silently drop source text.
- Prefer small composable modules and deterministic output formats.

## Done Means

A task is done only when:
- the Codex Skill workflow is written or updated;
- the example paper can be processed by Codex end-to-end;
- generated outputs match the expected schema.
- extracted skills include source evidence and review status.
```

---

# 21. 开发阶段计划

## Phase 0: Codex Skill 初始化

完成：

```text
README.md
AGENTS.md
skills/paper-to-skill-extractor/SKILL.md
skills/paper-to-skill-extractor/references/
skills/paper-to-skill-extractor/assets/
examples folder
```

验收：

```text
Codex 能识别什么时候应该使用 paper-to-skill-extractor。
Skill 文件结构符合 Codex Skill 规范。
```

---

## Phase 1: 抽取协议与模板

完成：

```text
extraction_protocol.md
proof_pattern_taxonomy.md
quality_rubric.md
schemas.md
skill_candidate_template.yaml
skill_card_template.yaml
report_template.md
```

验收：

```text
Codex 能根据协议区分“论文结论”和“可复用 Skill”。
Codex 能按模板输出 SkillCandidate 和 SkillCard。
```

---

## Phase 2: 示例论文与人工验证

完成：

```text
examples/inputs/example_paper.md
outputs/example_paper/skill_candidates.json
outputs/example_paper/skill_cards/*.yaml
outputs/example_paper/report.md
```

验收：

```text
能从示例 proof 中抽取：
- descent_lemma_auto_derivation
- inequality_relaxation
- telescoping_convergence_bound
所有 Skill 都有 paper.md 行号证据。
```

---

## Phase 3: Skill 迭代与边界校准

完成：

```text
补充反例
补充不要抽取的情况
补充 mathematical_risk 说明
补充 needs_review 标准
```

验收：

```text
Codex 不抽取纯背景、实验结果、related work 或论文特有结论。
Codex 对条件不完整的 Skill 标记 needs_review。
```

---

## Phase 4: 可选 Python 骨架

完成：

```text
pyproject.toml
src package
tests folder
schemas
markdown_loader
line_utils
```

验收：

```text
pytest 能运行。
example_paper.md 能被加载并保留行号。
```

---

## Phase 5: 可选 Paper Indexer / Segment Selector

完成：

```text
paper_indexer
block_detector
segment_selector
```

验收：

```text
能识别 title / section / theorem / proof。
能生成 paper_index.json 和 selected_segments.json。
```

---

## Phase 6: 可选自动化 Pipeline

完成：

```text
skill_candidate_miner
skill_generalizer
skill_scorer
skill_deduplicator
skill_card_generator
report_generator
```

验收：

```text
自动 pipeline 与 Codex Skill 产物格式兼容。
没有 API 时仍可用 mock mode 或 Codex-assisted mode。
```

---

# 22. 不要做的事情

MVP 阶段请不要做：

```text
OCR
扫描版 PDF 解析
复杂数学公式 OCR
未经用户确认的 arXiv / PDF 自动下载
LaTeX source 解析
Lean4 验证
真实 LLM API 强依赖
Web UI
数据库
多用户系统
完整 benchmark 平台
```

这些都可以后续做。

---

# 23. 最终验收标准

`paper-to-skill-extractor` MVP 完成时，应满足：

```text
1. 存在可被 Codex 调用的 paper-to-skill-extractor Skill；
2. Skill 明确说明：目标不是总结论文，而是抽取可复用数学科研 Skill；
3. example_paper.md 可以被 Codex 按 Skill 流程处理；
4. paper.md 被完整保留；
5. skill_candidates.json 至少包含 3 个候选 Skill；
6. skill_cards/ 下至少生成 3 个 YAML；
7. report.md 总结提取结果、质量分数和 review 状态；
8. 所有 Skill 都能回溯到 paper.md 的行号；
9. Codex 不把论文特有结论、背景介绍或实验结果误抽成 Skill；
10. 后续 Python pipeline 可以复用同一套 schema、模板和质量标准。
```

完整人机交互式自动科研 workflow v0.1 还应满足：

```text
1. 能从少量 seed papers 生成 research_profile.json；
2. 能基于画像生成 candidate_papers.json 与 innovation_candidates.json；
3. 能生成 reading_plan.json，并区分 must_read / should_read / maybe_read / skip；
4. 下载只发生在用户确认之后，且只下载 open-access 或用户提供的 PDF；
5. 每个下载结果保留 metadata.json、paper.pdf、source_url、pdf_url；
6. PDF 转 Markdown 后保留 paper.md 与 conversion_report.json；
7. 单篇 paper.md 能产出 proof_pattern SkillCandidates 与 SkillCards；
8. 多篇 SkillCards 能合成为 domain_method_map.yaml 和 merged SkillCards；
9. 每个阶段都有中英文报告或说明，便于人工确认；
10. 每个合成 Skill 保留来源 paper.md 路径和行号证据。
```

---

# 24. 你作为 Codex 的优先任务

如果仓库从零开始，请先完成 extractor MVP；如果 extractor 已存在，则优先维护完整 Skill chain 与示例输出。

从零开始时：

```text
1. 创建 AGENTS.md；
2. 创建 skills/paper-to-skill-extractor/SKILL.md；
3. 创建 Skill 的 references：
   - extraction_protocol.md
   - proof_pattern_taxonomy.md
   - quality_rubric.md
   - schemas.md
4. 创建 Skill 的 assets：
   - skill_candidate_template.yaml
   - skill_card_template.yaml
   - report_template.md
5. 创建 examples/inputs/example_paper.md；
6. 用 Codex 按该 Skill 处理 example_paper.md；
7. 生成 outputs/example_paper/ 下的 skill_candidates.json、skill_cards/*.yaml 和 report.md；
8. 检查每个 Skill 是否有 source line references。
```

当前仓库已有 extractor 和自动科研 Skill chain 时，优先做：

```text
1. 检查 README.md 是否说明完整 workflow；
2. 检查每个 Skill 的 SKILL.md 是否职责清晰、边界明确；
3. 使用 outputs/auto_research_trial 作为端到端样例；
4. 验证 research_profile -> retrieval -> triage -> download -> pdf-to-md -> extraction -> synthesis 的产物结构；
5. 更新 brief、README、examples，让未来 Codex 能从当前状态继续。
```
