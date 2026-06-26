# Paper-to-Skill Report

## Paper Information

- Input: `paper.md` from arXiv `2602.05174v1` (omitted from this example package)
- Output directory: `outputs/2602.05174v1` in the original run
- Extraction mode: Codex-assisted
- Number of extracted candidates: 7

## Extracted Skill Candidates

| Skill | Type | Score | Source | Status |
|---|---|---:|---|---|
| `tv_transport_stability_identity` | proof_pattern | 4.60 | `paper.md:285-595` | accepted_candidate |
| `manifold_euler_parallel_transport_interpolation` | proof_pattern | 4.35 | `paper.md:313-919` | needs_review |
| `jacobi_field_step_size_invertibility` | proof_pattern | 3.80 | `paper.md:337-1116` | needs_review |
| `tv_rate_term_aggregation` | proof_pattern | 4.40 | `paper.md:1121-1190` | accepted_candidate |
| `manifold_score_regularity_reduction` | proof_pattern | 3.20 | `paper.md:375-3272` | needs_review |
| `spd_curvature_moment_regularization` | proof_pattern | 3.15 | `paper.md:1336-3682` | needs_review |
| `related_work_narrative` | proof_pattern | 1.30 | `paper.md:86-98` | rejected |

## High Confidence Skills

- `tv_transport_stability_identity`: central, clean, and highly reusable transport-stability proof pattern.
- `tv_rate_term_aggregation`: clear recipe for turning local estimates into an end-to-end TV rate.

## Needs Review

- `manifold_euler_parallel_transport_interpolation`: useful but depends on invertibility of the Exp-step map.
- `jacobi_field_step_size_invertibility`: technically strong but requires domain-expert review of curvature and cut-locus assumptions.
- `manifold_score_regularity_reduction`: broad extraction spanning several geometry-specific lemmas.
- `spd_curvature_moment_regularization`: useful for SPD/Hadamard cases, but not generally portable without checking moment and curvature assumptions.

## Rejected Candidates

- `related_work_narrative`: rejected because it is literature positioning rather than a proof pattern.

## Notes

- Mathematical risk: several candidates rely on intrinsic differential-geometry conventions, including divergence, parallel transport, Jacobi fields, and comparison theorems. Misstating tangent-space locations or cut-locus assumptions would invalidate the proof.
- `paper.md` has been preserved in this output directory.
- Skill Cards were written only for accepted and review-worthy candidates.
