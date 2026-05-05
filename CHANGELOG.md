# Changelog

## v0.1.1 - Human Feedback State

This release upgrades the workflow from a mostly linear Codex pipeline into a lightweight human-in-the-loop research loop.

本版本的核心变化是引入 `human_feedback_state.json`，把用户对研究方向、论文筛选和 Skill Card 判断的反馈沉淀为可复用状态，而不是只留在聊天上下文里。

### Added

- Added the public workflow convention:

```text
outputs/<research_project_id>/human_feedback_state.json
```

- Added a reproducible example feedback state:

```text
examples/auto_research_trial/human_feedback_state.json
```

- Added a README section, `Human-in-the-loop Research State`, documenting:
  - `focus_updates`
  - `negative_preferences`
  - `paper_decisions`
  - `skill_decisions`
  - `next_step_directives`
  - `stage_feedback_log`

### Changed

- Updated the workflow instructions so each downstream Skill reads `human_feedback_state.json` when it exists.
- Updated all existing workflow Skills to treat human feedback as an optional input or workflow dependency:
  - `seed-paper-profiler`
  - `related-paper-retriever`
  - `innovation-paper-finder`
  - `paper-triage-ranker`
  - `paper-pdf-downloader`
  - `pdf-to-markdown-converter`
  - `paper-to-skill-extractor`
  - `cross-paper-skill-synthesizer`
- Updated the auto research trial example to show the loop:

```text
Codex output -> human feedback -> human_feedback_state.json -> next Skill uses state
```

### Design Notes

- No new `human-research-reviewer` Skill was added in this version.
- The feedback state is intentionally lightweight: Codex can create or update it from natural-language user feedback.
- The first emphasis is on research direction and paper triage:
  - strengthen Wasserstein error, coupling bias, and reusable proof patterns;
  - down-rank heavy-tailed priors as a standalone topic;
  - down-rank purely empirical flow matching papers unless needed for positioning.

### Verification

- Validated `examples/auto_research_trial/human_feedback_state.json` with `python3 -m json.tool`.
- Revalidated existing example JSON files.
- Ran the local test suite:

```text
21 passed
```

## v0.1.0 - Initial Workflow Release

Initial public baseline for `ai4math-paper-skills`, a Codex-native paper-to-skill workflow module for AI4Math auto research.

### Added

- Added the end-to-end Skill chain:
  - `seed-paper-profiler`
  - `related-paper-retriever`
  - `innovation-paper-finder`
  - `paper-triage-ranker`
  - `paper-pdf-downloader`
  - `pdf-to-markdown-converter`
  - `paper-to-skill-extractor`
  - `cross-paper-skill-synthesizer`
- Added a full reproducible example under:

```text
examples/auto_research_trial/
```

- Preserved the PDF-to-Skill evidence chain in the example:

```text
paper.pdf -> paper.md -> skill_candidates.json / skill_cards -> synthesized_skills
```

- Added project README, MIT license, `.env.example`, and git ignore rules for local outputs and intermediate artifacts.

### Boundaries

- This repository is not the full AI4Math auto research system.
- It is the paper Skill submodule: research-paper discovery, triage, conversion, proof-pattern extraction, and cross-paper Skill synthesis.
- `outputs/`, `docs/`, and `tests/` are kept local and ignored by Git for the initial public package.
