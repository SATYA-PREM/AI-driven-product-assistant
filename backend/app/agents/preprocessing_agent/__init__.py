"""
preprocessing_agent package
---------------------------
CrewAI Preprocessing Agent for cleaning, normalization, deep AI preprocessing,
quarantining dirty data, and PM salvage validation workflows.
"""

from app.agents.preprocessing_agent.agent import (
    PreprocessingAgent,
    preprocessing_agent,
    create_preprocessing_agent,
    create_preprocessing_tasks,
    create_preprocessing_crew,
)
from app.agents.preprocessing_agent.tools import (
    get_preprocessing_agent_tools,
    clean_and_normalize_dataset,
    preprocess_valid_data,
    audit_dirty_data,
    promote_salvaged_data,
    get_dataset_usability_report,
    inspect_dataset,
    get_job_status,
)
from app.agents.preprocessing_agent.prompts import (
    PREPROCESSING_AGENT_ROLE,
    PREPROCESSING_AGENT_GOAL,
    PREPROCESSING_AGENT_BACKSTORY,
)

__all__ = [
    "PreprocessingAgent",
    "preprocessing_agent",
    "create_preprocessing_agent",
    "create_preprocessing_tasks",
    "create_preprocessing_crew",
    "get_preprocessing_agent_tools",
    "clean_and_normalize_dataset",
    "preprocess_valid_data",
    "audit_dirty_data",
    "promote_salvaged_data",
    "get_dataset_usability_report",
    "inspect_dataset",
    "get_job_status",
    "PREPROCESSING_AGENT_ROLE",
    "PREPROCESSING_AGENT_GOAL",
    "PREPROCESSING_AGENT_BACKSTORY",
]

