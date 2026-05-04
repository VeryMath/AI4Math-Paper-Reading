# Related Paper Search Strategy

## Query Routes

- `problem`: exact mathematical problem, objective, equation, or setting.
- `method`: algorithm, proof method, estimator, relaxation, or decomposition.
- `theorem`: named theorem, rate, bound type, stability result, or convergence claim.
- `assumption`: smoothness, convexity, coercivity, monotonicity, regularity, distributional, or structural assumptions.
- `application`: domain where the same technique is used.
- `author_trail`: papers by seed-paper authors or frequent collaborators.
- `citation_trail`: papers cited by or citing seed papers.

## Source Priority

1. arXiv, OpenReview, conference proceedings, journal pages with open full text.
2. Author homepages and institutional repositories.
3. DOI pages or publisher pages for metadata only when full text is not open.
4. Secondary pages only when they point to a primary source.

## Relevance Tests

Classify `relation_type` as:

- `direct_extension`: builds directly on a seed paper, theorem, method, or setting.
- `same_problem`: studies the same problem with different methods.
- `same_method`: uses the same method or proof pattern on another problem.
- `theoretical_background`: supplies a theorem, lemma, or framework needed for understanding.
- `benchmark_only`: useful mainly for comparison, experiments, or positioning.

Reject or down-rank papers whose relation is only generic domain overlap.
