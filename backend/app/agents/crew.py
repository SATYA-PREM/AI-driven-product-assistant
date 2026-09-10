"""
crew.py
-------
Multi-Agent System Coordinator for Product Intelligence using CrewAI.

Orchestrates collaboration between specialized agents:
- PreprocessingAgent (Cleaning, normalization, dirty data quarantine, AI signals, PM salvage)
- DataAgent (Inspects, validates, cleans, and standardizes data)
- Future: InsightsAgent (Sentiment, themes, and pain-point extraction)
- Future: ProductStrategyAgent (Feature prioritization and roadmap suggestions)

Supports both sequential workflows and hierarchical manager-led multi-agent execution.
"""

from __future__ import annotations

from typing import Any, Optional
from crewai import Agent, Task, Crew, Process

from app.core.logging import get_logger
from app.agents.llm import get_llm
from app.agents.data_agent.agent import create_data_agent, create_data_pipeline_tasks
from app.agents.preprocessing_agent.agent import (
    create_preprocessing_agent,
    create_preprocessing_tasks,
)

logger = get_logger(__name__)


class ProductIntelligenceCrew:
    """
    Multi-Agent Crew orchestrator for the Product Intelligence system.

    Manages agent lifecycle, task assignment, and crew kickoff across
    one or more specialized CrewAI agents.
    """

    def __init__(self, llm: Optional[Any] = None):
        self.llm = llm or get_llm()
        self._agents: dict[str, Agent] = {}
        self._initialize_default_agents()

    def _initialize_default_agents(self) -> None:
        """Initialize core system agents."""
        self._agents["preprocessing_agent"] = create_preprocessing_agent(
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
        )
        self._agents["data_agent"] = create_data_agent(
            llm=self.llm,
            allow_delegation=False,
            verbose=True,
        )

    def register_agent(self, name: str, agent: Agent) -> None:
        """
        Register a new agent into the multi-agent system (e.g. insights_agent, strategy_agent).

        Args:
            name: Identifier for the agent.
            agent: Configured CrewAI Agent.
        """
        self._agents[name] = agent
        logger.info(f"Registered agent '{name}' into Multi-Agent System.")

    def get_agent(self, name: str) -> Optional[Agent]:
        """Retrieve a registered agent by name."""
        return self._agents.get(name)

    def list_agents(self) -> list[str]:
        """List names of all registered agents."""
        return list(self._agents.keys())

    def build_preprocessing_crew(
        self,
        dataset_id: str,
        workspace_id: str,
    ) -> Crew:
        """
        Build a crew focused on the cleaning, normalization, dirty-data audit, and AI-ready preprocessing.
        """
        agent = self._agents["preprocessing_agent"]
        tasks = create_preprocessing_tasks(
            agent=agent,
            dataset_id=dataset_id,
            workspace_id=workspace_id,
        )
        return Crew(
            agents=[agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

    def build_data_pipeline_crew(
        self,
        dataset_id: str,
        workspace_id: str,
    ) -> Crew:
        """
        Build a crew focused on standard data validation, cleaning, and preprocessing.
        """
        data_agent = self._agents["data_agent"]
        tasks = create_data_pipeline_tasks(
            agent=data_agent,
            dataset_id=dataset_id,
            workspace_id=workspace_id,
        )

        return Crew(
            agents=[data_agent],
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
        )

    def build_multi_agent_crew(
        self,
        tasks: list[Task],
        agents: Optional[list[Agent]] = None,
        process: Process = Process.sequential,
        manager_llm: Optional[Any] = None,
    ) -> Crew:
        """
        Build a custom multi-agent crew with specified agents, tasks, and process flow.

        Args:
            tasks: List of CrewAI Tasks to execute.
            agents: Specific agents to include. If None, includes all registered agents.
            process: Process.sequential or Process.hierarchical.
            manager_llm: Required if process is hierarchical.

        Returns:
            CrewAI Crew ready for execution.
        """
        selected_agents = agents or list(self._agents.values())

        crew_kwargs: dict[str, Any] = {
            "agents": selected_agents,
            "tasks": tasks,
            "process": process,
            "verbose": True,
        }

        if process == Process.hierarchical:
            crew_kwargs["manager_llm"] = manager_llm or self.llm

        return Crew(**crew_kwargs)


# Module-level singleton
crew_manager = ProductIntelligenceCrew()
