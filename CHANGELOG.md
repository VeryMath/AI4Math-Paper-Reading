# 更新日志 / Changelog

## Unreleased — 2026-10-22

### 改动 / Changes

- 为 `paper-to-skill-extractor` 和 `cross-paper-skill-synthesizer` 的 SkillCard 增加数学依赖、独立验证、失败案例、跨问题复用和晋级状态，并更新模板、提取与合并说明。
  Add mathematical dependencies, independent verification, failure cases, cross-problem reuse, and promotion status to SkillCards and their workflows.
- 区分抽取评分、数学核查和可入库结论；合并时明确处理假设、证明路线、结论范围和来源冲突。旧卡缺少记录时视为未验证。
  Separate extraction quality from mathematical verification and library readiness; require explicit handling of merge conflicts and missing evidence.
- 按原有加权公式修正 6 张单篇卡的总分，保留原分项评分及数学验证状态。
  Correct six score totals arithmetically without changing component scores or mathematical status.
- 同步 3.9 分高斯平滑卡及报告的抽取复核状态；为五张单来源合成卡补齐来源评分并注明未重新评分，数学验证和晋级状态保持不变。
  Align the 3.9-score card and report with the review threshold; preserve source scores explicitly in five single-source synthesis cards without implying new verification.
- 同步两份候选索引的分数，保留高斯平滑的有界支撑条件，以及经验过程分解的样本独立性和条件化要求。
  Synchronize candidate scores and retain the source support, independence, and conditioning requirements in synthesized cards and the method map.

### 数学结果 / Mathematical results

- 流稳定性合成卡补充独立积分 Gronwall 推导，明确共同初始化、正确路径分布、有限二阶矩、可积 Lipschitz 常数和时间长度因子。这里的独立指另作论证，尚无独立研究者复核或形式化证明。
  Derive the continuous-flow bound separately and state its assumptions and time factor; this is a separate argument, not an independent human review or formal proof.
- 完成 3 个新 ODE 问题的精确解复用及 4 种失败边界检查；实际程序的 9 项比较全部符合预期，包含错误推广的拒绝和修正后的比较。见[数学检查与运行记录](skills/paper-to-skill/examples/auto_research_trial/flow_stability_validation.md)。
  All nine exact-ODE comparisons matched expectations, covering three reuse problems and four failure boundaries.
- 13 张示例卡中，仅该流稳定性卡在已检查的连续流结论范围内为 `ready_for_library`；其余 12 张保留 `candidate`。本次未重新转换 PDF，也未测量 Agent 使用收益。
  One of thirteen example cards is ready within its verified scope; twelve remain candidates. PDF conversion and agent benefit were not evaluated in this update.

### 数学论文精读 / Mathematical paper reading

- `math-paper-reading` 改为按原文核对作者陈述，JSON 只作可纠正索引；局部阅读、检索和笔记不再要求先生成整篇结构。
  Treat extracted JSON as a correctable index and allow source-based local reading, queries, and notes without a full-paper extraction prerequisite.
- 删除实体锁定与强制重走阶段的要求；区分原文、解释、Agent 补充推导和未完成步骤。原文纠错后同步索引、报告和依赖图，不把文件自洽当数学证明。
  Separate source quotations from explanations and additional derivations, and propagate source-supported corrections without entity locks or workflow restarts.
- Gowers 示例逐项核对 15 个既有实体并补入 2 个遗漏结果，修正条件和直接依赖，同步 17 节点、18 条确认边的图。Behrens 示例核对六项主结果，保留未完成的实体抽取状态。
  Check the existing local sources, update the selected Gowers graph, and explicitly retain Behrens as a partial extraction.
- 原始 TeX 不改；原文疑似笔误与抽取错误分开记录。外部文献、出版信息和整篇数学证明未独立核验，未新增 CI 或测试依赖。详见[原文核对记录](skills/math-paper-reading/examples/source-checks.md)。
  Preserve the original TeX and distinguish suspected source errors from extraction mistakes. External works and full proofs remain outside the checked scope.

### 发布状态 / Release status

- 本次拟提交 Skill 流程、卡片记录及数学案例，不包含单独准备中的新 CI 工作流；远端 Actions 尚未运行。
  The proposed update covers Skill workflows, card records, and mathematical examples. The separately prepared CI workflow is excluded; remote Actions has not run.
- 本节为未发布改动，不对应新版本号或标签。
  These changes are unreleased; no new version or tag is assigned.
