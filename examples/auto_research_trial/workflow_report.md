# Auto Research Trial Workflow Report

This example preserves the full human-in-the-loop test flow for the Codex-native paper-to-skill workflow.

It starts from PDFs and preserves the full `paper.pdf -> paper.md -> Skill Card` evidence chain. MinerU folders, local `.env`, and other machine-local intermediate artifacts are intentionally excluded.

The interaction loop is:

```text
Codex output -> human feedback -> human_feedback_state.json -> next Skill uses state
```

## 0. Seed Papers

Seed PDF and Markdown papers:

- `seed_papers/2510.08929v1/paper.pdf`
- `seed_papers/2510.08929v1/paper.md`
- `seed_papers/2602.05174v1/paper.pdf`
- `seed_papers/2602.05174v1/paper.md`

These were used as the initial research-interest signals.

## 1. Seed Paper Profiling

Skill:

```text
seed-paper-profiler
```

Outputs:

- `research_profile.json`
- `human_feedback_state.json`
- `profile_review.md`

Purpose:

- infer target domain;
- identify core problems, methods, assumptions, proof patterns, and search directions;
- create a structured profile for retrieval and triage.

Human feedback applied:

- emphasize Wasserstein error, coupling bias, and reusable proof patterns;
- down-rank heavy-tailed priors as a standalone topic;
- down-rank purely empirical flow-matching papers unless needed for positioning.

## 2. Related And Innovation Paper Retrieval

Skills:

```text
related-paper-retriever
innovation-paper-finder
```

Outputs:

- `candidate_papers.json`
- `innovation_candidates.json`
- `retrieval_report.md`
- `innovation_report.md`

Purpose:

- find directly related papers;
- find papers that may provide new proof techniques, sharper assumptions, alternative theory, or cross-domain transfer ideas.

Human feedback state used:

- retrieval prioritized proof-technique, error-analysis, coupling, lower-bound, and regularity routes;
- speculative or application-only papers were kept lower unless they could support positioning.

## 3. Paper Triage

Skill:

```text
paper-triage-ranker
```

Outputs:

- `reading_plan.json`
- `triage_report.md`

Purpose:

- rank papers into reading priorities;
- create a confirmed `download_queue`;
- decide which papers should be downloaded and converted next.

Human feedback state used:

- proof-pattern value was weighted above topical proximity alone;
- `vES22INUKm` and `uqQPyWFDhY` were selected for download and extraction as high-value error-bound papers.

## 4. PDF Download

Skill:

```text
paper-pdf-downloader
```

Outputs:

- `download_report.md`
- `papers/<paper_id>/metadata.json`
- `papers/<paper_id>/paper.pdf`

Purpose:

- download only confirmed open-access PDFs;
- preserve metadata and source URLs;
- avoid paywall bypassing.

Human feedback state used:

- only papers selected by the reading plan and aligned with user paper decisions were downloaded.

## 5. PDF To Markdown Conversion

Skill:

```text
pdf-to-markdown-converter
```

Outputs:

- `papers/<paper_id>/paper.md`
- `papers/<paper_id>/conversion_report.json`

Excluded conversion artifacts:

- `papers/<paper_id>/mineru/`

Purpose:

- convert downloaded PDFs into `paper.md`;
- preserve conversion metadata;
- prepare Markdown input for single-paper Skill extraction.

Human feedback state used:

- conversion preserved the project handoff path so extraction could still read `human_feedback_state.json`.

## 6. Single-Paper Skill Extraction

Skill:

```text
paper-to-skill-extractor
```

Outputs:

- `papers/<paper_id>/skill_candidates.json`
- `papers/<paper_id>/skill_cards/*.yaml`
- `papers/<paper_id>/report.md`

Purpose:

- extract reusable `proof_pattern` Skill Cards from each selected `paper.md`;
- preserve line references to each source `paper.md`;
- mark candidates as `accepted_candidate`, `needs_review`, or `rejected`.

Human feedback state used:

- extraction prioritized proof spans that convert approximation, coupling, or velocity-field errors into Wasserstein or total-variation guarantees.

## 7. Cross-Paper Skill Synthesis

Skill:

```text
cross-paper-skill-synthesizer
```

Outputs:

- `synthesized_skills/domain_method_map.yaml`
- `synthesized_skills/merged_skill_cards/*.yaml`
- `synthesized_skills/synthesis_report.md`

Purpose:

- cluster and merge single-paper Skill Cards;
- generalize proof patterns across papers;
- produce a domain method map and library-ready or review-worthy merged Skill Cards.

Human feedback state used:

- synthesis prioritized reusable proof mechanisms over paper-specific model families;
- `ode_flow_stability_to_wasserstein_error` was accepted as central;
- empirical-process style skills were kept visible but marked for review where assumptions need checking.

## Preserved Artifacts

This example preserves:

- seed papers as PDFs;
- seed papers as Markdown;
- human feedback state;
- profile, retrieval, triage, and report JSON/Markdown artifacts;
- downloaded selected PDFs;
- converted `paper.md` files;
- single-paper Skill extraction outputs;
- cross-paper synthesis outputs.

This example excludes:

- local `.env`;
- MinerU intermediate folders;
- macOS `.DS_Store`;
- temporary pytest or Python cache files.
