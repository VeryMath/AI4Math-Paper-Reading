# Reading Plan / 阅读计划

## Summary / 总览

中文：我合并了 `candidate_papers.json` 和 `innovation_candidates.json`，去重后共有 16 篇候选论文。阅读计划优先服务于你的画像：theory-heavy flow matching、geometric/constrained generative modeling、learned ODE sampler convergence、Euler discretization、TV/Wasserstein error analysis，以及后续 `paper-to-skill-extractor` 的 proof-pattern 抽取。

English: I merged `candidate_papers.json` and `innovation_candidates.json`; after deduplication there are 16 unique candidate papers. The plan prioritizes the research profile: theory-heavy flow matching, geometric/constrained generative modeling, learned ODE sampler convergence, Euler discretization, TV/Wasserstein error analysis, and downstream proof-pattern extraction with `paper-to-skill-extractor`.

## Must Read / 必读

1. `vES22INUKm` - An Error Analysis of Flow Matching for Deep Generative Modeling
   - 中文：Euclidean flow matching 的 W2 error-analysis 核心基线，适合先抽 learned velocity / Wasserstein convergence proof pattern。
   - English: Core Euclidean FM W2 error-analysis baseline; ideal for extracting learned-velocity and Wasserstein-convergence proof patterns.

2. `uqQPyWFDhY` - Error Bounds for Flow Matching Methods
   - 中文：通用 FM error-bound 框架，适合和种子论文的 proof decomposition 对齐。
   - English: General FM error-bound framework; useful for aligning with the seed papers' proof decompositions.

3. `2302.03660` - Flow Matching on General Geometries
   - 中文：RFM 方法源头，定义和定位必须读。
   - English: Foundational RFM method paper; must-read for definitions and positioning.

4. `VTaO5BXDxV` - Geometry-Grounded Flow Matching on Compact Manifolds
   - 中文：和 RFM TV seed 很接近，提供 compact manifold Wasserstein / end-to-end guarantee 视角。
   - English: Very close to the RFM TV seed; adds compact-manifold Wasserstein and end-to-end guarantee perspective.

5. `2604.06065` - Lipschitz regularity in Flow Matching and Diffusion Models
   - 中文：最强创新候选，直接针对 velocity regularity、terminal-time behavior 和 discretization rates。
   - English: Strongest innovation candidate; directly targets velocity regularity, terminal-time behavior, and discretization rates.

6. `openreview_vxq1OnaAMq` - Gauge Flow Matching
   - 中文：constrained-domain 路线的强竞争方法，可对比 mirror / reflection / gauge 三条路径。
   - English: Strong competing constrained-domain route; useful for comparing mirror, reflection, and gauge approaches.

## Should Read / 应读

1. `2310.01236` - Mirror Diffusion Models
   - 中文：mirror-map constrained generation 的关键背景。
   - English: Key background for mirror-map constrained generation.

2. `2405.16577` - Reflected Flow Matching
   - 中文：同样解决 constrained FM，但偏方法和比较。
   - English: Also targets constrained FM, but mainly useful for method comparison.

3. `qKKxzTucgy` - On the Convergence and Straightness of Rectified Flow
   - 中文：可能把 discretization error 重新解释为 path geometry / straightness 问题。
   - English: May reinterpret discretization error through path geometry or straightness.

4. `2305.11798` - The probability flow ODE is provably fast
   - 中文：相邻 deterministic generative ODE 理论，可借 proof technique。
   - English: Adjacent deterministic generative ODE theory; useful for proof-technique transfer.

5. `2601.02499` - Polynomial Convergence of Riemannian Diffusion Models
   - 中文：Riemannian diffusion 的 TV / curvature proof machinery 可迁移参考。
   - English: Riemannian diffusion TV/curvature proof machinery may transfer.

## Maybe Read / 可暂存

- `2202.02763` - Riemannian Score-Based Generative Modelling
- `2406.12816` - Neural Approximate Mirror Maps for Constrained Diffusion Models
- `JEn5B8JC5n` - Flow Matching Generalizes Through Discretization Bias
- `oBc4oWAlcs` - Sample Complexity of Flow Matching
- `KwGec9703J` - Wasserstein Gradient Flow Matching reinterpretation

中文：这些论文有背景或概念价值，但不是当前 proof-pattern workflow 的第一批核心对象。

English: These papers have background or conceptual value, but they are not first-batch core targets for the current proof-pattern workflow.

## Recommended Next Step / 下一步建议

中文：建议不要一次下载全部。先下载并转换前两篇 Euclidean FM error-analysis 论文：

English: I recommend not downloading everything at once. First download and convert the two Euclidean FM error-analysis papers:

```text
vES22INUKm
uqQPyWFDhY
```

中文：这样可以先验证 `paper-to-skill-extractor` 对 proof-heavy FM theory 的抽取质量。验证成功后，再处理 `VTaO5BXDxV`、`2604.06065` 和 `openreview_vxq1OnaAMq`。

English: This lets us test `paper-to-skill-extractor` on proof-heavy FM theory first. If the extraction quality is good, continue with `VTaO5BXDxV`, `2604.06065`, and `openreview_vxq1OnaAMq`.

## Checkpoint / 请确认

1. 中文：是否先下载并转换 `vES22INUKm` 和 `uqQPyWFDhY`？
   English: Should we first download and convert `vES22INUKm` and `uqQPyWFDhY`?
2. 中文：后续抽取 proof-pattern 时，是先抽 Euclidean FM error proof，还是先抽 geometric/Riemannian proof？
   English: For proof-pattern extraction, should we start with Euclidean FM error proofs or geometric/Riemannian proofs?
3. 中文：是否保留 `maybe_read`，还是先从本轮工作流排除？
   English: Should we keep the `maybe_read` papers in the workflow, or exclude them for now?
