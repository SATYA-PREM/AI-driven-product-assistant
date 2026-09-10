"""
data_agent package
------------------
CrewAI-powered Data Agent for dataset inspection, validation, cleaning, and preprocessing.
"""

from app.agents.data_agent.agent import (
    DataAgent,
    data_agent,
    create_data_agent,
    create_data_pipeline_tasks,
    create_data_pipeline_crew,
)
from app.agents.data_agent.tools import (
    get_data_agent_tools,
    inspect_dataset,
    get_job_status,
    get_dataset_summary,
    validate_dataset,
    clean_dataset,
    preprocess_dataset,
)
from app.agents.data_agent.prompts import (
    DATA_AGENT_ROLE,
    DATA_AGENT_GOAL,
    DATA_AGENT_BACKSTORY,
)

__all__ = [
    "DataAgent",
    "data_agent",
    "create_data_agent",
    "create_data_pipeline_tasks",
    "create_data_pipeline_crew",
    "get_data_agent_tools",
    "inspect_dataset",
    "get_job_status",
    "get_dataset_summary",
    "validate_dataset",
    "clean_dataset",
    "preprocess_dataset",
    "DATA_AGENT_ROLE",
    "DATA_AGENT_GOAL",
    "DATA_AGENT_BACKSTORY",
]

