## 全文证明路径梳理 — On a conjecture of Marton

> **数据来源**：`gowers2024_marton_structure.json` + 原文全文

---

### 问题与贡献

| 项目 | 内容 |
|:---|:---|
| **问题** | 多项式 Freiman–Ruzsa 猜想（Marton 猜想）：若 $A \subset \F_2^n$ 满足 $|A+A| \leq K|A|$，证明 $A$ 可被 $O(K^{O(1)})$ 个陪集覆盖 |
| **贡献** | 证明 $C=12$ 成立。首次得到多项式界的常数 |
| **定位** | 加性组合学核心猜想，此前 Sanders (2012) 仅做到拟多项式界 $\exp(\log^{4+o(1)}K)$ |
| **核心创新** | 熵方法与变分框架的结合——将组合问题转化为**含惩罚项泛函的最小化** |

---

### 符号速查

| 符号 | 含义 | 位置 |
|:---|:---|:---:|
| $G = \F_2^n$ | 特征 2 向量空间 | 全文 |
| $X, Y, Z$ | $G$ 值随机变量 | 全文 |
| $\mathbf{H}[X]$ | Shannon 熵 | §A |
| $\mathbf{I}[X:Y]$ | 互信息 | §A |
| $\mathbf{d}(X,Y)$ | Ruzsa 熵距离 $\mathbf{H}[X-Y] - \tfrac12\mathbf{H}[X] - \tfrac12\mathbf{H}[Y]$ | §1 |
| $\mathbf{d}(X\|Z, Y\|W)$ | 条件 Ruzsa 距离 | §A |
| $\tau[X_1;X_2]$ | 含惩罚项的泛函 $\mathbf{d}(X_1,X_2) + \eta\,\mathbf{d}(X_1^0,X_1) + \eta\,\mathbf{d}(X_2^0,X_2)$ | §2 |
| $\eta$ | 常数 $= 1/9$ | §2 |
| $X_1^0, X_2^0$ | 参考变量（固定不动的两个原始变量） | §2 |
| $k$ | $\mathbf{d}(X_1,X_2)$ 的简写 | §3 |
| $U_H$ | 子群 $H$ 上的均匀分布 | §1 |
| $I_1, I_2, I_3$ | 三组条件互信息 | §5–§7 |

---

### 核心定理链

> **Theorem 1 (pfr) — 组合形式 PFR（最终结果）**
> Conjecture 1 以 $C=12$ 成立。
> *证明：由 Theorem pfr-entropy 经附录推导*

> **Theorem pfr-entropy — 熵形式 PFR（核心定理）**
> $\mathbf{d}(X_1^0,U_H) + \mathbf{d}(X_2^0,U_H) \leq 11\;\mathbf{d}(X_1^0,X_2^0)$
> *证明：选择 $\tau$ 的最小元，利用 Proposition de-prop 迫使距离为零，再由 Lemma lem:100pc 得到子群*

> **Proposition de-prop — 递减命题（全篇技术核心）**
> 若 $\mathbf{d}(X_1,X_2) > 0$，则存在 $(X'_1,X'_2)$ 使 $\tau[X'_1;X'_2] < \tau[X_1;X_2]$
> *证明：$\S3$–$\S7$ 的全部内容*

---

### 证明骨架：全篇路径

**武器库**：熵方法 · 纤维引理 · 变分最小化 · Balog–Szemerédi–Gowers 熵引理 · 特征 2 特殊性质

**核心技巧**：将证明拆解为四种候选构造（和/纤维），若全部失败则 $U+V+W=0$ 的 pairwise (almost) independence 通过 BSG 引理导出矛盾。

---

#### Step 0：等价重述

将原组合 PFR 猜想先等价转化为熵形式（已在 [GMT] 中建立等价性）。目标变为：对任意 $G=\F_2^n$ 值随机变量 $X_1^0,X_2^0$，找到子群 $H$ 使 $X_1^0,X_2^0$ 到 $U_H$ 的 Ruzsa 距离被 $11\cdot\mathbf{d}(X_1^0,X_2^0)$ 控制。

---

#### Step 1：变分框架（§2）

引入含惩罚项的泛函（$\eta = 1/9$）：

$$
\tau[X_1; X_2] = \mathbf{d}(X_1,X_2) + \eta\,\mathbf{d}(X_1^0,X_1) + \eta\,\mathbf{d}(X_2^0,X_2)
$$

选取 $\tau$ 的极小元 $(X_1,X_2)$（紧性保证存在性）。

**Lemma lem:100pc**：若 $\mathbf{d}(X_1,X_2)=0$ 则两者都是某个子群 $H$ 的均匀分布。

因此，要证明熵形式 PFR，只需证明极小元处的距离为 0。等价地，需要 **Proposition de-prop**：若距离为正，则存在 $(X'_1,X'_2)$ 使 $\tau$ 严格递减——与极小性矛盾。

剩余全部的证明工作集中在 **Proposition de-prop**。

---

#### Step 2：反证法假设与 $I_1,I_2,I_3$ 的定义（§3）

假设对所有 $(X'_1,X'_2)$ 都有 $\tau[X'_1;X'_2] \geq \tau[X_1;X_2]$（即 de-prop 的逆否），目标是推出 $\mathbf{d}(X_1,X_2)=0$。

定义四种候选构造（$X_1,X_2,\tilde X_1,\tilde X_2$ 为独立同分布拷贝）：

| 构造 | 公式 | 含义 |
|:---|:---|:---|
| 和-1 (S1) | $X'_1 = X_1 + \tilde X_2,\; X'_2 = X_2 + \tilde X_1$ | 交叉和 |
| 和-2 (S2) | $X'_1 = X_1 + \tilde X_1,\; X'_2 = X_2 + \tilde X_2$ | 自和 |
| 纤维-1 (F1) | $(X_1\|X_1+\tilde X_2),\; (X_2\|X_2+\tilde X_1)$ | 交叉纤维 |
| 纤维-2 (F2) | $(X_1\|X_1+\tilde X_1),\; (X_2\|X_2+\tilde X_2)$ | 自纤维 |

如果这四个构造都不满足 de-prop 的递减要求，则可推导出三组条件互信息的上界：

$$
\begin{aligned}
I_1 &= \mathbf{I}[U:V \mid S] \leq 2\eta k \\
I_2 &= \mathbf{I}[U:W \mid S] \leq 2\eta k + \frac{2\eta(2\eta k - I_1)}{1-\eta} \\
I_3 &= \mathbf{I}[V:W \mid S] = I_2
\end{aligned}
$$

其中 $U = X_1+X_2,\; V = \tilde X_1+X_2,\; W = X_1+\tilde X_1,\; S = X_1+X_2+\tilde X_1+\tilde X_2$。

---

#### Step 3：纤维引理 / 核心工具（§4）

**Proposition projections-1（纤维引理）**：
$$
\mathbf{d}(Z_1,Z_2) \geq \mathbf{d}(\pi(Z_1),\pi(Z_2)) + \mathbf{d}(Z_1|\pi(Z_1),\; Z_2|\pi(Z_2))
$$
差距由条件互信息刻画。

**Corollary cor-fibre**（纤维引理的 $G^2$ 特化，两个步骤中均使用的关键恒等式）：
$$
\mathbf{d}(Y_1-Y_3,\,Y_2-Y_4) + \mathbf{d}(Y_1|Y_1-Y_3,\;Y_2|Y_2-Y_4) + \mathbf{I}[Y_1-Y_2:Y_2-Y_4 \mid Y_1-Y_2-Y_3+Y_4] = \mathbf{d}(Y_1,Y_2) + \mathbf{d}(Y_3,Y_4)
$$

该推论本质上是将两个独立随机变量对的 Ruzsa 距离分解为"投影距离 + 条件距离 + 条件互信息"三部分，是推导 $I_1$、$I_2$ 上界的核心计算工具。

---

#### Step 4：第一估计 — 推导 $I_1 \leq 2\eta k$（§5）

将 Cor cor-fibre 应用于 $(Y_1,Y_2,Y_3,Y_4) = (X_1,X_2,\tilde X_2,\tilde X_1)$：

$$
\mathbf{d}(X_1+\tilde X_2, X_2+\tilde X_1) + \mathbf{d}(X_1|X_1+\tilde X_2,\; X_2|X_2+\tilde X_1) + I_1 = 2k
$$

由反证假设（S1 和 F1 不满足递减），用 **Lemma cond-dist-fact** 和 **Lemma first-useful**（来自 Madiman/KV 不等式的熵界）控制条件距离项，得到 $I_1 \leq 2\eta k$。

**Lemma cond-dist-fact**：
$$
\mathbf{d}(X|Z,\;Y|W) \leq \mathbf{d}(X,Y) + \tfrac12 \mathbf{I}(X:Z) + \tfrac12 \mathbf{I}(Y:W)
$$

**Lemma first-useful**（两个不等式）：
$$
\begin{aligned}
\mathbf{d}(X, Y-Z) - \mathbf{d}(X,Y) &\leq \tfrac12(\mathbf{H}[Y-Z] - \mathbf{H}[Y]) \\
\mathbf{d}(X,Y|Y-Z) - \mathbf{d}(X,Y) &\leq \tfrac12(\mathbf{H}[Y-Z] - \mathbf{H}[Z])
\end{aligned}
$$

---

#### Step 5：第二估计 — 推导 $I_2,I_3$ 上界（§6）

再次调用 Cor cor-fibre，但置换变量 $(Y_1,Y_2,Y_3,Y_4) = (X_2,X_1,\tilde X_2,\tilde X_1)$：

$$
\mathbf{d}(X_1+\tilde X_1, X_2+\tilde X_2) + \mathbf{d}(X_1|X_1+\tilde X_1,\; X_2|X_2+\tilde X_2) + I_2 = 2k
$$

类似的推导路径给出 $I_2 = I_3$ 的上界。关键中间步骤是利用第一估计的 $I_1$ 控制 $\mathbf{d}(X_1,X_1)+\mathbf{d}(X_2,X_2)$：

$$
\mathbf{d}(X_1,X_1) + \mathbf{d}(X_2,X_2) \leq 2k + \frac{2(2\eta k - I_1)}{1-\eta}
$$

代入后得 $I_2 \leq 2\eta k + \frac{2\eta(2\eta k - I_1)}{1-\eta}$。

---

#### Step 6：终局论证（§7）—— 特征 2 的独奏

当 S1/S2/F1/F2 全部失效时，$I_1,I_2,I_3$ 都"足够小"。此时定义一组随机变量：

$$
U = X_1+X_2,\quad V = \tilde X_1+X_2,\quad W = X_1+\tilde X_1,\quad S = X_1+X_2+\tilde X_1+\tilde X_2
$$

在 **特征 2** 下有关键恒等式（全文唯一不能通过换号回避的特征 2 使用处）：

$$
U + V + W = 0
$$

因此对每个 $s$，条件变量 $(U|S=s), (V|S=s), (W|S=s)$ 满足和为 0。

**Lemma lem:abstract**：若 $T_1+T_2+T_3=0$ 且 $\delta = \sum_{i<j}\mathbf{I}[T_i:T_j]$ 较小，则存在 $T'_1,T'_2$ 使 $\psi[T'_1;T'_2]$ 以 $\delta$ 和距离项的上界控制。证明使用 **熵 BSG 引理**（Lemma lem-bsg，本文附录给出更优常数版本）。

将 Lemma lem:abstract 应用于条件变量 $(U|S=s), (V|S=s), (W|S=s)$ 并关于 $s$ 取平均，得到：

$$
k \leq \tilde\delta + \frac{\eta}{3}\Bigl(\tilde\delta + \sum_{i=1}^2\sum_{A\in\{U,V,W\}} \bigl(\mathbf{d}(X_i^0|A|S) - \mathbf{d}(X_i^0,X_i)\bigr)\Bigr)
$$

代入 $\tilde\delta \leq 6\eta k - \frac{1-5\eta}{1-\eta}(2\eta k - I_1)$ 和距离上界，对 $\eta=1/9$ 得：

$$
k \leq (8\eta + \eta^2)k < k
$$

矛盾。因此 $k=0$，Proposition de-prop 获证。

---

#### Step 7：从熵 PFR 到组合 PFR（附录 B）

1. 取 $U_A$ 为 $A$ 上均匀分布，由 $|A+A|\leq K|A|$ 得 $\mathbf{d}(U_A,U_A) \leq \log K$
2. 熵形式 PFR $\Rightarrow \exists H$ 使 $\mathbf{d}(U_A,U_H) \leq \frac{C'}{2}\log K$
3. 由 Ruzsa 覆盖引理，$A$ 可被至多 $2K^{C'/2+1}\frac{|H|^{1/2}}{|A|^{1/2}}$ 个 $H$ 的陪集覆盖
4. 结合 $|\;|H|-|A|\;| \leq \frac{C'}{2}\log K$ 的约束，总覆盖数 $\leq 2K^{C'+1}$
5. $C' = 11$ 代入得 $C = 12$

---

### 逻辑依赖全图

```
paper:arxiv:2311.05762
│
├── Theorem 1 (pfr)          ← 组合形式 PFR，C=12
│   └── Theorem pfr-entropy  ← 熵形式 PFR
│       ├── Proposition de-prop ← 递减命题（主体工程）
│       │   ├── Corollary cor-fibre ← 纤维引理推论（关键工具）
│       │   │   └── Proposition projections-1 ← 纤维引理
│       │   ├── Lemma cond-dist-fact ← 条件距离上界 [入度=3，核心枢纽]
│       │   ├── Lemma first-useful ← Madiman/KV 熵不等式
│       │   │   └── Lemma cond-dist-fact (用到)
│       │   ├── Lemma second-useful ← 另一个熵不等式
│       │   │   └── Lemma first-useful (用到)
│       │   └── Lemma lem:abstract ← 终局抽象引理
│       │       ├── Lemma lem-bsg (entropic BSG，来自 [tao-entropy])
│       │       └── Lemma cond-dist-fact (用到)
│       └── Lemma lem:100pc ← 零距离 → 子群
│           └── [EXTERNAL: tao-entropy Thm 1.11(i)]
│
├── Corollary additive-stability  (f: F2^m → F2^n 的线性性逼近)
├── Corollary partial-additivity   (partial linearity → 几乎线性)
├── Corollary u3-inverse           (U^3 范数的逆定理)
└── Theorem th13                   (整数群上的弱 PFR)
```

---

### 核心技术洞察

1. **为什么用熵而非组合？** 熵版本将集合 $A$ 替换为随机变量 $X$，将组合对象（和集、陪集）替换为信息论量（熵、互信息）。其优势在于：条件作用（conditioning）可作为"精细化"工具，且变分框架允许使用紧性。

2. **为什么 τ 泛函需要惩罚项？** 纯 $\mathbf{d}(X_1,X_2)$ 的最小化是平凡的（取 $X_1=X_2$ 即可）。惩罚项将参考变量 $X_1^0,X_2^0$ 的信息拉入泛函，确保极小元与原始问题相关。

3. **四种构造的逻辑**：和构造与纤维构造是"对偶"的——和对应组合学中的 sumset，纤维对应 intersection/covering。两种都不行就意味着 additive 结构极弱。

4. **为何特征 2 不可或缺？** $U+V+W=0$ 的恒等式依赖于 $\F_2^n$ 中 $x+x=0$。在奇特征下需要改用 $p$-部距离 $\mathbf{D}[X_1;\dots;X_p]$，推广到后续论文 [GGMT-pfr-odd]。

5. **BSG 引理的角色**：当 $I_1,I_2,I_3$ 仅"较小"而非零时，$T_1,T_2,T_3$ 只是近似 pairwise 独立而非精确独立。熵 BSG 引理提供了从近似独立到真正小距离的"能量转移"机制。

---

### 阅读门槛

| 前置知识 | 熟练度要求 | 参考来源 |
|:---|:---:|:---|
| Shannon 熵、互信息、条件熵 | 高 | 附录 A（自含） |
| Ruzsa 熵距离及其三角不等式 | 高 | [tao-entropy] / [GMT] |
| Balog–Szemerédi–Gowers 引理（熵版本） | 中 | 附录 A.2（自含） |
| Madiman/KV 不等式 | 低 | 附录 A.1（自含） |
| Ruzsa 覆盖引理 | 低 | [tao-vu] |
| $\F_2^n$ 上 Freiman 型问题的背景 | 中 | [green-pfr-note] / [lovett-survey] |

文件中已保存至：`memory/notes/Gowers_PFR_证明路径_2026-05-15.md`
