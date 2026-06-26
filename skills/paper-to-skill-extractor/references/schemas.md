# Schemas

Use these fields for generated artifacts.

## SkillCandidate

```yaml
skill_name: string
zh_name: string
skill_type: proof_pattern
source:
  paper_md: paper.md
  start_line: integer
  end_line: integer
  source_blocks: [string]
source_span: string
why_reusable: string
input: [string]
output: [string]
assumptions: [string]
core_steps: [string]
trigger_keywords: [string]
limitations: [string]
reusability_score: integer
confidence: number
status: accepted_candidate | needs_review | rejected
quality:
  reusability: integer
  clarity: integer
  generality: integer
  verifiability: integer
  agent_callability: integer
  mathematical_risk: integer
  total_score: number
```

## SkillCard

```yaml
name: string
zh_name: string
category: proof_pattern
status: accepted_candidate | needs_review | rejected
source:
  paper_title: string | null
  paper_md: paper.md
  source_blocks: [string]
  start_line: integer
  end_line: integer
description: string
input: [string]
output: [string]
assumptions: [string]
core_steps: [string]
trigger_keywords: [string]
limitations: [string]
quality:
  reusability: integer
  clarity: integer
  generality: integer
  verifiability: integer
  agent_callability: integer
  mathematical_risk: integer
  total_score: number
```
