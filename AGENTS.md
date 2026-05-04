# AGENTS.md

## Project Goal

This repository implements a Codex-assisted paper-to-skill workflow for an AI4Math skill library.

The goal is not to summarize papers, but to extract reusable mathematical research skills from papers.

## Current MVP Scope

Prioritize the Codex Skill at `skills/paper-to-skill-extractor`.

Only support Markdown input and `proof_pattern` mining in v0.1. The current MVP does not require external LLM APIs. Codex itself is the extraction engine.

Do not implement OCR, PDF conversion, arXiv download, Lean verification, Web UI, database storage, or full benchmark generation in v0.1.

## Source of Truth

Always preserve the full `paper.md`. Structured files are weak indexes, reports, or generated artifacts, not replacements for the original paper.

Every extracted skill must include source line references back to `paper.md`.

## Engineering Rules

- Encode the extraction workflow as a Codex Skill first.
- Keep schemas and templates explicit.
- Keep future Python automation compatible with the Skill workflow.
- If Python modules are later added, use Pydantic for schemas and pytest for tests.
- Do not silently drop source text.
- Prefer small composable modules and deterministic output formats.

## Done Means

A task is done only when:

- the Codex Skill workflow is written or updated;
- the example paper can be processed end-to-end;
- generated outputs match the expected schema;
- extracted skills include source evidence and review status.
