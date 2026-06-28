# Seed Paper Profiler Schemas

## `research_profile.json`

```json
{
  "research_project_id": "string",
  "created_at": "YYYY-MM-DD",
  "seed_inputs": [
    {
      "paper_id": "string",
      "title": "string",
      "path_or_url": "string",
      "input_type": "paper_md | abstract | notes | extraction_report | skill_cards",
      "source_note": "string"
    }
  ],
  "domain": ["string"],
  "core_problems": [
    {
      "problem": "string",
      "evidence": [
        {
          "paper_id": "string",
          "paper_md": "paper.md",
          "start_line": 0,
          "end_line": 0,
          "note": "string"
        }
      ],
      "confidence": 0.0
    }
  ],
  "methods": ["string"],
  "assumptions": ["string"],
  "proof_patterns": ["string"],
  "technical_keywords": ["string"],
  "user_interest_hypotheses": [
    {
      "hypothesis": "string",
      "why": "string",
      "confidence": 0.0
    }
  ],
  "negative_preferences": ["string"],
  "search_queries": [
    {
      "query": "string",
      "search_route": "problem | method | theorem | assumption | application | adjacent_domain | author_trail | citation_trail",
      "purpose": "string"
    }
  ],
  "open_questions": ["string"],
  "checkpoint_questions": ["string"],
  "checkpoint_questions_bilingual": [
    {
      "zh": "string",
      "en": "string"
    }
  ],
  "language_policy": {
    "user_facing_markdown": "zh_en_bilingual",
    "json_keys": "english_stable",
    "json_text": "english_with_bilingual_checkpoints"
  }
}
```

Use 1-based line numbers when source lines exist. Use `0` for `start_line` and `end_line` only when the input has no stable line numbers.

Keep JSON keys and enum values in English for downstream tools. Put bilingual confirmation questions in `checkpoint_questions_bilingual`; write `profile_review.md` fully bilingual.
