# Seed Paper Profile Review / 种子论文画像确认

## Inferred Direction / 推断方向

中文：

```text
这两篇种子论文共同指向一个理论型方向：
几何或约束域上的 flow matching，
在 learned velocity field、Euler discretization、early stopping、
geometry/tail regularity assumptions 下建立非渐近采样保证。
```

English:

```text
The two seed papers point to a theory-heavy direction:
flow matching on geometric or constrained domains,
with nonasymptotic sampling guarantees under learned velocity fields,
Euler discretization, early stopping, and geometry/tail regularity assumptions.
```

中文：这不是一个以经验 benchmark 为主的生成模型方向。最强信号是 sampler theory：如何把 vector field、score、divergence、curvature、moment/tail 等局部条件转化为全局 Wasserstein 或 TV 采样误差保证。

English: This is not mainly an empirical benchmark-driven generative modeling direction. The strongest signal is sampler theory: how to convert local assumptions on vector fields, scores, divergences, curvature, and moment/tail behavior into global Wasserstein or TV sampling guarantees.

## High-Confidence Interests / 高置信兴趣点

- 中文：带 learned velocity field 的 flow matching 与 deterministic ODE samplers。
  English: Flow matching with learned velocity fields and deterministic ODE samplers.
- 中文：Euler discretization 下的非渐近收敛率。
  English: Nonasymptotic convergence rates under Euler discretization.
- 中文：convex domains、manifolds、hyperspheres、SPD manifolds 上的 geometry-aware generation。
  English: Geometry-aware generation on convex domains, manifolds, hyperspheres, and SPD manifolds.
- 中文：用 early stopping 处理 `t = 1` 附近的 terminal-time stiffness。
  English: Early stopping as a way to handle terminal-time stiffness near `t = 1`.
- 中文：regularity verification，包括 spatial/temporal Lipschitzness、score regularity、divergence control、curvature distortion 和 moment/tail conditions。
  English: Regularity verification, including spatial/temporal Lipschitzness, score regularity, divergence control, curvature distortion, and moment/tail conditions.
- 中文：可复用证明套路，包括 exact-vs-discretized flow coupling、TV differential inequalities、Young inequality splitting、recurrence/Gronwall propagation 和 dual-to-primal guarantee transfer。
  English: Reusable proof patterns such as exact-vs-discretized flow coupling, TV differential inequalities, Young inequality splitting, recurrence/Gronwall propagation, and dual-to-primal guarantee transfer.

## Likely Negative Preferences / 可能的负向偏好

- 中文：没有数学保证的纯 benchmark 或 architecture 论文。
  English: Pure benchmark or architecture papers without mathematical guarantees.
- 中文：泛泛的 flow/diffusion survey，除非其中有可复用证明框架。
  English: Generic flow/diffusion surveys unless they expose a useful proof framework.
- 中文：纯 Euclidean 论文，除非 proof method 能迁移到 constrained 或 geometric settings。
  English: Euclidean-only papers unless the proof method transfers to constrained or geometric settings.
- 中文：只做 manifold generative modeling 应用、但不分析 discretization 或 sampling error 的论文。
  English: Application-only manifold generative modeling papers without discretization or sampling-error theory.

## Suggested Retrieval Focus / 建议检索重点

1. 中文：直接相关方向
   English: Directly related direction

   中文：检索 Riemannian flow matching、constrained flow matching、mirror flow matching 和 geometric flow matching convergence papers。
   English: Search for Riemannian flow matching, constrained flow matching, mirror flow matching, and geometric flow matching convergence papers.

2. 中文：证明方法迁移
   English: Proof-method transfer

   中文：检索 probability-flow ODE、stochastic interpolant 和 deterministic diffusion sampler analyses 中的 TV/Wasserstein error bounds。
   English: Search for TV/Wasserstein error bounds in probability-flow ODE, stochastic interpolant, and deterministic diffusion sampler analyses.

3. 中文：创新候选方向
   English: Innovation candidates

   中文：重点找改进 terminal-time analysis、弱化 moment/tail assumptions、降低 exponential Lipschitz dependence，或更干净处理 curvature/noncompactness 的论文。
   English: Look for work that improves terminal-time analysis, weakens moment/tail assumptions, reduces exponential Lipschitz dependence, or handles curvature/noncompactness more cleanly.

## Checkpoint / 请确认

1. 中文：下一步应该先做 related-paper retrieval，还是先做 innovation-paper search？
   English: Should the next step emphasize related-paper retrieval or innovation-paper search first?
2. 中文：应该优先 TV bounds、Wasserstein bounds，还是两者都要？
   English: Should we prioritize TV bounds, Wasserstein bounds, or both?
3. 中文：你的主要目标几何是 convex domains、Riemannian manifolds、SPD/hypersphere examples，还是 unified theory？
   English: Is your main target geometry convex domains, Riemannian manifolds, SPD/hypersphere examples, or a unified theory?
4. 中文：现在应该从两篇种子论文抽取 proof-pattern SkillCards，还是先检索更多论文？
   English: Should the workflow now extract proof-pattern SkillCards from the two seed papers, or search more papers first?
