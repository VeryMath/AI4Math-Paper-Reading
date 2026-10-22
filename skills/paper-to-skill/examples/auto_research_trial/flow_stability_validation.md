# 流稳定性 SkillCard：实际提取、合并与数学检查

检查日期：2026-10-22。输入是本例已保存的两篇完整论文 Markdown；本次没有重新转换 PDF。以下为实际完成的提取修订和数学检查，不是 Agent 能力评测。

## 1. 从原文提取的内容

| 原文 | 直接支持的证明步骤 | 不能直接带入通用卡的内容 |
| --- | --- | --- |
| [An Error Analysis of Flow Matching](papers/vES22INUKm/paper.md)，354–402 行 | 360–369 行共同初始化耦合；375–393 行分离漂移误差和稳定项；396–402 行 Gronwall | 特定神经网络、样本数和统计收敛率；399 行使用论文的单位时间范围 |
| [Error Bounds for Flow Matching Methods](papers/uqQPyWFDhY/paper.md)，101–171 行 | 101 行沿精确路径的 L2 误差；103–105 行光滑流与近似场 Lipschitz；144–168 行扰动公式、Jacobian 和积分估计 | 删除光滑性后继续使用 Jacobian 公式；把时间区间 [0,1] 的公式直接推广到任意 T |

两者共同的数学目标是：把沿精确流分布的漂移误差，转成共同初始化下的终点 W2 误差。源论文并没有提供本记录下面三个新问题的复用结果。

## 2. 独立推导及依赖

记 X'=v(X,t)，Y'=w(Y,t)，X0=Y0，初始分布和两个终点分布有有限二阶矩。要求两条流存在且唯一、路径绝对连续；w 在空间全局 Lipschitz，常数 L(t)≥0 且可积。记

\[
\eta(t)=\bigl(\mathbb E\|w(X_t,t)-v(X_t,t)\|^2\bigr)^{1/2},
\qquad \varepsilon^2=\int_0^T\eta(t)^2\,dt<\infty.
\]

本次用积分形式另作推导，不复用论文的最终误差公式。逐路径加减 w(X,t)，得到

\[
\|Y_t-X_t\|\leq\int_0^t L(s)\|Y_s-X_s\|ds+
\int_0^t\|w(X_s,s)-v(X_s,s)\|ds.
\]

积分 Gronwall 给出

\[
\|Y_T-X_T\|\leq\int_0^T e^{\int_s^T L(r)dr}
\|w(X_s,s)-v(X_s,s)\|ds.
\]

再用 L2 的 Minkowski 积分不等式和时间上的 Cauchy–Schwarz：

\[
W_2(\mathrm{Law}(X_T),\mathrm{Law}(Y_T))
\leq\|Y_T-X_T\|_{L^2}
\leq\left(\int_0^T e^{2\int_s^T L(r)dr}ds\right)^{1/2}\varepsilon
\leq\sqrt{T}\,e^{\int_0^T L(r)dr}\varepsilon.
\]

依赖逐项为：共同初始化构成合法耦合；可积 L 保证 Gronwall 因子有限；有限二阶矩使 W2 定义适用；漂移误差沿 X 的分布求值；Minkowski 和 Cauchy–Schwarz 使用上述可积性。这个论证不要求对流映射求导。它不证明 ODE 的存在唯一性，也不包含离散求解器误差或样本复杂度。

“独立”在这里指采用不同数学论证并检查精确解；执行者仍是本次 coding agent，没有独立研究者复核，也没有 Lean 形式化证明。

## 3. 合并冲突与实际解决

| 冲突 | 处理与依据 |
| --- | --- |
| 第一条路线用差分不等式，第二条路线对流映射求导 | 合并目标，通用步骤采用上面的积分证明；光滑 Jacobian 路线保留为原文来源，不把其公式直接用于不可微场。 |
| 旧卡写“differentiable or Lipschitz enough”而没有确定条件 | 明确为存在唯一的绝对连续流、空间全局 Lipschitz、可积 L、有限二阶矩与正确路径分布。 |
| 原文在单位时间上给出界，通用卡未说明任意 T 的常数 | 补上核积分，粗界含 sqrt(T)。第四节的 T=4 精确解直接否定缺失时间因子的推广。 |
| 旧合并卡 source 行为 0，字段与提取模板不同 | 改用真实代表来源行 354–402；保留两篇来源，统一 description/input/output 字段。 |

## 4. 跨问题复用和失败案例

运行：

```bash
python3 examples/auto_research_trial/flow_stability_check.py
```

脚本直接计算精确 ODE 解和理论界，只用 Python 标准库。高斯例中两个终点高斯方差相同，W2 等于均值差；Dirac 例中 W2 等于两点距离。以下都检查实际数学命题，不涉及 PDF 转换或程序调用是否成功的替代指标。

| 问题 | 条件和调整 | 结果 |
| --- | --- | --- |
| X'=X，Y'=Y+0.1，共同 N(0,1) 起点，T=1 | 线性增长、L=1；沿 X 的误差恒为 0.1 | 精确 W2=0.171828182846；核积分上界=0.178732427093。 |
| X'=-2X，Y'=-2Y+0.1t，共同 N(0,1) 起点，T=2 | 改为收缩流和时变输入；L=2；epsilon²=0.01 T³/3 | 精确 W2=0.0754578909722，上界=4.45717248716；通用 Lipschitz 界有效但很松。 |
| X'=0，Y'=abs(Y)+0.2，共同起点 0，T=1 | 近似场在 0 不可微，但全局 Lipschitz、唯一；Y 始终非负 | 精确 W2=0.343656365692，上界=0.357464854187；不能直接调用源文的光滑 Jacobian 论证。 |
| 错误推广：删除稳定性因子 | 取 X'=3X，Y'=3Y+0.1，T=1 | W2=0.1(e³-1)/3 > epsilon=0.1，拒绝该推广。 |
| 错误推广：任意 T 都用单位区间公式 | 取 X'=0，Y'=0.2，T=4 | W2=0.8 > epsilon=0.4；补 sqrt(T) 后等号成立。 |
| 错误推广：用无关分布的误差替代路径误差 | X'=0，Y'=Y，共同起点 1；却在 delta_0 下测漂移误差 | 错误误差为 0，实际 W2=e-1；沿正确 delta_1 路径计算后界成立。 |
| 失败边界：删除唯一性和 Lipschitz 条件 | X'=0，Y'=2sqrt(abs(Y))，共同起点 0 | 沿 X 的漂移误差为 0，但 Y=t² 是另一合法解，T=1 时 W2=1；拒绝应用。 |

## 5. 当前状态

通用积分界已完成手工推导，三个新数学问题已用精确解复用，四种失败边界已有显式反例。对应卡的验证状态只覆盖上述连续流稳定性结论；不覆盖论文统计率、离散化、训练效果或 Agent 使用收益。其余示例卡尚无这些检查记录，保留为待验证候选，不能沿用旧报告的入库结论。

数值输出由执行命令实际计算；没有数值积分误差，仍有通常的浮点舍入。

## 6. 实际运行记录

上述命令退出码为 0，输出如下：

```text
affine Gaussian perturbation: exact_W2=0.171828182846, bound=0.178732427093, expected <=: confirmed
time-dependent forcing of a contracting flow: exact_W2=0.0754578909722, bound=4.45717248716, expected <=: confirmed
nondifferentiable Lipschitz field: exact_W2=0.343656365692, bound=0.357464854187, expected <=: confirmed
reject removal of stability amplification: exact_W2=0.636184564106, bound=0.1, expected >: confirmed
reject unit-interval formula at T=4: exact_W2=0.8, bound=0.4, expected >: confirmed
restore time factor at T=4: exact_W2=0.8, bound=0.8, expected <=: confirmed
reject drift error under an unrelated path law: exact_W2=1.71828182846, bound=0, expected >: confirmed
use drift error along the exact path instead: exact_W2=1.71828182846, bound=1.78732427093, expected <=: confirmed
reject omission of uniqueness and Lipschitz control: exact_W2=1, bound=0, expected >: confirmed
```
