# Innovation Paper Finder Schemas

## `innovation_candidates.json`

```json
{
  "research_project_id": "string",
  "created_at": "YYYY-MM-DD",
  "source_profile": "research_profile.json",
  "queries": [
    {
      "query": "string",
      "innovation_route": "proof_technique | sharper_bound | weaker_assumption | cross_domain | lower_bound | abstraction | alternative_formulation",
      "notes": "string"
    }
  ],
  "candidates": [
    {
      "paper_id": "string",
      "title": "string",
      "authors": ["string"],
      "year": "string",
      "venue": "string",
      "url": "string",
      "pdf_url": "string",
      "abstract_summary": "string",
      "innovation_signal": "new_proof_technique | sharper_bound | weaker_assumption | cross_domain_transfer | lower_bound | new_abstraction | alternative_formulation",
      "why_it_may_help": "string",
      "possible_research_angle": "string",
      "risk": "string",
      "recommended_action": "read_now | skim | save_for_later | reject",
      "download_status": "not_downloaded | open_pdf_found | downloaded | needs_user_pdf | paywalled_metadata_only",
      "notes": "string"
    }
  ],
  "strong_leads": ["paper_id"],
  "speculative_leads": ["paper_id"],
  "checkpoint_questions": ["string"]
}
```
