# Math Paper Reading

面向数学论文精读、结构提取、定理依赖分析和文献笔记的 Skill。

论文原文用于核对作者的陈述、假设和引用。`<slug>_structure.json` 是可修正的阅读索引，可能存在遗漏或提取错误；结构化格式和图计算不能保证没有幻觉，也不能证明论文结论正确。

## 从哪里开始

安装时保留完整包目录，读取 [SKILL.md](SKILL.md)，再由 [agent_router.md](agent_router.md) 按任务加载模块。直接给出论文、目标定理或需要解释的段落即可，无需先生成整篇 JSON。

| 任务 | 模块 |
| --- | --- |
| 提取定义、定理、假设和引用位置 | [skill_base.md](skill_base.md) |
| 计算依赖关系、生成图和阅读路径 | [skill_pathway_proof.md](skill_pathway_proof.md) |
| 解释论文、展开推导、分析缺口 | [skill_paper_deep_read.md](skill_paper_deep_read.md) |
| 从概念和引用寻找文献 | [skill_literature_search.md](skill_literature_search.md) |
| 保存文献元数据、个人笔记和阅读状态 | [skill_reference_manager.md](skill_reference_manager.md) |

## 阅读与纠错

1. 明确用户要读整篇还是一个局部。已有 JSON 可以帮助定位；缺少 JSON 时也可直接读取所需原文。
2. 核对目标陈述的全部条件、量词和证明引用。提取的引文保留原文；意译、解释和补充推导分开呈现。
3. 对明确的提取错误，依据原文直接修正索引，说明原文位置及改正内容，并同步受影响的报告、反向引用和图。无需重新启动全部流程。
4. 原文疑似笔误、无法补齐的推导和未确认依赖保持显式未解决。Agent 提议的补充论证不能冒充作者原文或已完成证明。
5. 图中只用已确认的内部依赖计算度数和阅读次序；不确定边和外部引用另行标注。缺节点或环首先是待回查的问题。
6. 保存成果时沿用项目目录，保留用户笔记和编辑；明确哪些章节、陈述及依赖已经核对，哪些尚未核对。

## 使用示例

- “解释这篇论文的 Theorem 2，并核对它需要哪些假设。”
- “现有 JSON 把 Lemma 3 的依赖记错了，请回查原文并同步图。”
- “只读这一段证明，分开列出作者写出的步骤、你补充的推导和仍有疑问的步骤。”
- “根据这条引文找原始文献；先核实题名和版本，再更新我的笔记。”

包内 `examples/` 是既有案例，不是用户的文献库。案例的原始论文保留不改；个别核对结果不能代表整篇论文或整个 Skill 已被独立验证。

本次对现有案例的实际修改与原文位置见 [核对记录](examples/source-checks.md)：Gowers 的局部图已同步修正，Behrens 的空实体表保留为未完成抽取。

---

# Math Paper Reading — English

A Skill for reading mathematical papers, extracting theorem dependencies, constructing reading paths, and maintaining reference notes.

The paper is the source for what its authors state, assume, and cite. `<slug>_structure.json` is a correctable reading index and can contain omissions or extraction errors. Structured output and graph computation neither eliminate hallucinations nor establish mathematical correctness.

## Entry point

Keep the complete package together. Read [SKILL.md](SKILL.md), then use [agent_router.md](agent_router.md) to load the relevant module. A local question can be answered from its source passage without extracting a complete paper-wide JSON file first.

## Workflow

1. Identify the requested scope and locate the relevant source. Use an existing index to navigate when helpful.
2. Check all conditions and quantifiers in the target statement. Separate source quotations, explanations, additional derivations, and unresolved steps.
3. Correct an extraction error directly from its source, state the location and correction, and update the affected index, report, reverse references, and graph. No full restart or entity-lock procedure is required.
4. Preserve suspected source typos and incomplete arguments as unresolved issues. An Agent's proposed repair is not an author quotation or a verified proof.
5. Compute graph degrees and reading order from confirmed internal dependencies only. Display uncertain and external edges separately. A cycle or missing node prompts a source check.
6. Save results within the current project, retain user notes, and state the actual coverage and remaining unknowns.

Use the package modules linked above for extraction, graphs, deep reading, literature queries, and reference management. The bundled examples are reference material rather than user data, and selected checks do not constitute validation of a whole paper or of the Skill's general performance.

See the [source-check record](examples/source-checks.md) for the actual corrections to the existing examples and the limits of their checked scope.
