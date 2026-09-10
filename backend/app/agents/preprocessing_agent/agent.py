"""
agent.py
---------
CrewAI Preprocessing Agent for the Product Intelligence platform.

Orchestrates the entire cleaning, normalization, and AI preprocessing lifecycle:
1. Validates records with Pydantic v2 and enforces business rules.
2. Normalizes valid data records into 'cleaned_data'.
3. Isolates dirty, corrupted, or rejected data into 'dirty_data'.
4. Preprocesses valid data into deep AI-ready ProductSignals in 'ai_preprocessed_data'.
5. Audits dirty data to recover valuable customer feedback for PM review.
6. Promotes PM-approved salvaged data into the production AI signal stream.
"""

from __future__ import annotations

from typing import Any, Optional
from crewai import Agent, Task, Crew, Process

from app.core.config import settings
from app.core.logging import get_logger
from app.agents.llm import get_llm
from app.agents.preprocessing_agent.prompts import (
    PREPROCESSING_AGENT_ROLE,
    PREPROCESSING_AGENT_GOAL,
    PREPROCESSING_AGENT_BACKSTORY,
    VALIDATE_TASK_DESC,
    VALIDATE_TASK_OUTPUT,
    CLEAN_AND_NORMALIZE_TASK_DESC,
    CLEAN_AND_NORMALIZE_TASK_OUTPUT,
    PREPROCESS_VALID_TASK_DESC,
    PREPROCESS_VALID_TASK_OUTPUT,
    AUDIT_DIRTY_DATA_TASK_DESC,
    AUDIT_DIRTY_DATA_TASK_OUTPUT,
    TOOL_DESCRIPTIONS,
)
from app.agents.preprocessing_agent import tools

logger = get_logger(__name__)


def create_preprocessing_agent(
    llm: Optional[Any] = None,
    allow_delegation: bool = False,
    verbose: bool = True,
) -> Agent:
    """
    Instantiate a native CrewAI Preprocessing Agent.
    """
    agent_llm = llm or get_llm()
    agent_tools = tools.get_preprocessing_agent_tools()

    return Agent(
        role=PREPROCESSING_AGENT_ROLE,
        goal=PREPROCESSING_AGENT_GOAL,
        backstory=PREPROCESSING_AGENT_BACKSTORY,
        tools=agent_tools,
        llm=agent_llm,
        verbose=verbose,
        allow_delegation=allow_delegation,
    )


def create_preprocessing_tasks(
    agent: Agent,
    dataset_id: str,
    workspace_id: str,
) -> list[Task]:
    """
    Create sequential CrewAI Tasks for the Preprocessing Agent:
    1. Pydantic validation: validate schema & business rules.
    2. Clean and normalize valid data & quarantine dirty data.
    3. Preprocess valid data into AI-ready ProductSignals.
    4. Audit dirty data for recoverable insights and PM validation.
    """
    validate_task = Task(
        description=VALIDATE_TASK_DESC.format(
            dataset_id=dataset_id, workspace_id=workspace_id
        ),
        expected_output=VALIDATE_TASK_OUTPUT,
        agent=agent,
        tools=[tools.validate_dataset_records_tool],
    )

    clean_task = Task(
        description=CLEAN_AND_NORMALIZE_TASK_DESC.format(
            dataset_id=dataset_id, workspace_id=workspace_id
        ),
        expected_output=CLEAN_AND_NORMALIZE_TASK_OUTPUT,
        agent=agent,
        tools=[tools.clean_and_normalize_dataset_tool],
    )

    preprocess_task = Task(
        description=PREPROCESS_VALID_TASK_DESC.format(
            dataset_id=dataset_id, workspace_id=workspace_id
        ),
        expected_output=PREPROCESS_VALID_TASK_OUTPUT,
        agent=agent,
        tools=[tools.preprocess_valid_data_tool],
    )

    audit_dirty_task = Task(
        description=AUDIT_DIRTY_DATA_TASK_DESC.format(
            dataset_id=dataset_id, workspace_id=workspace_id
        ),
        expected_output=AUDIT_DIRTY_DATA_TASK_OUTPUT,
        agent=agent,
        tools=[tools.audit_dirty_data_tool, tools.get_dataset_usability_report_tool],
    )

    return [validate_task, clean_task, preprocess_task, audit_dirty_task]


def create_preprocessing_crew(
    dataset_id: str,
    workspace_id: str,
    llm: Optional[Any] = None,
    agent: Optional[Agent] = None,
) -> Crew:
    """
    Construct a CrewAI Crew dedicated to dataset cleaning and AI-ready preprocessing.
    """
    worker = agent or create_preprocessing_agent(llm=llm)
    tasks = create_preprocessing_tasks(
        agent=worker,
        dataset_id=dataset_id,
        workspace_id=workspace_id,
    )

    return Crew(
        agents=[worker],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )


class PreprocessingAgent:
    """
    Unified Preprocessing Agent service wrapper.
    Supports deterministic programmatic execution, salvage promotion workflows,
    and CrewAI autonomous orchestration.
    """

    def __init__(self):
        self.has_gemini = bool(settings.GEMINI_API_KEY)
        self._tools = {
            "validate_dataset_records": tools.validate_dataset_records,
            "clean_and_normalize_dataset": tools.clean_and_normalize_dataset,
            "preprocess_valid_data": tools.preprocess_valid_data,
            "audit_dirty_data": tools.audit_dirty_data,
            "promote_salvaged_data": tools.promote_salvaged_data,
            "get_dataset_usability_report": tools.get_dataset_usability_report,
            "inspect_dataset": tools.inspect_dataset,
            "get_job_status": tools.get_job_status,
        }
        self._crew_agent: Optional[Agent] = None

    def get_crew_agent(self, llm: Optional[Any] = None, allow_delegation: bool = False) -> Agent:
        """Get or initialize the native CrewAI Agent instance."""
        if self._crew_agent is None or llm is not None:
            self._crew_agent = create_preprocessing_agent(llm=llm, allow_delegation=allow_delegation)
        return self._crew_agent

    def execute_tool(self, tool_name: str, **kwargs: Any) -> dict:
        """Execute a named tool directly."""
        if tool_name not in self._tools:
            raise ValueError(
                f"Unknown tool: {tool_name}. Available: {list(self._tools.keys())}"
            )
        logger.info(f"Preprocessing Agent executing tool: {tool_name}")
        return self._tools[tool_name](**kwargs)

    def run_full_pipeline(
        self,
        dataset_id: str,
        workspace_id: str,
    ) -> dict:
        """
        Run the complete programmatic preprocessing pipeline:
        1. Run Pydantic v2-based validation and business rule checks.
        2. Clean and normalize valid data & quarantine dirty data.
        3. Preprocess valid data into deep AI ProductSignals.
        4. Audit dirty data for recoverable customer feedback.
        5. Produce dataset usability report.
        """
        logger.info(f"Preprocessing Agent: running full pipeline for dataset={dataset_id}")

        results: dict[str, Any] = {
            "dataset_id": dataset_id,
            "workspace_id": workspace_id,
            "steps": {},
            "status": "running",
        }

        try:
            # Step 1: Pydantic Validation
            val_res = self.execute_tool(
                "validate_dataset_records",
                dataset_id=dataset_id,
                workspace_id=workspace_id,
            )
            results["steps"]["validation"] = val_res

            # Step 2: Clean & Normalize valid records + isolate dirty records
            clean_res = self.execute_tool(
                "clean_and_normalize_dataset",
                dataset_id=dataset_id,
                workspace_id=workspace_id,
            )
            results["steps"]["clean_and_normalize"] = clean_res

            # Step 3: Preprocess valid data into AI ProductSignals
            preprocess_res = self.execute_tool(
                "preprocess_valid_data",
                dataset_id=dataset_id,
                workspace_id=workspace_id,
            )
            results["steps"]["ai_preprocessing"] = preprocess_res

            # Step 4: Audit dirty/rejected data for salvageable feedback
            audit_res = self.execute_tool(
                "audit_dirty_data",
                dataset_id=dataset_id,
                workspace_id=workspace_id,
            )
            results["steps"]["dirty_data_audit"] = audit_res

            # Step 5: Generate overall usability report
            usability = self.execute_tool(
                "get_dataset_usability_report",
                dataset_id=dataset_id,
            )
            results["usability_report"] = usability
            results["status"] = "completed"

            logger.info(f"Preprocessing Agent: pipeline finished successfully for dataset={dataset_id}")

        except Exception as e:
            results["status"] = "failed"
            results["error"] = str(e)
            logger.error(f"Preprocessing Agent: pipeline failed for dataset={dataset_id}: {e}")

        return results

    def promote_salvaged(
        self,
        dataset_id: str,
        workspace_id: str,
        salvage_ids: Optional[list[str]] = None,
        reviewer: str = "ProductManager",
    ) -> dict:
        """Promote PM-approved salvaged records into the AI signal stream."""
        return self.execute_tool(
            "promote_salvaged_data",
            dataset_id=dataset_id,
            workspace_id=workspace_id,
            salvage_ids=salvage_ids,
            reviewer=reviewer,
        )

    def run_crew(
        self,
        dataset_id: str,
        workspace_id: str,
        llm: Optional[Any] = None,
    ) -> Any:
        """Run the Preprocessing Agent using CrewAI autonomous orchestration."""
        crew = create_preprocessing_crew(
            dataset_id=dataset_id,
            workspace_id=workspace_id,
            llm=llm,
            agent=self.get_crew_agent(llm=llm),
        )
        logger.info(f"Preprocessing Agent: kicking off CrewAI for dataset={dataset_id}")
        return crew.kickoff()

    def list_tools(self) -> list[dict]:
        """List available tools with documentation."""
        return [
            {"name": name, "description": TOOL_DESCRIPTIONS.get(name, "")}
            for name in self._tools
        ]


preprocessing_agent = PreprocessingAgent()
