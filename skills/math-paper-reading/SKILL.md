---
name: math-paper-reading
description: Route mathematical paper-reading tasks through structured extraction, dependency analysis, deep reading, literature search, and reference management modules.
---

# Math Paper Reading

Use this skill when a coding agent needs to read, structure, explain, trace, or
manage mathematical papers with a data-driven workflow.

## Entry Point

Start with `agent_router.md`. It is the master router and decides which
package-local module to load:

- `skill_base.md`: extract definitions, lemmas, theorems, proofs, and
  dependency structure into JSON.
- `skill_pathway_proof.md`: compute dependency paths and render proof graphs.
- `skill_paper_deep_read.md`: provide layered paper reading and gap filling.
- `skill_reference_manager.md`: maintain the local paper reference database.
- `skill_literature_search.md`: generate targeted literature-search strategies.

## Operating Rules

- Keep fact extraction separate from interpretation.
- Prefer structured JSON evidence before graph, reading, or reference updates.
- Use package-local examples only as examples; do not treat them as user data.
- For complex dependency or merge tasks, write and run scripts instead of
  estimating manually.

Prefer the router and package-local module files over this thin compatibility
entrypoint when executing a concrete workflow.
