# Related Paper Retriever Schemas

## `candidate_papers.json`

```json
{
  "research_project_id": "string",
  "created_at": "YYYY-MM-DD",
  "source_profile": "research_profile.json",
  "queries": [
    {
      "query": "string",
      "search_route": "problem | method | theorem | assumption | application | author_trail | citation_trail",
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
      "relation_type": "direct_extension | same_problem | same_method | theoretical_background | benchmark_only",
      "relevance_reason": "string",
      "priority_hint": "high | medium | low",
      "download_status": "not_downloaded | open_pdf_found | downloaded | needs_user_pdf | paywalled_metadata_only",
      "source_quality": "primary | author_copy | metadata_only | secondary",
      "notes": "string"
    }
  ],
  "coverage_gaps": ["string"],
  "checkpoint_questions": ["string"]
}
```
