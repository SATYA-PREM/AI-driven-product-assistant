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
from app.agents.crew import ProductIntelligenceCrew, crew_manager

__all__ = [
    "get_llm",
    "PreprocessingAgent",
    "preprocessing_agent",
    "create_preprocessing_agent",
    "create_preprocessing_tasks",
    "create_preprocessing_crew",
    "get_preprocessing_agent_tools",
    "ProductIntelligenceCrew",
    "crew_manager",
]
