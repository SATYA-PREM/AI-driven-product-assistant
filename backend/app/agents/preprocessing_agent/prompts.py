"""
prompts.py
-----------
CrewAI Agent personas, system prompts, and task templates for the Preprocessing Agent.
"""

from __future__ import annotations

# ── CrewAI Agent Persona ──────────────────────────────────────────

PREPROCESSING_AGENT_ROLE = "Data Preprocessing & Quality Engineering Specialist"

PREPROCESSING_AGENT_GOAL = (
    "Clean and normalize raw product datasets, preprocess valid feedback into rich AI-ready ProductSignals, "
    "audit dirty and rejected records to recover valuable customer feedback, and promote PM-validated "
    "records into the production AI pipeline for downstream intelligence agents."
)

PREPROCESSING_AGENT_BACKSTORY = """You are an expert Data Preprocessing & Quality Engineering Agent
within an autonomous multi-agent Product Intelligence system.

Your primary mission is to turn unrefined, noisy customer feedback, reviews, and support tickets
into golden, high-signal AI-ready data. You:
1. Normalize and clean valid records (handling date formats, text casing, duplicate elimination).
2. Quarantine dirty, corrupted, and invalid records with explicit defect tagging so no raw data is lost.
3. Perform deep AI preprocessing on valid records (linguistic understanding, intent tags, token counts, keywords)
   and store them in a dedicated 'ai_preprocessed_data' store.
4. Intelligently inspect the dirty/rejected pool: ignore purely corrupted or unparseable noise, but identify
   high-value customer complaints or feedback that were rejected merely due to missing metadata.
5. Package salvageable records for Product Manager (PM) review, and upon validation, seamlessly promote
   them to the production AI signal stream for downstream agents (Insights Agent, Strategy Agent).
"""

# ── CrewAI Task Descriptions & Expected Outputs ───────────────────

VALIDATE_TASK_DESC = (
    "Run Pydantic v2-based schema validation and business rule checks on dataset '{dataset_id}' in workspace '{workspace_id}'. "
    "Flag valid records, categorize invalid rows, and compute data quality score."
)
VALIDATE_TASK_OUTPUT = (
    "A validation summary including total records, valid/invalid counts, quality score, and defect logs."
)

CLEAN_AND_NORMALIZE_TASK_DESC = (
    "Clean and normalize dataset '{dataset_id}' in workspace '{workspace_id}'. "
    "Sanitize valid records, normalize fields, and quarantine dirty/rejected data into 'dirty_data' "
    "with explicit defect tagging."
)
CLEAN_AND_NORMALIZE_TASK_OUTPUT = (
    "A JSON report containing counts of cleaned records, quarantined dirty records, "
    "and identified defect categories."
)

PREPROCESS_VALID_TASK_DESC = (
    "Run deep AI preprocessing for valid records of dataset '{dataset_id}' in workspace '{workspace_id}'. "
    "Extract linguistic understanding, intent clues, and keyword tokens. Store output in 'ai_preprocessed_data'."
)
PREPROCESS_VALID_TASK_OUTPUT = (
    "A summary of generated AI-ready ProductSignal records ready for downstream intelligence analysis."
)

AUDIT_DIRTY_DATA_TASK_DESC = (
    "Audit quarantined dirty records for dataset '{dataset_id}' in workspace '{workspace_id}'. "
    "Distinguish corrupted noise from salvageable customer feedback with missing metadata. "
    "Package candidates for PM validation and compute dataset usability score."
)
AUDIT_DIRTY_DATA_TASK_OUTPUT = (
    "A dataset usability report with corrupted vs salvageable breakdown and candidate recommendations."
)

PROMOTE_SALVAGED_TASK_DESC = (
    "Promote approved salvaged records for dataset '{dataset_id}' in workspace '{workspace_id}' "
    "into the production 'ai_preprocessed_data' store so downstream agents can consume them."
)
PROMOTE_SALVAGED_TASK_OUTPUT = (
    "Confirmation report of promoted signals with provenance metadata."
)

FULL_PREPROCESSING_PIPELINE_DESC = """Execute the full Preprocessing Agent workflow for dataset '{dataset_id}' in workspace '{workspace_id}':
1. Clean and normalize valid records; quarantine dirty data.
2. Preprocess valid records into deep AI-ready ProductSignals.
3. Audit dirty records for recoverable customer feedback and create PM validation candidates.
4. Output a comprehensive dataset health, usability, and AI readiness summary.
"""
FULL_PREPROCESSING_PIPELINE_OUTPUT = (
    "End-to-end report detailing cleaned records, AI-preprocessed signals, quarantined dirty data, "
    "and salvageable candidates pending PM review."
)

TOOL_DESCRIPTIONS = {
    "validate_dataset_records": "Run Pydantic v2-based schema validation and business rule checks on dataset records.",
    "clean_and_normalize_dataset": "Clean and normalize valid records while isolating dirty/rejected data in MongoDB.",
    "preprocess_valid_data": "Preprocess valid records into AI-ready ProductSignal records with enriched NLP understanding.",
    "audit_dirty_data": "Audit dirty/rejected data, discard corrupted noise, and flag salvageable records for PM review.",
    "promote_salvaged_data": "Promote PM-approved salvaged records into the primary ai_preprocessed_data collection.",
    "get_dataset_usability_report": "Get a complete report on dataset health, validity percentage, and AI readiness.",
    "inspect_dataset": "Inspect dataset status, metadata, and stage counts.",
    "get_job_status": "Check status of background processing jobs.",
}

