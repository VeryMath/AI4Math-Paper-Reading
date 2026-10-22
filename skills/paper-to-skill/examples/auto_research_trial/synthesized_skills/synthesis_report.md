# Cross-Paper Skill Synthesis Report / 跨论文 Skill 合成报告

Research project: `auto_research_trial_flow_matching_error_analysis`

Inputs:

- `examples/auto_research_trial/papers/vES22INUKm/skill_cards`
- `examples/auto_research_trial/papers/uqQPyWFDhY/skill_cards`

## Result / 结果

EN: The seven single-paper extractions form six proof-pattern families. The 2026-10-22 revision independently derives the continuous-flow stability statement, checks three new exact-solution problems, and records four failed generalizations. Only that bounded statement currently meets the revised library criteria.

ZH: 7 张单篇卡组成 6 个证明模式族。2026-10-22 修订对连续流稳定性结论另作推导，完成三个新问题的精确解复用，并检查四种失败边界。当前只有这个明确范围内的结论满足新的入库标准。详见[实际数学检查](../flow_stability_validation.md)。

EN: Five single-source cards preserve their source extraction scores, without a new synthesis assessment. The Gaussian smoothing score is 3.9 and its extraction status is `needs_review`. These scores do not change mathematical verification or promotion. The Gaussian-support and empirical-process independence conditions remain explicit.

ZH: 五张单来源合成卡保留来源抽取评分，没有重新评价合成质量。高斯平滑卡分数为 3.9，抽取状态为 `needs_review`；评分不改变数学验证或晋级结论。有界支撑及样本独立性条件均需显式保留。

## Ready For Library / 可入库

- `ode_flow_stability_to_wasserstein_error`
  EN: Uses an integral Gronwall argument with explicit path law, finite moments, integrable Lipschitz envelope, and final-time factor.
  ZH: 采用积分 Gronwall 论证，明确路径分布、有限矩、可积 Lipschitz 常数和时间长度因子。独立检查指不同数学论证，不代表独立研究者或形式化系统复核。

## Needs Human Review / 需要人工复核

- `truncation_based_l2_approximation_on_unbounded_domain`
- `gaussian_smoothing_lipschitz_integral_control`
- `smoothing_bias_variance_balance_for_polynomial_wasserstein_rate`

  EN: These remain candidates until their mathematical dependencies, reusable statement, actual reuse, and failure boundaries have been checked. Earlier readiness labels relied only on extraction and are withdrawn.
  ZH: 三张卡尚缺数学依赖检查、独立论证、实际复用和失败边界，保留候选状态；旧报告仅凭抽取质量作出的入库判断已撤回。

- `truncated_empirical_process_generalization_decomposition`
  EN: The proof pattern is useful, but reuse depends on independence, truncation event design, and covering-number constants.
  ZH: 模式有价值，但复用前必须检查独立性、截断事件设计和覆盖数常数。

- `lambda_regular_certification_via_conditional_covariance`
  EN: Best treated as a certification checklist for now because lambda-regularity is nonstandard.
  ZH: 目前更适合作为假设认证清单，因为 lambda-regular 条件并非常规假设。

## Method Map / 方法论地图

EN:

1. Approximation layer: use truncation to move compact approximation into unbounded-domain L2 control.
2. Statistical layer: control learned velocity error via empirical-process decomposition with truncation.
3. Dynamical layer: convert velocity or drift error into endpoint W2 error through flow stability.
4. Regularization layer: use Gaussian smoothing to control time-varying Lipschitz constants.
5. Tradeoff layer: add smoothing bias and optimize the smoothing scale.
6. Assumption-certification layer: verify covariance regularity conditions before applying smoothing-based theorems.

ZH:

1. 逼近层：用截断把紧域逼近推广到无界域 L2 控制。
2. 统计层：通过截断经验过程分解控制学习到的速度场误差。
3. 动力系统层：用流稳定性把速度/漂移误差转成终点 W2 误差。
4. 正则化层：用高斯平滑控制时间变 Lipschitz 常数。
5. 权衡层：加入平滑偏差并优化平滑尺度。
6. 假设认证层：在使用平滑定理前先认证条件协方差正则性。

## Conflicts And Risks / 冲突与风险

- EN: The two flow-stability sources use different proof routes. Their references are preserved; the merged procedure uses the separately derived integral argument, with Jacobian control retained only as source context.
- ZH: 两个来源的证明路线均保留引用；合成卡的通用步骤采用另行推导的积分论证，Jacobian 路线只保留为来源说明。

- EN: Several cards rely on nontrivial regularity assumptions: spatial Lipschitz bounds, positive smoothing schedules, covariance regularity, and correct path-law L2 errors.
- ZH: 多张卡依赖较强正则性条件：空间 Lipschitz、正的平滑日程、条件协方差正则性，以及沿正确路径分布的 L2 误差。

- EN: Do not reuse paper-specific convergence exponents unless all assumptions and schedules match.
- ZH: 不要直接复用单篇论文里的收敛指数，除非假设和日程选择完全匹配。
