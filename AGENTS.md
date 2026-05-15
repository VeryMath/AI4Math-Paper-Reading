# AGENTS.md

## Project Goal

This repository implements a coding-agent-assisted paper-to-skill workflow for an AI4Math skill library.

Codex is the reference operator for this repository, but the Skill layer should remain usable by other coding agents such as Claude Code, Gemini, OpenCode, Cursor, and similar agentic development tools.

The goal is not to summarize papers, but to extract reusable mathematical research skills from papers.

## Current Scope

Prioritize the user-facing workflow Skill at `skills/paper-to-skill-workflow`.

The default user input is `paper.pdf`. If the user provides `paper.md`, skip conversion and extract directly.

The active coding agent is the extraction engine. The workflow should not require external LLM APIs.

Keep PDF conversion, extraction, retrieval, synthesis, and future automation as separate Skills rather than folding every responsibility into one file.

## Source of Truth

Always preserve the original `paper.pdf` when provided and the full converted `paper.md`. Structured files are weak indexes, reports, or generated artifacts, not replacements for the original paper.

Every extracted skill must include source line references back to `paper.md`.

## Engineering Rules

- Encode the extraction workflow as a portable Skill first.
- Keep platform-specific adapter files thin and point them back to `skills/registry.yaml` and the shared `skills/` layer.
- Keep schemas and templates explicit.
- Keep future Python automation compatible with the Skill workflow.
- If Python modules are later added, use Pydantic for schemas and pytest for tests.
- Do not silently drop source text.
- Prefer small composable modules and deterministic output formats.

## Done Means

A task is done only when:

- the portable Skill workflow is written or updated;
- a PDF paper can be processed end-to-end into Markdown, SkillCandidates, SkillCards, and a report;
- generated outputs match the expected schema;
- extracted skills include source evidence and review status.
