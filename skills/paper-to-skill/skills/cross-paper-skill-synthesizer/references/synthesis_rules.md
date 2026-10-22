# Cross-Paper Skill Synthesis Rules

## Cluster Signals

Cluster SkillCandidates by:

- Transferable intent.
- Mathematical inputs and outputs.
- Assumptions and applicability conditions.
- Core proof steps.
- Trigger keywords and theorem families.
- Source evidence similarity.

## Merge Policy

Merge candidates when they share the same operational method and differ mainly by notation or paper-specific names. First write a condition-and-conclusion comparison for every source; an apparently minor assumption can be essential.

Do not merge when:

- Assumptions are incompatible.
- Outputs prove different types of statements.
- One candidate needs a condition absent from the other.
- Evidence is too weak to support the generalized form.

## Status Labels

- `ready_for_library`: source conditions checked, merged statement independently checked, actual reuse recorded, and a failure boundary examined, with no unresolved material conflict.
- `needs_human_review`: promising but has assumption, notation, or proof-safety uncertainty.
- `too_specific`: tied to one paper's model or theorem.
- `duplicate`: redundant with a stronger merged skill.
- `unsafe_generalization`: over-generalized or missing critical assumptions.

## Generalization Safety

For a single-source carry-forward, source extraction scores may be retained with an explicit note that the synthesized wording has not been rescored. Preserve the source's applicability conditions, recalculate the weighted total, and align extraction `status` with the shared rubric. Do not treat inherited scores as independent verification or evidence for a broader claim.

Use sufficient conditions for the chosen argument. Taking the set intersection of two assumption lists can remove a condition needed by both routes. If one source has a weaker assumption and another has a stronger assumption, state the weaker condition only with a separate argument supporting it directly.

For different proof routes, record each route's conditions and its supported conclusion. Keep a `conflict_resolutions` entry with the source disagreement, decision, and mathematical evidence. Use `unresolved` when the issue remains open; do not promote that card.

Preserve the verification scope when merging. Two source extractions are not two successful reuses. A successful scalar computation is evidence for that case; promotion of a general theorem additionally needs an argument for the full statement. See the extractor's `references/quality_rubric.md` for the shared criteria.

## Worked Conflict and Failed Generalizations

The existing flow-stability sources use direct coupling/Gronwall and a differentiable-flow perturbation formula. Their common target can be checked by an integral Gronwall argument without requiring differentiability of the flow map. This relaxation needs that separate argument; it does not follow from deleting smoothness from the source assumption lists.

The same example rejects two plausible but false merges: dropping the Lipschitz amplification, and carrying a unit-interval bound to arbitrary final time without its time factor. Exact scalar solutions and results are in `../../../examples/auto_research_trial/flow_stability_validation.md`.
