---
type: paper
global_uri: "paper:behrens_induced_saturation"
arxiv_id: "[UNKNOWN]"
source_json: true
json_path: "behrens_induced_saturation_structure.json"
core_theorems: ["paper:behrens#Cor-indsat_paw", "paper:behrens#Thm-paw_unique", "paper:behrens#Cor-sis_paw", "paper:behrens#Cor-cor:stars", "paper:behrens#Thm-bound:stars"]
status: [待读]
tags: ["#graph-theory", "#induced-saturation", "#extremal-combinatorics", "#paw", "#claw"]
---

## 文献笔记：Graphs with induced-saturation number zero

### L1 基础视图
- **核心一句话**：证明了许多常见图的诱导饱和数为零（即存在真正的图而非 trigraph 满足诱导饱和性），并引入新参数 $\operatorname{indsat}^*(n,H)$ 刻画最小边数。
- **直觉与启发**：诱导饱和数的定义天然需要 trigraph（三色图），但本文发现对许多图而言普通图就足够了——这简化了问题，并引出了有趣的极值问题。

### 核心结论

**逐字原文（Corollary indsat_paw）**：
> For $n \geq 7$, $\operatorname{indsat}(n,K_{1,3}^+) = 0$.

**逐字原文（Theorem paw_unique — paw 的刻画定理）**：
> A graph is paw-induced-saturated if and only if it is as described in Construction 3.1: a graph with at most one trivial component, where each nontrivial component is complete multipartite with at least three parts, at most one part of size 1, and all other parts of size at least 3.

**逐字原文（Corollary sis paw — paw 的最小边数公式）**：
> For $n \geq 7$, let $n \equiv r \pmod{7}$, $0 \leq r \leq 6$. Then
> $$\operatorname{indsat}^*(n,\text{paw}) = \begin{cases} 15n/7 & \text{if } r=0 \\ 15\lfloor n/7\rfloor + 4(r-1) & \text{if } r \neq 0 \end{cases}.$$

**逐字原文（Corollary cor:stars — 星图的诱导饱和数为零）**：
> For fixed $k \geq 2$ and $n \geq 3^k$, $\operatorname{indsat}(n, K_{1,k+1}) = 0$.

**逐字原文（Theorem bound:stars — 星图 sis 的上下界）**：
> For $n \geq 2\cdot 3^k$ and $k \geq 2$, there exist constants $c_1=c_1(k)$ and $c_2=c_2(k)$ such that $n\cdot k/2 - c_1 \leq \operatorname{indsat}^*(n,K_{1,k+1}) \leq n\cdot k + c_2$.

**用我的话复述**：
这篇论文研究的是"诱导饱和数"——这是一个衡量"还需要多少条灵活边（灰色边）才能让一个图系统对目标图 $H$ 满足饱和性质"的参数。作者发现对 paw（带柄三角形）、星图 $K_{1,k+1}$、$C_4$、奇圈、匹配等许多常见图，诱导饱和数为零，意味着存在真正的图（而非 trigraph）满足诱导饱和性。对于 paw，他们不仅证明了这一点，还完整刻画了所有 paw-诱导饱和图的结构（完全多部图的并），从而精确算出了极值边数 $\operatorname{indsat}^*(n,\text{paw})$。对于星图，他们给出了上下界，系数在 $k/2$ 和 $k$ 之间，且对 $k=2$（即 claw $K_{1,3}$）达到了上界。

### 与我何干
- **对我有用的是**：诱导饱和数的构造方法和极值下界技巧，特别是 paw 的完整刻画
- **可以用在**：图饱和理论的文献引用，或扩展至其他图类的诱导饱和数研究
- **待验证的假设**：星图 sis 的下界是否可达？系数 $k/2$ 能否改进？

### 待深入问题
- [ ] 对于 $C_4$ 和奇圈，诱导饱和数为零的具体构造是什么？
- [ ] $\operatorname{indsat}^*(n,K_{1,3})$ 的 additive constant of four 是如何实现的？

### 录入时间
录入于：2026-05-15 | 最近查看：2026-05-15
