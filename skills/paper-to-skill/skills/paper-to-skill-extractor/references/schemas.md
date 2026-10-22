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
mathematical_dependencies:
  - name: string
    required_statement: string
    conditions: [string]
    role: string
    evidence: string
    status: checked | needs_review | not_checked
independent_verification:
  status: not_run | passed | failed | inconclusive
  checks:
    - method: separate_derivation | formal_proof | exact_solution | numerical_check
      performed_by: string
      claim_checked: string
      assumptions_checked: [string]
      result: string
      evidence: string
      scope_and_limits: string
failure_cases:
  - problem: string
    violated_assumption: string
    result: string
    evidence: string
    response: restrict_claim | reject_application | revise_method
cross_problem_reuse:
  status: not_run | checked_examples | failed | inconclusive
  cases:
    - problem: string
      difference_from_source: string
      assumptions_checked: [string]
      adaptations: [string]
      result: string
      evidence: string
promotion:
  status: candidate | ready_for_library | needs_human_review | rejected
  rationale: string
  unmet_requirements: [string]
quality:
  reusability: integer
  clarity: integer
  generality: integer
  verifiability: integer
  agent_callability: integer
  mathematical_risk: integer
  total_score: number
```

The fields above after `limitations` belong to **SkillCard**. SkillCandidate remains a short extraction record; copy any completed verification evidence into its associated card. Templates may use empty lists while work is pending. Completed records need concrete conditions, results, evidence paths, and limits. `independent_verification.status: passed` applies only to the recorded claims and scopes; a numerical check cannot establish an unrestricted theorem. Missing fields in older cards mean unverified, never passed.
