"""
agent.py
---------
CrewAI Data Agent for the Product Intelligence platform.

The Data Agent orchestrates data pipeline operations:
Validation → Cleaning → Preprocessing → AI-Ready Product Signals.

Operates both as:
1. A native CrewAI Agent (for multi-agent crews and autonomous task execution).
2. A direct programmatic service interface (for deterministic API / test execution).

Architecture:
    User / Multi-Agent Crew → Data Agent (CrewAI) → Tools → Services → Repositories → MongoDB
"""

from __future__ import annotations

from typing import Any, Optional
from crewai import Agent, Task, Crew, Process

from app.core.config import settings
from app.core.logging import get_logger
from app.agents.llm import get_llm
from app.agents.data_agent.prompts import (
    DATA_AGENT_ROLE,
    DATA_AGENT_GOAL,
    DATA_AGENT_BACKSTORY,
    FULL_PIPELINE_TASK_DESCRIPTION,
    FULL_PIPELINE_TASK_EXPECTED_OUTPUT,
    VALIDATE_TASK_DESCRIPTION,
    VALIDATE_TASK_EXPECTED_OUTPUT,
    CLEAN_TASK_DESCRIPTION,
    CLEAN_TASK_EXPECTED_OUTPUT,
    PREPROCESS_TASK_DESCRIPTION,
    PREPROCESS_TASK_EXPECTED_OUTPUT,
    TOOL_DESCRIPTIONS,
)
from app.agents.data_agent import tools

logger = get_logger(__name__)


def create_data_agent(
    llm: Optional[Any] = None,
    allow_delegation: bool = False,
    verbose: bool = True,
) -> Agent:
    """
    Factory function to instantiate a native CrewAI Data Agent.

    Args:
        llm: Custom LLM instance. If None, uses the shared centralized get_llm().
        allow_delegation: Whether the agent can delegate tasks to other agents
                          in a multi-agent system.
        verbose: Whether the agent should log its reasoning steps.

    Returns:
        CrewAI Agent configured with data pipeline tools.
    """
    agent_llm = llm or get_llm()
    agent_tools = tools.get_data_agent_tools()

    return Agent(
        role=DATA_AGENT_ROLE,
        goal=DATA_AGENT_GOAL,
        backstory=DATA_AGENT_BACKSTORY,
        tools=agent_tools,
        llm=agent_llm,
        verbose=verbose,
        allow_delegation=allow_delegation,
    )


def create_data_pipeline_tasks(
    agent: Agent,
    dataset_id: str,
    workspace_id: str,
) -> list[Task]:
    """
    Create sequential CrewAI Tasks for dataset processing:
    Validation -> Cleaning -> Preprocessing.
    """
    validation_task = Task(
        description=VALIDATE_TASK_DESCRIPTION.format(
            dataset_id=dataset_id,
            workspace_id=workspace_id,
        ),
        expected_output=VALIDATE_TASK_EXPECTED_OUTPUT,
        agent=agent,
        tools=[tools.validate_dataset_tool],
    )

    cleaning_task = Task(
        description=CLEAN_TASK_DESCRIPTION.format(
            dataset_id=dataset_id,
            workspace_id=workspace_id,
        ),
        expected_output=CLEAN_TASK_EXPECTED_OUTPUT,
        agent=agent,
        tools=[tools.clean_dataset_tool],
    )

    preprocessing_task = Task(
        description=PREPROCESS_TASK_DESCRIPTION.format(
            dataset_id=dataset_id,
            workspace_id=workspace_id,
        ),
        expected_output=PREPROCESS_TASK_EXPECTED_OUTPUT,
        agent=agent,
        tools=[tools.preprocess_dataset_tool],
    )

    return [validation_task, cleaning_task, preprocessing_task]


def create_data_pipeline_crew(
    dataset_id: str,
    workspace_id: str,
    llm: Optional[Any] = None,
    agent: Optional[Agent] = None,
) -> Crew:
    """
    Construct a CrewAI Crew dedicated to data pipeline orchestration.

    Args:
        dataset_id: Dataset to process.
        workspace_id: Workspace context.
        llm: Optional LLM override.
        agent: Optional pre-configured Agent instance.

    Returns:
        CrewAI Crew ready for kickoff.
    """
    data_worker = agent or create_data_agent(llm=llm)
    tasks = create_data_pipeline_tasks(
        agent=data_worker,
        dataset_id=dataset_id,
        workspace_id=workspace_id,
    )

    return Crew(
        agents=[data_worker],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )


class DataAgent:
    """
    Data Agent service wrapper.

    Provides a clean, unified interface for both:
    - Direct tool execution / deterministic pipelines
    - CrewAI-based autonomous execution and multi-agent participation
    """

    def __init__(self):
        self.has_gemini = bool(settings.GEMINI_API_KEY)
        self._tools = {
            "inspect_dataset": tools.inspect_dataset,
            "get_job_status": tools.get_job_status,
            "get_dataset_summary": tools.get_dataset_summary,
            "validate_dataset": tools.validate_dataset,
            "clean_dataset": tools.clean_dataset,
            "preprocess_dataset": tools.preprocess_dataset,
        }
        self._crew_agent: Optional[Agent] = None

    def get_crew_agent(self, llm: Optional[Any] = None, allow_delegation: bool = False) -> Agent:
        """
        Get or create the native CrewAI Agent instance.
        """
        if self._crew_agent is None or llm is not None:
            self._crew_agent = create_data_agent(llm=llm, allow_delegation=allow_delegation)
        return self._crew_agent

    def execute_tool(self, tool_name: str, **kwargs: Any) -> dict:
        """
        Execute a named tool with the given arguments programmatically.

        Args:
            tool_name: Name of the tool to execute.
            **kwargs: Arguments to pass to the tool.

        Returns:
            Tool execution result dict.
        """
        if tool_name not in self._tools:
            raise ValueError(
                f"Unknown tool: {tool_name}. "
                f"Available tools: {list(self._tools.keys())}"
            )

        logger.info(f"Data Agent executing tool: {tool_name}")
        result = self._tools[tool_name](**kwargs)
        logger.info(f"Data Agent tool {tool_name} completed")
        return result

    def run_full_pipeline(
        self,
        dataset_id: str,
        workspace_id: str,
    ) -> dict:
        """
        Run the complete pipeline for a dataset deterministically:
        Inspect → Validate → Clean → Preprocess → Summary
        """
        logger.info(f"Data Agent: running full pipeline for dataset={dataset_id}")

        results = {
            "dataset_id": dataset_id,
            "steps": {},
            "status": "running",
        }

        try:
            # Step 1: Inspect
            inspection = self.execute_tool(
                "inspect_dataset",
                dataset_id=dataset_id,
            )
            results["steps"]["inspect"] = {
                "status": "completed",
                "raw_count": inspection.get("raw_record_count", 0),
            }

            # Step 2: Validate
            validation = self.execute_tool(
                "validate_dataset",
                dataset_id=dataset_id,
                workspace_id=workspace_id,
            )
            results["steps"]["validation"] = {
                "status": "completed",
                "valid": validation.get("valid_count", 0),
                "invalid": validation.get("invalid_count", 0),
                "quality_score": validation.get("quality_score", 0.0),
            }

            # Step 3: Clean
            cleaning = self.execute_tool(
                "clean_dataset",
                dataset_id=dataset_id,
                workspace_id=workspace_id,
            )
            results["steps"]["cleaning"] = {
                "status": "completed",
                "cleaned_count": cleaning.get("cleaned_count", 0),
            }

            # Step 4: Preprocess
            preprocessing = self.execute_tool(
                "preprocess_dataset",
                dataset_id=dataset_id,
                workspace_id=workspace_id,
            )
            results["steps"]["preprocessing"] = {
                "status": "completed",
                "processed_count": preprocessing.get("processed_count", 0),
            }

            results["status"] = "completed"

            # Final summary
            summary = self.execute_tool(
                "get_dataset_summary",
                dataset_id=dataset_id,
            )
            results["summary"] = summary

            logger.info(f"Data Agent: pipeline completed for dataset={dataset_id}")

        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
            logger.error(f"Data Agent: pipeline failed for dataset={dataset_id}: {e}")

        return results

    def run_crew_pipeline(
        self,
        dataset_id: str,
        workspace_id: str,
        llm: Optional[Any] = None,
    ) -> Any:
        """
        Run the data pipeline using CrewAI autonomous orchestration.

        Args:
            dataset_id: The dataset to process.
            workspace_id: The workspace context.
            llm: Optional LLM instance.

        Returns:
            CrewAI CrewOutput result.
        """
        crew = create_data_pipeline_crew(
            dataset_id=dataset_id,
            workspace_id=workspace_id,
            llm=llm,
            agent=self.get_crew_agent(llm=llm),
        )
        logger.info(f"Data Agent: kicking off CrewAI data pipeline for dataset={dataset_id}")
        return crew.kickoff()

    def list_tools(self) -> list[dict]:
        """List all available tools with their descriptions."""
        return [
            {"name": name, "description": TOOL_DESCRIPTIONS.get(name, "")}
            for name in self._tools
        ]


# Module-level singleton
data_agent = DataAgent()
