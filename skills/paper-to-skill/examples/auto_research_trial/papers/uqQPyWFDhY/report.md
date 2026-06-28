# Paper To Skill Report / 论文 Skill 抽取报告

Paper: `Error Bounds for Flow Matching Methods`

Input preserved: `paper.md`

## Accepted / 已接受

- `alekseev_grobner_ode_perturbation_wasserstein_bound`  
  EN: Uses Alekseev-Grobner plus Gronwall to turn ODE drift error into endpoint W2 error.  
  ZH: 用 Alekseev-Grobner 和 Gronwall 将 ODE 漂移误差转为终点 Wasserstein 误差。

- `gaussian_smoothing_lipschitz_integral_control`  
  EN: Bounds an integrated time-varying Lipschitz constant through Gaussian smoothing and conditional covariance control.  
  ZH: 通过高斯平滑和条件协方差控制，证明时间变 Lipschitz 常数的积分界。

- `smoothing_bias_variance_balance_for_polynomial_wasserstein_rate`  
  EN: Balances smoothing bias with stability-amplified approximation error to get a polynomial W2 rate.  
  ZH: 平衡平滑偏差与稳定性放大的逼近误差，得到多项式 W2 速率。

## Needs Review / 需要复核

- `lambda_regular_certification_via_conditional_covariance`  
  EN: Useful as a verification checklist, but the regularity notion is nonstandard and should be reviewed before adding to the core library.  
  ZH: 可作为正则性假设认证清单，但 lambda-regular 条件较非标准，入库前建议专家复核。

## Rejected / 已拒绝

- No pure related-work or contribution-summary spans were extracted, because they do not provide operational proof steps.

## Mathematical Risk / 数学风险

The key risk is assumption transfer. These cards require smooth ODE flows, correct path-law L2 error, positive smoothing schedules, and covariance regularity. The cards should be called only after those assumptions are explicitly checked.

关键风险是条件迁移：这些 Skill 需要光滑 ODE 流、沿正确路径分布的 L2 误差、正的平滑日程，以及条件协方差正则性。调用前应先显式检查这些条件。
