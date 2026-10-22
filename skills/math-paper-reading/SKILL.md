---
name: math-paper-reading
description: Read mathematical papers from their source text, using correctable structure indexes for theorem extraction, dependency analysis, proof explanations, literature queries, and reference notes.
---

# Math Paper Reading

Start with [agent_router.md](agent_router.md) and load only the modules needed
for the user's current task. A full-paper extraction is optional for a local
question or a targeted literature query.

Resolve module references relative to this package. Read papers from their
actual supplied locations and save working outputs in the user's project;
do not treat the package's examples or reference database as user data.

## Modules

- [skill_base.md](skill_base.md): extract statements, assumptions, locations,
  and source-supported dependencies into a working JSON index.
- [skill_pathway_proof.md](skill_pathway_proof.md): compute dependencies and
  reading paths; keep confirmed, uncertain, and external edges distinct.
- [skill_paper_deep_read.md](skill_paper_deep_read.md): explain the paper and
  separate source text, additional derivations, and unresolved proof steps.
- [skill_reference_manager.md](skill_reference_manager.md): maintain reference
  metadata and user notes without treating extracted claims as verified facts.
- [skill_literature_search.md](skill_literature_search.md): build source-linked
  queries and distinguish proposed searches from retrieved evidence.

## Source and correction rules

- Use the original paper to check what its authors state, assume, and cite.
  JSON is a correctable index, not mathematical ground truth.
- Consult the relevant source passage whenever a statement, condition, or edge
  is uncertain or disputed, even when a JSON index already exists.
- Correct source-supported extraction mistakes in the current index. Explain
  the source location and the correction, then update affected reports and
  graph calculations. Do not require entity locks or a full workflow restart.
- Keep source quotations separate from interpretation and Agent-proposed
  derivations. Retain unresolved gaps and suspected author errors explicitly;
  do not silently repair a quotation or declare proof completion.
- For a confirmed dependency, `B.dependencies` containing `A` means the graph
  edge `A -> B`. Rebuild `cited_by` from these confirmed edges. Uncertain or
  external references do not contribute to confirmed internal graph degrees.
- Use available code tools or existing functions for exact graph calculations;
  do not require generating a helper script merely to proceed.
- Preserve user notes and state the checked scope. Package examples are not
  user data; graph consistency is not a proof of mathematical correctness.
