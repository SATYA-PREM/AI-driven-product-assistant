"""
agents package
--------------
CrewAI multi-agent framework for the Product Intelligence platform.
"""

from app.agents.llm import get_llm
from app.agents.preprocessing_agent.agent import (
    PreprocessingAgent,
    preprocessing_agent,
    create_preprocessing_agent,
    create_preprocessing_tasks,
    create_preprocessing_crew,
)
from app.agents.preprocessing_agent.tools import get_preprocessing_agent_tools
from app.agents.data_agent.agent import (
    DataAgent,
    data_agent,
    create_data_agent,
    create_data_pipeline_crew,
    create_data_pipeline_tasks,
)
from app.agents.data_agent.tools import get_data_agent_tools
from app.agents.crew import ProductIntelligenceCrew, crew_manager

__all__ = [
    "get_llm",
    # Preprocessing Agent (Primary Cleaning, Normalization & AI Preprocessing)
    "PreprocessingAgent",
    "preprocessing_agent",
    "create_preprocessing_agent",
    "create_preprocessing_tasks",
    "create_preprocessing_crew",
    "get_preprocessing_agent_tools",
    # Data Agent (General Data Operations)
    "DataAgent",
    "data_agent",
    "create_data_agent",
    "create_data_pipeline_crew",
    "create_data_pipeline_tasks",
    "get_data_agent_tools",
    # Multi-Agent Coordination
    "ProductIntelligenceCrew",
    "crew_manager",
]
