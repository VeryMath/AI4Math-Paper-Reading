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

Merge candidates when they share the same operational method and differ mainly by notation, paper-specific names, or minor assumptions.

Do not merge when:

- Assumptions are incompatible.
- Outputs prove different types of statements.
- One candidate needs a condition absent from the other.
- Evidence is too weak to support the generalized form.

## Status Labels

- `ready_for_library`: strong evidence from one or more papers, clear reusable steps, stable assumptions.
- `needs_human_review`: promising but has assumption, notation, or proof-safety uncertainty.
- `too_specific`: tied to one paper's model or theorem.
- `duplicate`: redundant with a stronger merged skill.
- `unsafe_generalization`: over-generalized or missing critical assumptions.

## Generalization Safety

Keep the strongest common safe statement. If one source has a weaker assumption and another has a stronger assumption, state the weaker condition only if the evidence supports it directly.
