# Paper To Skill Report / 论文 Skill 抽取报告

2026-10-22 状态补充：下列 accepted 只表示抽取质量。所有单篇卡新增验证字段并保留为候选；连续流稳定性目标已在[跨论文检查](../../flow_stability_validation.md)完成另行推导和精确解复用，其余卡的数学依赖与适用范围尚未独立检查。

Paper: `Error Bounds for Flow Matching Methods`

Input preserved: `paper.md`

## Accepted / 已接受

- `alekseev_grobner_ode_perturbation_wasserstein_bound`  
  EN: Uses Alekseev-Grobner plus Gronwall to turn ODE drift error into endpoint W2 error.  
  ZH: 用 Alekseev-Grobner 和 Gronwall 将 ODE 漂移误差转为终点 Wasserstein 误差。

- `smoothing_bias_variance_balance_for_polynomial_wasserstein_rate`  
  EN: Balances smoothing bias with stability-amplified approximation error to get a polynomial W2 rate.  
  ZH: 平衡平滑偏差与稳定性放大的逼近误差，得到多项式 W2 速率。

## Needs Review / 需要复核

- `gaussian_smoothing_lipschitz_integral_control`
  EN: The corrected extraction score is 3.9, so the card requires review under the existing rubric. Its mathematical verification remains pending.
  ZH: 修正后的抽取评分为 3.9，按既有规则调整为需要复核；数学验证仍未完成。

- `lambda_regular_certification_via_conditional_covariance`  
  EN: Useful as a verification checklist, but the regularity notion is nonstandard and should be reviewed before adding to the core library.  
  ZH: 可作为正则性假设认证清单，但 lambda-regular 条件较非标准，入库前建议专家复核。

## Rejected / 已拒绝

- No pure related-work or contribution-summary spans were extracted, because they do not provide operational proof steps.

## Mathematical Risk / 数学风险

The key risk is assumption transfer. These cards require smooth ODE flows, correct path-law L2 error, positive smoothing schedules, and covariance regularity. The cards should be called only after those assumptions are explicitly checked.

关键风险是条件迁移：这些 Skill 需要光滑 ODE 流、沿正确路径分布的 L2 误差、正的平滑日程，以及条件协方差正则性。调用前应先显式检查这些条件。
