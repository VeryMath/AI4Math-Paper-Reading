# 真实论文示例核对

核对日期：2026-10-22。范围为仓库已有的两份 TeX 原文、两个结构 JSON，以及 Gowers 的依赖图；不修改论文原文。本次没有调用外部模型或查阅外部论文，也没有重新编译 PDF。行号均指 `examples/paper/` 中现有文件。

## Gowers：抽取错误与遗漏

已逐项对照原文的 15 个既有实体，并补入两个确实遗漏的无标签结果。JSON 的 `statement` 改为保留原符号的 TeX 原文，`location.source_lines` 给出定位。未核实的印刷页码改为 `[UNKNOWN]`。年、arXiv 编号沿用旧记录，未独立核实。

| 原文位置：pfr2-submit.tex | 原记录问题 | 本次处理 |
|---|---|---|
| 187–189；1137–1161 | pfr 的 role 写成 corollary，证明位置只写 §1，漏掉实际使用的外部覆盖引理 | role 改为 main，定位附录 B；补记 1155 行引用的 tao-vu, Lemma 2.14 |
| 255–263；292–308；313–338 | 简写没有保留 de-prop 的固定群、参考变量和 eta 上下文 | 保留完整定理原文，补 `source_context`；确认 de-prop、lem:100pc → pfr-entropy |
| 559–601 | 纤维引理摘要漏掉同态/阿贝尔群条件和独立时的余项；cor-fibre 漏掉四变量独立条件 | 保留完整原陈述；确认 projections-1 → cor-fibre；补记 gmt, Proposition 1.4 的来源说明 |
| 674–686 | cond-dist-fact 摘要未交代变量所在群及成对条件化设置 | 改为完整原陈述；证明引用的是本地定义和熵事实，不把“standard entropy identities”当一篇外部文献 |
| 689–714；1070–1087 | first-useful 漏掉 Y、Z 独立及第二条条件距离结论；把 Madiman/KV 写成不确定依赖；附录中有完整引理却没抽取 | 补入 `Lemma entropy-growth (auto, Appendix A)`，标 `auto_labeled: true`；确认它及 cond-dist-fact → first-useful |
| 809–818 | second-useful 漏掉 Y、Z、Z' 独立 | 改为完整原陈述；两条被引用的不等式都是 first-useful 的结论，确认 first-useful → second-useful |
| 874–897；923 | abstract 只有“存在带某界的变量”等摘要；把 BSG 到 de-prop 的间接使用记成不确定直连 | 保留完整界；确认 lem-bsg、cond-dist-fact → lem:abstract → de-prop；删除那条多余的不确定直连 |
| 636、719、749、768、842–846、923 | de-prop 到 cond-dist-fact 的直接关系混入了传递依赖 | de-prop 的已记录直接前置项为 cor-fibre、first-useful、second-useful、lem:abstract；经引理使用 cond-dist-fact 的路径仍保留 |
| 1091–1097 | BSG 来源写成简单复述 tao-entropy Lemma 3.3，漏掉“更好常数、不同证明”和联合分布可以相关的说明 | 保留完整陈述，准确记录“closely related”来源；不能把 ent(A+B) 当作独立副本之和的熵 |
| 196–224 | th13 和三个 PFR 应用的外部论证没有列入 external_refs；u3-inverse 漏掉 1-bounded 条件，两个函数结论漏掉定义域/陪域 | 补完整原陈述与当地引用；这些外部定理的实际内容仍未独立核对 |
| 231–235 | 无标签 Mudgal 推论未抽取 | 补入 `Corollary Mudgal (auto, §1)`；记录 th13 → Mudgal 和外部 mudgal, Theorem 6.2 |
| 743、806、952、1137 | section_map 仅到 §5，且 completeness 称完全自包含 | 补列 §6、§7、附录 A/B；状态改 partial，撤销“完全自包含”和提取完整的断言 |

引用核对仅到本地引用上下文及书目：gmt 在 1194 行，kv 在 1201 行，madiman 在 1227–1228 行，mudgal 在 1235–1236 行，samorodnitsky 在 1252 行，tao-entropy 在 1262 行，tao-vu 在 1263–1265 行。这不等于独立核对了这些论文的定理内容。

## Behrens：六个主结果与空实体表

`behrens.tex` 的 thm:sat（223–231）、indsat_paw（373–375）、paw_unique（380–382）、sis paw（427–439）、cor:stars（630–632）及 bound:stars（637–639）与六项主结果逐项对照。星图阈值分别确为 `n ≥ 3^k` 与 `n ≥ 2·3^k`，paw 的分段公式也与原文相符，不改其数值。

原 paw_unique 写成 `Construction 3.1`，缺乏已核实的编译编号；现在引用原文 `\ref{cons:paw}`，构造在 346–349 行。六个 `statement` 使用实际生效的 TeX 陈述，排除 `%` 注释中的旧版本。尤其 519–583 行位于 `comment` 环境中，不能因看见 theorem/lemma 标签就当作当前正文结果。

`entities` 仍为空：它意味着尚未提取依赖图。`merge_status` 改为 partial，不计算或宣称“无依赖、无环、全文自包含”。section_map 也尚未覆盖原文全部章节。MS、KT、EHM 的引用上下文在 222–229 行，书目分别在 1933–1935、1924–1926、1906–1909 行；本次未打开外部原作。

## 原文疑似笔误与局部补推导

以下与“JSON 抽取漏条件/错边”分开处理。原 `.tex` 保留作者写法；这些是本次核对给出的纠正候选，不代表作者发布了勘误，也不是对整篇证明的认证。

| 原文位置 | 原文文字/公式 | 局部依据与纠正候选 |
|---|---|---|
| pfr2-submit.tex:1127，bsg-25 | `H(A_2,B_1) ≤ H(A) − H(B)` | 由边缘分布相同和熵次可加性，只能在此直接得到 `H(A_2,B_1) ≤ H(A)+H(B)`。用这个加号界与 1122、1124、1117–1118 行合并，得 `H(A_1−B_2) ≤ 2I(A:B)+H(Z)`，恰是 1129 行。此局部推导支持把减号改为加号的候选；未改原文。 |
| behrens.tex:415 | “at most one nontrivial component” | 其理由只排除两个孤立点：给两孤立点加边只生成一个 K2 分量，不会生成 paw。因此候选是“at most one trivial component”；与 347 行构造一致。不能把原文字面当成“至多一个非平凡分量”的新定理。 |
| behrens.tex:423 | “at most two parts of order one” | 紧接着用两个单点部讨论删边，欲排除的正是两个单点部；347 行构造要求至多一个。候选是“at most one”。本次只记录局部理由与冲突，不替作者改定稿。 |
| behrens.tex:452–456 | “at least three parts” 时合并两个部，随后断言最小图为 tripartite | 三个部合并后只剩两个，不再满足 347 行构造；四个或更多部合并才保留至少三部。候选是“more than three parts”。该局部操作解释了这里的数量条件，未重新验证整个极小边数证明。 |

## 实际计算及结果

读取当前两个 JSON，用 `python3 - <<'PY'` 内联运行标准库 `json`、`collections.deque` 和 `pathlib.Path`：以 labels 建索引，只把 `dependencies` 转为前置项 → 使用者的边，反算 `cited_by` 和度数，用 Kahn 顺序检查环，并沿该顺序计算最长路径。未新建检查脚本、测试目录或依赖。

实际输出：

```text
gowers2024_marton_structure.json
  entities=17; confirmed_edges=18; uncertain_entries=0
  dangling=[]; reverse_or_degree_mismatches=[]; cycle=False
  longest path: 8 vertices, 7 edges
  shared_nodes=['Theorem 1 (pfr)']
behrens_induced_saturation_structure.json
  entities=0; graph unavailable (partial extraction); no graph conclusions
```

共享节点使用本流程定义：直接使用者至少两个，且至少一个类型为 THEOREM。完整计算表和实际 18 条边已同步到 [现有 Gowers 图](Gowers_PFR_全局依赖图_2026-05-15.md)。当前索引中没有某个 label，不足以否定依赖，须回原文检查别名或漏项；本次调整依据的是上表的原文使用位置。

另用标准库读取 Mermaid 节点/边和 Markdown 表，与当前 JSON 比较，实际输出 `Current Mermaid: 17 nodes; 18 edges; edge set and all degree rows agree with JSON.`。`git diff --check` 退出码为 0；`git diff --name-only -- skills/math-paper-reading/examples/paper` 没有输出，原文文件没有修改。

旧笔记的局部修正：Gowers 长笔记中把猜想和定理拼接的“逐字原文”拆开，单列标签 pfr 的原文和 pfr-conj 的摘要；熵定理的省略式改标摘要。Behrens 笔记的整理式陈述也改标摘要，并去掉未核实的 Construction 3.1 编号。Gowers 旧证明路径中，Ruzsa 距离定义补明使用独立副本（原文 243–248 行）。三份长笔记均在顶部说明剩余内容尚未全部复核。

范围限制：没有逐行重证整篇论文，没有完成全部定义/熵事实/应用的提取，没有独立验证外部结果或出版元信息，也没有重新编译页码。图没有环、数值一致，不等于数学证明成立。两份旧 Gowers 长笔记/路径和 Behrens 长笔记仅作为历史示例保留，未随本次核对全部更新。
