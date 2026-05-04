# Related Paper Retrieval Report / 相关论文检索报告

## Scope / 范围

中文：本轮基于 `research_profile.json` 检索理论型 flow matching、Riemannian / constrained generative modeling、learned ODE sampler convergence、Euler discretization 和 TV/Wasserstein error analysis。没有下载 PDF，只记录开放 PDF 链接。

English: This pass searched for theory-heavy flow matching, Riemannian/constrained generative modeling, learned ODE sampler convergence, Euler discretization, and TV/Wasserstein error analysis. No PDFs were downloaded; open PDF links were recorded only.

## Strong Related Papers / 强相关论文

1. `2302.03660` Flow Matching on General Geometries
   - 中文：RFM 原始方法论文，必须读。
   - English: Foundational RFM method paper; must-read.
2. `2405.16577` Reflected Flow Matching
   - 中文：constrained-domain FM 直接邻近方法。
   - English: Direct neighboring method for constrained-domain FM.
3. `openreview_vxq1OnaAMq` Gauge Flow Matching
   - 中文：用 gauge mapping 替代 mirror/reflection 的强相关方法。
   - English: Strong related method using gauge mappings instead of mirror/reflection.
4. `vES22INUKm` An Error Analysis of Flow Matching for Deep Generative Modeling
   - 中文：Euclidean FM 的端到端 W2 error analysis。
   - English: End-to-end W2 error analysis for Euclidean FM.
5. `VTaO5BXDxV` Geometry-Grounded Flow Matching on Compact Manifolds
   - 中文：RFM compact manifold Wasserstein 保证，和种子 TV paper 很近。
   - English: Compact-manifold RFM Wasserstein guarantees, close to the seed TV paper.

## Background Papers / 背景论文

- `2310.01236` Mirror Diffusion Models for Constrained and Watermarked Generation.
- `2202.02763` Riemannian Score-Based Generative Modelling.
- `2601.02499` Polynomial Convergence of Riemannian Diffusion Models.
- `2305.11798` The probability flow ODE is provably fast.

## Coverage Gaps / 覆盖缺口

中文：本轮不是完整 citation graph 展开。下一轮如果要更系统，可以从 `Flow Matching on General Geometries`、`Error Bounds for Flow Matching Methods`、`Mirror Diffusion Models` 和两篇种子论文的 references/citations 向外扩展。

English: This was not a full citation-graph expansion. A more systematic next pass should expand references and citations from `Flow Matching on General Geometries`, `Error Bounds for Flow Matching Methods`, `Mirror Diffusion Models`, and the two seed papers.

## Checkpoint / 请确认

中文：建议下一步直接跑 `paper-triage-ranker`，把这些候选分成 `must_read / should_read / maybe_read / skip`。

English: I recommend running `paper-triage-ranker` next to split these candidates into `must_read / should_read / maybe_read / skip`.
