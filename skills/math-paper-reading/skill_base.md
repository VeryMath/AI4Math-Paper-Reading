---
name: math-paper-structure
version: 4.2
description: >
  数学研究论文的内容结构分析。触发条件：用户上传或粘贴数学论文（PDF/Markdown/纯文本），
  并要求进行以下任意一种操作——章节结构梳理、定理/引理/定义提取、证明框架构建、
  证明依赖关系分析、证明完整性审查、生成结构报告。
  关键词触发："结构分析"、"证明框架"、"定理提取"、"依赖树"、"引理关系"、
  "证明骨架"、"章节地图"、"proof structure"、"structural analysis"。

  【本 skill 不做的事】
  - 用通俗语言重新解释定理含义（→ 论文解读模块）
  - 分析论文中的图片/Figure 内容（→ 图片分析模块）
  - 文献检索与引用推荐（→ 文献检索模块）
  - 验证数学证明的正确性（超出 AI 结构分析能力范围）
  - 解读依赖路径的数学意义（→ 内容分析模块）

  【对外输出接口】
  本 skill 的 JSON 是可纠正的结构索引，各模块沿用以下字段：

  - skill_literature_search：
      paper.title / paper_summary / paper.arxiv_id / paper.authors / paper.year
      main_theorems[].statement / related_work[].result_summary
      completeness_check.external_deps

  - skill_paper_deep_read：
      section_map / main_theorems / entities[] / proof_framework
      completeness_check / uncertain_log

  - skill_pathway_proof：
      entities[].dependencies / entities[].cited_by
      entities[].uncertain_dependencies / entities[].external_refs
      entities[].shared_node / entities[].auto_labeled
      completeness_check.isolated_results / completeness_check.circular_deps
      proof_framework.dependency_tree

  - skill_reference_manager：
      paper.title / paper.authors / paper.year / paper.venue
      paper.arxiv_id / paper.paper_type / paper_summary
      main_theorems[].statement / related_work[]

  论文原文是依据。各模块发现有来源支持的遗漏或错误时，可直接修正 JSON，
  说明修改内容与原文位置，并同步相关 MD 和派生图；用户注释仍保留在对应字段。
---

# Math Paper Structural Analysis v4.2

## 概述

本 skill 对数学研究论文进行**结构性分析**，记录原文陈述及其引用关系，不生成新数学结论。原文未明确支持的解释或依赖须标明不确定性。

**依据与范围**：论文原文（包括公式、图表和附录）是判断依据；JSON、MD 和依赖图都是可修正的分析结果。任一阶段发现遗漏、误读或错误分类，都应回看相关原文后增删或修正，不必返回某个阶段重新开始。文件彼此一致只说明记录同步，不能证明数学陈述或证明正确。

**完整结构报告的建议流程**（可随原文核查修正前面的记录）：
```
论文原文
   │
   ▼
[S1] 结构速览与章节地图
   │ 输出：元信息 + section_map + 复杂度估计 + 主定理预清单
   ▼
[S2] 数学实体抽取
   │ 输出：实体的结构化 JSON 索引
   ▼
[S3+4] 证明框架构建 + 结构覆盖核查（结合原文）
   │ 输出：依赖树 + 证明策略 + 时间线 + 完整性报告
   ▼
[S5] 输出交付物
      输出：.md 结构报告 + .json 结构化数据
```

---

## 被其他模块调用时的执行规范

当其他模块（skill_paper_deep_read / skill_literature_search / skill_reference_manager）
需要为某篇论文生成或补充结构索引时，按用户问题选择范围：

**调用入口**：用户已提供论文全文（PDF / 粘贴文本 / arXiv 链接）

**执行范围**：
- 局部问题可直接阅读有关章节、定理和证明；没有 JSON 时，不要求先完成全文提取。说明本次覆盖范围及尚未核查的部分。
- 请求完整结构索引时，执行 Skill 1 + Skill 2 + Skill 5；调用方需要证明框架时加入 Skill 3+4。
- 已有 JSON 时先用它定位原文；回答所需的陈述和依赖仍须核对原文。来源暂不可取得时，说明依据仅为现有索引及其限制。

**调用后输出**：
- 按请求生成或更新 `<slug>_structure.json`，局部问答不强制生成文件。
- 生成文件时简述覆盖范围、实体数及未解决的问题；不得把局部提取描述为全文完成。

调用方可复用已核查记录，并按当前问题继续查阅原文；不必重复全文流程。

---

## 来源与记录要求

以下要求适用于本次分析范围内的记录。输出前核对适用项；未覆盖的内容应说明范围，不用补造条目。

### C1 — LaTeX 符号强制要求

所有数学符号必须用 LaTeX，禁止任何纯文本近似：

| ❌ 禁止 | ✅ 正确 |
|---|---|
| `K1,3` / `K1,k+1` / `2K2` | `$K_{1,3}$` / `$K_{1,k+1}$` / `$2K_2$` |
| `C4` / `C5` | `$C_4$` / `$C_5$` |
| `indsat(n,H)` / `indsat*(n,H)` | `$\text{indsat}(n,H)$` / `$\text{indsat}^*(n,H)$` |
| `n >= 7` / `n <= k` | `$n \geqslant 7$` / `$n \leqslant k$` |

行内公式用 `$...$`，独立公式用 `$$...$$`。

### C2 — 定理陈述必须逐字引用

记录任何 **定义/引理/命题/定理/推论/构造/Claim** 的陈述时，必须从论文中**逐字复制原文**，禁止意译、总结或简化。陈述跨多行则全部复制。

保留假设、量词、参数范围和全部条款，并给出节、页或标签位置。PDF 换行、空白和 LaTeX 排版可整理，但不得改变数学内容；OCR 有歧义时回看原页，仍无法确认则标 `[UNCERTAIN]`。解释性摘要须与原文引用分开。

> ⚠️ **Skill 1 边界**：Skill 1 阶段只记录定理标签和一句话作用，**不写完整陈述**。完整陈述在 Skill 2 中提取。

Skill 1 章节总结中允许事实性意译（说明"这节做了什么"），但定理/引理的编号标签和节标题本身仍须逐字。

**图片中的构造**：若构造仅出现在 Figure 中，写 `（完整结构见原文 Figure X，由图片分析模块处理）`。

### C3 — 不确定性必须显式标记

以下情况在行内写 `[UNCERTAIN: <原因>]`，不猜测：
- 陈述在原文中被截断或模糊
- 依赖关系为推断（无明确引用句）→ 写入 `uncertain_dependencies`
- 引用了外部文献但本文未重新证明 → 改用 `[EXTERNAL: 文献标签]`

| 支撑程度 | 处理方式 |
|---|---|
| 有明确引用句（"by Lemma 2.3"） | 写入 `dependencies`，无需标注 |
| 上下文暗示，无明确引用句 | 写入 `uncertain_dependencies`，标 `[UNCERTAIN: 上下文推断]` |
| 完全无上下文支撑 | 不写任何依赖字段，在 `uncertain_log` 中记录 |

不确定性由实际证据决定，不设数量下限。没有发现不确定项时可写“本次核查未发现”，并注明核查范围；不得为满足数量要求制造疑点。

### C4 — 禁止捏造依赖关系

无明确文本依据（"X 的证明使用了 Y"）不写依赖，遵照 C3 的优先级表处理。

### C5 — 多条款陈述禁止省略

定理/引理/命题/构造含多个编号条款时，必须完整列出所有条款，每条独立成行，不得用 `...` 省略。

### C6 — 多证明变体必须分别记录

同一定理/引理存在多个证明时，在 `proof_methods` 中用 `proof_variant: 1/2/...` 区分，每个变体单独记录方法、关键工具和位置。

### C7 — 子节必须独立列入 section_map【v4.2 新增】

任何有编号的子节（如 §5.1、§1.3、§4.2）若**包含命名的定理/引理/构造/定义**，必须在 section_map 中**独立列出**，不得合并到父节。

示例：论文有 §5 和 §5.1 两层，§5.1 含 Proposition 5.6，则 §5 和 §5.1 各自独立列出。

### C8 — related_work 的作者、年份与覆盖范围须有来源

`related_work` 条目的 `authors` 和 `year` 从论文参考文献列表提取实际值。原文未提供或不可辨认时，可省略该字段或写 `null`，并在 `uncertain_log` 中注明原因；不得猜测作者或年份。

**完整结构报告的 related_work 收录范围**：核查下列引用是否已纳入 `related_work[]`：
1. 论文"相关工作"节中对比的外部结论
2. 正文证明中作为**核心工具**直接引用的外部定理（原文写明"by [X]"、"using [X]"且该结论直接参与推导）
3. 摘要或引言中明确提及的背景工作

仅作为脚注说明或补充说明引用的文献（如"see [X] for more details"）不强制纳入，但建议收录。

**论文无独立相关工作节时的处理**：引用散落在正文各处时，按以下优先级扫描全文补全 `related_work[]`：
- 第一优先：摘要和引言中被命名的外部结论（如"X proved that..."形式）
- 第二优先：正文证明中被 `[X]` 标注且原文明确写"by [X]"/"using [X]"的外部定理
- 第三优先：与本文核心参数定义直接相关的已有结论（如本文 $\text{indsat}$ 的定义来源）

**覆盖核查**：对照摘要、引言、相关工作和证明中实际出现的引用，检查上述范围内的工作及其作用是否被记录。条目数不与参考文献总数设固定比例；局部分析仅说明已查章节和未查范围。

### C9 — 节内主定理 role 判断规则【v4.2 新增】

`role` 字段的判断依据是**论文原文的明确语句**，不是全局结构猜测：
- 原文明确说 "main result of this section"，或在贡献说明中突出该结论 → `"role": "main"`
- 该结论仅作为辅助工具服务于另一定理 → `"role": "supporting"`
- 该结论直接从另一定理推出 → `"role": "corollary"`

即使某定理在全局看属于支撑性，若它是本节的核心贡献，仍标 `"main"`。

仅写 "we prove the following theorem" 不能单独证明它是主结果；结合原文的贡献说明判断，依据不足时说明不确定性。

**Corollary 纳入 `main_theorems[]` 的判断规则**：满足以下任意一条，Corollary 应写入 `main_theorems[]`（`role: "corollary"`），不得仅留在 `entities[]`：
- 论文摘要或 §1.x 概述中明确列出该 Corollary 为贡献之一
- 该 Corollary 给出本节核心定量结论（精确公式、精确值），而其来源定理只给出充要刻画或定性结论

不满足以上条件的 Corollary 仅保留在 `entities[]` 中即可。

主定理预清单只是初步定位，不能单独作为纳入或保留某条目的依据。后来发现角色判断有误时，按原文修正并说明位置和原因。

---

## Skill 1 — 论文结构速览与章节地图

全流程第一步。通读全文，**按实际节顺序**（不跳过任何一节）生成章节地图。

### 输出格式

#### 元信息块
```
标题：
作者：
来源（期刊/会议）：
年份：
arXiv 编号（如有，否则留空）：
语言：EN / CN / 其他
分析日期：YYYY-MM-DD
```

#### 论文类型（可多选，注明判断依据）
纯证明型 | 计算辅助型（含 computer search/穷举表格） | 构造型（主要贡献是构造） | 综述/调查型

#### 复杂度估计
```
结构元素估计数：约 X 个（定理/引理/定义合计）
证明方向数：X 个
计算机搜索参数范围：（如有）
skill-2 耗时预估：低(<10) / 中(10-30) / 高(30-50) / 极高(>50)
```
> 极高复杂度时：分批执行 Skill 2，每批处理一个主节，每批头部标注 `[BATCH X/N]`。

#### 章节地图总览表
| 节编号 | 标题 | 节类型 | 核心动作（一句话） |
|---|---|---|---|
| §X | ... | ... | ... |

节类型选项：引言 / 相关工作 / 预备知识 / 主要结果 / 构造节 / 证明节 / 计算/实验 / 讨论 / 结论 / 附录（可标复合类型）

> **⚠️ "主要结果"判断边界**：节类型"主要结果"仅用于**本文新证明**的结论所在节。若某节内容全部来自外部文献（如标题含"Previous Results"、"Background"的节），应标为"相关工作"或"预备知识"，不得标为"主要结果"。若节内同时含外部结论和本文证明（如本文 Proof of Observation），可标复合类型。MD 与 JSON 中的 `section_type` 必须一致。

#### 主定理预清单（初步定位，后续可修正）

列出全文所有预期的主定理/主推论标签，格式：

```
主定理预清单（初步）：Theorem X.X, Corollary X.X, ...
```

后续按原文的贡献说明和实际陈述修正候选列表。最终纳入 `main_theorems[]` 的条目，应在 MD §2 有陈述、位置、证明方法和地位说明；遗漏或误列均可直接修正，并在普通修改说明中写明依据。预清单不限制后续发现。

#### 每节详细总结（内联格式）

对每个节/子节（含所有 §X.Y 层级），用以下单一格式输出（不区分节类型，不切换模板）：

```
§X.Y  [标题]
节类型：[类型]
核心动作：<1句，说明本节做了什么>
关键标签：<本节所有命名结论的编号，仅列标签>
主要构造：<Construction X.X：一句描述>（如有）
关键引用：<本节引用的外部文献标签>（如有）
skill2_action：正常提取 / 无需处理 / 提取 proof_variant:2
```

**相关工作节 JSON 映射**：若本节为"相关工作"类型，将提取的"核心对比结果"逐条写入 JSON 的 `related_work[]` 数组，格式：
```json
{ "ref": "[编号]", "authors": "...", "year": ..., "result_summary": "..." }
```

> 禁止：推断作者意图、评价证明优劣、写出定理完整陈述（C2 Skill 1 边界）。

---

## Skill 2 — 数学实体抽取

按本次范围的节顺序扫描原文，提取命名结构元素；需要保存时沿用下文 JSON 字段，不另建格式体系。完整报告覆盖全文，局部分析注明所查章节和标签。

**提取对象类型**：
DEFINITION / LEMMA / PROPOSITION / THEOREM / COROLLARY / CONSTRUCTION / CLAIM / OBSERVATION / REMARK

**CLAIM 处理**：证明内部无编号局部断言，用 `Claim-[父标签]-[序号]` 自动命名（如 `Claim-Theorem3.4-1`），标注 `"auto_labeled": true`。

**多条款处理（C5）**：含 (1)(2)(3)... 的定理/引理，statement 字段中各条款用 `\n` 分隔，完整列出。

**极高复杂度（>50实体）**：分批执行，每批一个主节，批次头部注明 `[BATCH X/N — §Y]`。

### 分批合并与图计算

合并实体、重建反向索引和计算图属性时，调用代码工具或现有函数精确计算；可直接在工具中运行，不要求生成或落盘脚本。

1. 读取本次实际处理的批次或已有实体。以 `label` 定位重复项，结合原文位置处理冲突，不能直接覆盖不同陈述。
2. 仅从有明确原文依据的 `dependencies` 重建 `cited_by`：B 的 `dependencies` 包含 A，表示前置结果 A → 使用它的结论 B；A 的 `cited_by` 包含 B，并去重。`uncertain_dependencies` 和外部依赖单独保留，不混入已确认图的度数或拓扑计算。消费者使用度数时，B 的 `in_degree` 为有效确认前置数，A 的 `out_degree` 为 `len(A.cited_by)`。
3. 沿用 `shared_node` 的计算约定：`cited_by` 至少含两个实体且其中至少一个为 `THEOREM` 时设为 `true`，否则为 `false`。它表示当前引用图中的共享使用，不代表数学重要性或证明正确性。
4. 保存时沿用 `<slug>_structure.json` 和 `merge_status`。只有本次计划处理的批次均已合并时才写 `complete`；仍缺批次时注明已处理范围，不补造内容。

简述实际执行的计算与结果即可，不必在对话中打印完整 JSON。代码计算只检查给定记录的图关系，不能替代逐条回看原文。

---

## 分析过程中的修正

在实体提取、证明框架、精读和交付阶段均可依据原文增删或修正实体、主定理、依赖及分类。采用以下普通修改说明即可，不设锁定点或回退重走要求：

- 说明改了什么、为何修改，以及对应原文的节、页或标签；确认的错误修正不必写成不确定项。
- 同步 JSON、MD 中受影响的陈述、列表和引用；保留用户已有的 `user_notes`、`user_edits`。
- 依赖或实体变化后，重新计算相关 `cited_by`、`shared_node` 及消费者使用的度数和拓扑，并更新依赖树和其他派生图；不确定边继续单独标注。
- 原文不可取得时不凭索引冲突决定哪一份正确，说明待核查位置和当前限制。

MD 和 JSON 可以先后生成或同步整理；两者均需对照原文核查，不能因为来自同一份数据就宣称检查通过。

---

## Skill 3+4 — 证明框架构建与结构覆盖核查

用实体索引定位相关证明，回看原文中的引用句、假设和证明段落，完成以下工作。发现索引缺漏或误读时直接修正，并同步受影响记录。

### 3a. 定理关系图（多主定理时必须输出）
说明各主定理之间的依赖或独立关系，共享基础引理用 `*` 标注。

### 3b. 依赖树（ASCII 缩进，带类型标注）

树从目标定理向下展开它的前置结果，缩进表示查阅顺序；图中的箭头仍按“前置结果 → 使用它的结论”绘制。未确认依赖另行标记，不混入确认树。

```
[THEOREM] 主定理
├── [LEMMA] X（直接引用）
│   └── [DEFINITION] Y *（共享节点）
├── [CONSTRUCTION] Z
└── ([Claim-主定理-1])
```

### 3c. 结构化证明策略
按方向分别说明（充分性/必要性/上界/下界）：
```
[方向]：策略 | 关键工具（引用标签）| 分类/构造对象（如有）
```

### 3d. 证明时间线

| 步骤 | 标签 | 建立的性质（逐字） | 方法（具体） | 证明位置 | 被使用于 |
|---|---|---|---|---|---|
| 最终 | 主定理 | \<逐字结论\> | — | — | — |

### 3e. 证明策略摘要（意译，2–4句，此处允许意译）

### 4a. 依赖链完整性（每条一行）
```
✅ A → B：找到明确引用句
⚠️ C → D：上下文推断，已标 [UNCERTAIN]
❌ E → F：被引用但依赖来源缺失
```

### 4b. 外部文献依赖清单
自包含度：高 / 中 / 低
每条 `[EXTERNAL]` 一行，说明对主定理的影响程度。

### 4c. 孤立结论 & 循环依赖
各一行结论，或写"无"。

> **重要边界**：循环依赖检测的结论是「结构层面的循环引用」，
> 不等于「证明是循环论证」。是否构成逻辑谬误，由内容分析模块或人工判断。
> Skill 4 的输出仅为：「发现 A → B → A 的引用路径，建议人工核查是否为笔误或别名」。

### 4d. 完整性审查摘要（3–5句）

说明已查范围、缺失来源和未确定的依赖。“完整性”仅指所查原文与结构记录的覆盖情况，不是数学证明正确性验证。

---

## Skill 5 — 输出交付物

> **paper_summary 生成时机**：完整阅读后，根据原文研究问题和主要结果生成意译摘要（≤3句），可参考已核查的结构与证明策略记录。仅做局部分析时不补写未经核查的全文摘要。

完整结构报告生成以下两份文件；局部问答或仅请求索引时按请求交付，不强制补齐全文报告：

### 5a. Markdown 报告（`<slug>_structure_analysis.md`）

```markdown
# [论文标题] — 结构分析报告
**skill 版本**：4.2 | **分析日期**：YYYY-MM-DD

## 1. 元信息与章节地图
[Skill 1 完整输出]
[注明原文来源、实际核查范围；有修正时简述修改及原文位置]

## 2. 主定理
[每个主定理：标签 + 逐字陈述 + 证明方法 + 在论文中的地位]

## 3. 所有结构元素
### 3.1 定义
| 标签 | 陈述（逐字引用） | 位置 | 被哪些结论使用 | 备注 |

### 3.2 引理
| 标签 | 陈述（逐字引用，含全部条款） | 位置 | 依赖关系 | 被哪些结论使用 | 证明方法 |

### 3.3 命题
| 标签 | 陈述（逐字引用） | 位置 | 依赖关系 | 被哪些结论使用 | 证明方法 |

### 3.4 定理
| 标签 | 陈述（逐字引用，含全部条款） | 位置 | 依赖关系 | 证明方法 |

### 3.5 推论
| 标签 | 陈述（逐字引用） | 位置 | 来源 |

### 3.6 构造
| 标签 | 陈述（逐字引用，图片构造注明 Figure 编号） | 位置 | 被哪些结论使用 |

### 3.7 Claim（证明内部局部断言）
| 标签 | 所属父结论 | 陈述（逐字引用） | 位置 | 在证明中的角色 |

### 3.8 观察与注记
| 标签 | 类型 | 陈述（逐字引用） | 位置 | 被哪些结论使用 |

### 3.9 数值表格（如有）
| 表格标签 | 标题（逐字） | 数据来源 | 位置 |
完整数值：（原样复制所有行列）

## 4. 证明框架
[Skill 3+4 的 3a–3e 输出]

## 5. 完整性审查报告
[Skill 3+4 的 4a–4d 输出]

## 6. [UNCERTAIN] 日志
| 标签位置 | 不确定原因 | 严重程度（LOW/HIGH） |
（如果没有，写"无"）

## 7. 用户注释
### 7.1 总体备注
（用户在此处添加注释）
### 7.2 单条实体修订
（格式：**[标签]** 修订内容）
```

### 5b. JSON 文件（`<slug>_structure.json`）

**v4.2 精简写法**：沿用以下字段，空数组 `[]` 和 `null` 字段可省略。缺失可能表示未查或不适用，下游应结合覆盖说明判断，不能把缺失等同于已核实不存在。

```json
{
  "paper": {
    "title": "string",
    "authors": ["string"],
    "venue": "string",
    "year": 2024,
    "arxiv_id": "string | null",
    "source_file": "string | null（论文原文的本地路径或 arXiv URL；若原文仅存在于当次对话上下文中写 null）",
    "language": "EN | CN | other",
    "analysis_date": "YYYY-MM-DD",
    "skill_version": "4.2",
    "paper_type": ["纯证明型 | 计算辅助型 | 构造型 | 综述型"],
    "complexity_estimate": {
      "entity_count_estimate": 0,
      "proof_directions": 0,
      "skill2_effort": "low | medium | high | very_high"
    }
  },
  "section_map": [{
    "section": "§X.Y",
    "title": "string",
    "section_type": "引言 | 相关工作 | 预备知识 | 主要结果 | 构造节 | 证明节 | 计算/实验 | 讨论 | 结论 | 附录（可用 + 连接复合类型，须与 MD 节总结中一致）",
    "core_action": "string",
    "key_labels": ["string"],
    "skill2_action": "正常提取 | 无需处理 | 提取 proof_variant:2（JSON 中只写这三个枚举值之一，不得附加括号注释；注释仅允许出现在 MD 节总结的同名字段后）",
    "appendix": false
  }],
  "related_work": [{
    "ref": "[N]",
    "authors": "string | null（从参考文献列表提取，C8）",
    "year": null,
    "result_summary": "string"
  }],
  "paper_summary": "string（意译，≤3句）",
  "main_theorems": [{
    "label": "string",
    "short_title": "string",
    "statement": "string（逐字，多条款用 \\n 分隔）",
    "location": { "section": "string", "page": "string" },
    "proof_methods": [{
      "proof_variant": 1,
      "method": "string",
      "detail": "string",
      "location": "string"
    }],
    "role": "main | supporting | corollary"
  }],
  "theorem_relations": "string（多主定理时说明关系及共享引理）",
  "entities": [{
    "type": "DEFINITION | LEMMA | PROPOSITION | THEOREM | COROLLARY | CONSTRUCTION | CLAIM | OBSERVATION | REMARK",
    "label": "string",
    "statement": "string（逐字）",
    "location": { "section": "string", "page": "string" },
    "dependencies": ["string"],
    "uncertain_dependencies": ["string [UNCERTAIN: 原因]"],
    "cited_by": ["string"],
    "external_refs": ["string"],
    "proof_methods": [{
      "proof_variant": 1,
      "method": "string",
      "detail": "string",
      "location": "string"
    }],
    "parent_result": "string | null",
    "role_in_parent": "string | null",
    "shared_node": false,
    "auto_labeled": false
  }],
  "tables": [{
    "label": "string",
    "title": "string（逐字）",
    "data_source": "computer_search | formula | mixed",
    "location": { "section": "string", "page": "string" },
    "rows": [{ "parameter": "string", "value": "string", "source": "string", "open": false }],
    "open_values": [],
    "conjectured_values": []
  }],
  "proof_framework": {
    "center_theorem": "string",
    "theorem_relation_map": "string（ASCII，共享节点用 * 标注）",
    "dependency_tree": "string（ASCII 缩进树，含类型标注）",
    "proof_strategies": [{
      "direction": "充分性 | 必要性 | 上界 | 下界 | string",
      "proof_variant": 1,
      "method": "string",
      "object_constructed": "string | null",
      "case_split": "string | null",
      "key_tools": ["string"]
    }],
    "timeline": [{
      "step": 1,
      "label": "string",
      "establishes": "string（逐字）",
      "method": "string（具体）",
      "location": "string",
      "used_by": ["string"]
    }],
    "strategy_summary": "string（意译，≤4句）",
    "backquery_requests": [{ "label": "string", "reason": "string", "skill4_conclusion": "string" }]
  },
  "completeness_check": {
    "dependency_integrity": [{ "edge": "A → B", "status": "ok | missing | external", "note": "string" }],
    "self_containment": "high | medium | low",
    "external_deps": [{ "label": "string", "ref": "string", "impact": "string" }],
    "isolated_results": [{ "label": "string", "possible_reasons": ["string"] }],
    "circular_deps": [],
    "backquery_results": [{ "label": "string", "status": "ok | warning | missing", "note": "string" }],
    "summary": "string（3–5句）"
  },
  "uncertain_log": [{ "location": "string", "reason": "string", "severity": "LOW | HIGH" }],
  "source_warning": "string | null（说明原文不可取得或来源位置不明对本次核查的限制）",
  "merge_status": "complete | partial（说明已覆盖与未覆盖范围；批次合并完成不等于全文或数学验证完成）",
  "user_notes": "",
  "user_edits": {}
}
```

---

### 5c. 原文核查与交付物同步

先对照论文原文检查本次范围内的陈述、分类、引用和覆盖，再核对 MD、JSON 与派生图是否同步。冲突时回到相关原文，修正有误的记录；JSON 不优先于原文。两份文件一致不代表内容已获数学验证。

**必须逐项核对的字段**：

| 检查项 | JSON 字段 | MD 对应位置 | 核查要求 |
|---|---|---|---|
| 主定理列表 | `main_theorems[].label` | §2 主定理列表 + 初步预清单 | 按原文贡献说明核对纳入与分类；修正后的列表同步，候选列表可增删 |
| 主定理陈述 | `main_theorems[].statement` | §2 每条主定理的原文陈述 | 对照原文核查假设、量词、参数与全部条款；允许换行和排版差异，不做字符比较 |
| 节类型 | `section_map[].section_type` | 逐节详细总结的“节类型”行 | 分类有原文依据，两处表达同一判断 |
| 实体覆盖 | `entities[]` | §3 各子表 | 对照已查原文的命名结论和局部断言排查遗漏、重复、误提取；合计相等只辅助发现不同步 |
| UNCERTAIN 条目 | `uncertain_log[]` | §6 [UNCERTAIN] 日志表 | 实际未解决的问题及状态同步，不设条目数量要求 |
| 外部依赖 | `completeness_check.external_deps[]` | §5 外部文献依赖清单 | 回看引用句与参考文献，确认标签、来源和作用后同步 |
| 孤立结论 | `completeness_check.isolated_results[]` | §5 孤立结论 | 只对已查范围作判断，结合原文排除漏边和别名 |

**MD 允许有、JSON 不需要的内容**（不视为不一致）：
- 节总结的叙述性段落（研究问题、背景动机等）
- `skill2_action` 字段后的括号注释
- 用户注释区（§7）

**发现问题时**：依据原文修正相关 JSON、MD 和派生图，用普通修改说明记录改动、理由和原文位置；只有仍未解决的疑点进入 `uncertain_log`。不得为了文件对齐保留已知错误。

---

## 输出前核查清单（按本次范围适用）

### 格式与约束
- [ ] 所有数学符号已用 LaTeX，无裸符号（C1）
- [ ] 所有实体陈述为逐字引用，非意译（C2，Skill 2 起）
- [ ] 多条款定理全部条款完整列出，无 `...` 省略（C5）
- [ ] CLAIM 已提取；无编号 CLAIM 已自动标签并标注 `auto_labeled: true`（C3）
- [ ] 推断依赖已写入 `uncertain_dependencies`，标 `[UNCERTAIN]`（C3/C4）
- [ ] 外部文献依赖已标 `[EXTERNAL]`（C3）
- [ ] 不确定项来自实际疑点；未发现疑点时已说明核查范围，未凑数

### 结构完整性
- [ ] 完整报告的 section_map 覆盖全部节，含所有有命名结论的子节 §X.Y；局部分析已注明范围（C7）
- [ ] related_work 的 authors 和 year 有来源，缺失信息已注明，未编造（C8）
- [ ] 每个主定理的 role 按 C9 规则判断，非机械标 supporting
- [ ] 已对照实际证明引用核查依赖；不确定边和外部依赖单独记录，未混入确认图计算
- [ ] 多主定理时已给出定理关系图（3a）

### 交付物
- [ ] 已按请求交付文件或局部回答，未把部分提取称为全文分析
- [ ] JSON `skill_version` 字段值为 `"4.2"`
- [ ] `user_notes` 和 `user_edits` 字段已保留（更新时不覆盖）
- [ ] JSON 中所有 `location.page` 为字符串类型（允许范围如 `"3–4"`）
- [ ] 已按 5c 对照原文核查，并同步相关 MD、JSON 和派生图；未把文件一致称为数学正确
- [ ] 主定理纳入与角色以原文为据，预清单有误时已修正并说明依据
- [ ] related_work 已按实际引用及其作用核查覆盖，未按固定比例凑数（C8）
