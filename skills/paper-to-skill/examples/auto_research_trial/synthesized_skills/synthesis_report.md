# Cross-Paper Skill Synthesis Report / 跨论文 Skill 合成报告

Research project: `auto_research_trial_flow_matching_error_analysis`

Inputs:

- `examples/auto_research_trial/papers/vES22INUKm/skill_cards`
- `examples/auto_research_trial/papers/uqQPyWFDhY/skill_cards`

## Result / 结果

EN: The seven single-paper Skill Cards were clustered into six reusable proof-pattern families. One cross-paper merge was strong enough for a library-ready generalized card: ODE flow stability to Wasserstein error.

ZH: 7 张单论文 Skill Card 被聚类成 6 个可复用证明模式族。其中 1 个跨论文合并最稳定，适合作为可入库泛化卡：ODE 流稳定性到 Wasserstein 误差。

## Ready For Library / 可入库

- `ode_flow_stability_to_wasserstein_error`  
  EN: Cross-paper synthesis of coupling/Gronwall and Alekseev-Grobner routes.  
  ZH: 合并了“耦合 + Gronwall”和 “Alekseev-Grobner + Jacobian 控制”两条路线。

- `truncation_based_l2_approximation_on_unbounded_domain`  
  EN: Single-source but standard, operational, and broadly reusable.  
  ZH: 单论文来源，但模式标准、步骤清楚、复用性强。

- `gaussian_smoothing_lipschitz_integral_control`  
  EN: Useful for replacing uniform Lipschitz assumptions by schedule-dependent integral bounds.  
  ZH: 可用于把统一 Lipschitz 假设替换为依赖平滑日程的积分型 Lipschitz 控制。

- `smoothing_bias_variance_balance_for_polynomial_wasserstein_rate`  
  EN: Captures the bias-stability tradeoff induced by endpoint smoothing.  
  ZH: 抽象出端点平滑带来的“稳定性收益 vs 平滑偏差”平衡套路。

## Needs Human Review / 需要人工复核

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

- EN: The two flow-stability sources use different proof routes. The synthesized card preserves both rather than over-generalizing them into one formal proof.
- ZH: 两个流稳定性来源使用不同证明路线；合成卡保留两条路线，避免强行合并为单一形式。

- EN: Several cards rely on nontrivial regularity assumptions: spatial Lipschitz bounds, positive smoothing schedules, covariance regularity, and correct path-law L2 errors.
- ZH: 多张卡依赖较强正则性条件：空间 Lipschitz、正的平滑日程、条件协方差正则性，以及沿正确路径分布的 L2 误差。

- EN: Do not reuse paper-specific convergence exponents unless all assumptions and schedules match.
- ZH: 不要直接复用单篇论文里的收敛指数，除非假设和日程选择完全匹配。
