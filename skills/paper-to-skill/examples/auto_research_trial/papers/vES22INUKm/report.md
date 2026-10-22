# Paper To Skill Report / 论文 Skill 抽取报告

Paper: `An Error Analysis of Flow Matching for Deep Generative Modeling`

Input preserved: `paper.md`

2026-10-22 状态补充：下列 accepted 只表示抽取质量。所有单篇卡新增验证字段并保留为候选；连续流稳定性目标已在[跨论文检查](../../flow_stability_validation.md)完成另行推导和精确解复用，单篇统计收敛率未验证。

## Accepted / 已接受

- `truncation_based_l2_approximation_on_unbounded_domain`  
  EN: Turns compact approximation into full-domain L2 approximation by truncation and tail control.  
  ZH: 通过紧集截断和尾部概率控制，把紧域逼近定理迁移到无界域 L2 误差。

- `coupling_gronwall_wasserstein_flow_error_bound`  
  EN: Converts velocity-field L2 error into Wasserstein distribution error through coupled ODE paths and Gronwall.  
  ZH: 用同一起点耦合精确/近似流，再用 Gronwall 把速度场误差转成 W2 分布误差。

## Needs Review / 需要复核

- `truncated_empirical_process_generalization_decomposition`  
  EN: Useful, but the truncation event, sample-source independence, and covering-number constants need expert review.  
  ZH: 很有复用价值，但截断事件、样本源独立性和覆盖数常数需要人工复核。

## Rejected / 已拒绝

- No separate Skill Card was produced for the main consistency theorem alone, because it is primarily a paper-specific theorem statement rather than an operational proof pattern.

## Mathematical Risk / 数学风险

The main risk is that these patterns rely on hidden regularity: bounded moments, tail decay, Lipschitz flow maps, and valid conditioning of the distribution along the exact flow. Reuse should check these assumptions before applying the cards.

主要风险在于隐含正则性：矩、有界尾部、Lipschitz 流映射，以及沿精确流分布取条件期望的合法性。复用前需要逐项检查。
