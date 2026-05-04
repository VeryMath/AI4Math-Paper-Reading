# Paper Triage Ranker Schemas

## `reading_plan.json`

```json
{
  "research_project_id": "string",
  "created_at": "YYYY-MM-DD",
  "sources": ["candidate_papers.json", "innovation_candidates.json"],
  "deduplication_notes": ["string"],
  "papers": [
    {
      "paper_id": "string",
      "title": "string",
      "url": "string",
      "pdf_url": "string",
      "group": "must_read | should_read | maybe_read | skip",
      "scores": {
        "relevance": 0,
        "innovation_potential": 0,
        "proof_pattern_value": 0,
        "positioning_value": 0,
        "access_readiness": 0,
        "reading_cost": 0
      },
      "decision_reason": "string",
      "reading_focus": ["abstract", "introduction", "theorem_statements", "proofs", "appendix", "experiments", "related_work"],
      "recommended_next_step": "download_and_convert | request_user_pdf | skim_only | extract_skill | skip",
      "notes": "string"
    }
  ],
  "reading_sequence": ["paper_id"],
  "download_queue": ["paper_id"],
  "extraction_queue": ["paper_id"],
  "checkpoint_questions": ["string"]
}
```
