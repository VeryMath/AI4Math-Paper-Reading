# Extraction Protocol

Use this protocol when extracting skills from a math paper.

## Goal

Extract reusable mathematical research skills, not summaries. A valid skill is a portable method with inputs, outputs, assumptions, steps, triggers, limitations, and source evidence.

## Procedure

1. Establish line numbers from the Markdown source. Use 1-based inclusive line references.
2. Scan the paper for high-value spans:
   - theorem, lemma, proposition, corollary, assumption;
   - proof blocks;
   - convergence, stability, error analysis, generalization, lower bound, and appendix proof sections.
3. For each span, ask:
   - What proof technique is being used?
   - Is this technique reusable outside this paper?
   - What must be given as input?
   - What does the technique produce?
   - Which assumptions are essential?
   - What could go wrong if the assumptions are missing?
4. Convert reusable spans into `SkillCandidate` records.
5. Generalize paper-specific wording:
   - Replace named paper algorithms with generic algorithm classes.
   - Replace local assumption numbers with semantic assumptions.
   - Replace local theorem numbers with generic proof targets.
   - Keep mathematical conditions such as smoothness, coercivity, boundedness, convexity, mesh regularity, and independence.
6. Score and classify candidates with `quality_rubric.md`.
7. Generate Skill Cards for accepted and review-worthy candidates.

## Rejection Rules

Reject a candidate if it is:

- only a result statement, not a method;
- purely introductory or related work;
- an experiment, ablation, implementation detail, or empirical observation;
- too paper-specific to transfer;
- missing core assumptions so badly that the method cannot be safely described.

## Needs Review Rules

Use `needs_review` when the method is probably reusable but:

- the paper omits a condition that may be essential;
- a step relies on a domain-specific theorem not fully stated in the source span;
- notation is ambiguous;
- the extracted skill is broad and should be checked by a domain expert.

## Evidence Requirements

Every candidate must include:

- `source.paper_md`;
- `source.start_line`;
- `source.end_line`;
- a short `source_span` string;
- enough source text in the report or notes to let a reviewer locate the proof idea.
