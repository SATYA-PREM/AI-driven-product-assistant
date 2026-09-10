"""
Unit tests for Data Agent tools and CrewAI orchestration capabilities.
"""

from app.agents.data_agent.agent import (
    data_agent,
    create_data_agent,
    create_data_pipeline_tasks,
    create_data_pipeline_crew,
)
from app.agents.data_agent.tools import get_data_agent_tools
from app.agents.crew import crew_manager, ProductIntelligenceCrew


def test_data_agent_tool_listing():
    tools = data_agent.list_tools()
    assert len(tools) > 0
    tool_names = [t["name"] for t in tools]
    assert "inspect_dataset" in tool_names
    assert "validate_dataset" in tool_names
    assert "clean_dataset" in tool_names
    assert "preprocess_dataset" in tool_names
    assert "get_job_status" in tool_names
    assert "get_dataset_summary" in tool_names


def test_crewai_agent_creation():
    agent = create_data_agent()
    assert agent is not None
    assert agent.role == "Data Operations & Pipeline Specialist"
    assert "ProductSignal" in agent.goal
    assert len(agent.tools) == 6


def test_crewai_tools():
    tools = get_data_agent_tools()
    assert len(tools) == 6
    tool_names = [t.name for t in tools]
    assert "Inspect Dataset" in tool_names
    assert "Validate Dataset" in tool_names
    assert "Clean Dataset" in tool_names
    assert "Preprocess Dataset" in tool_names
    assert "Get Job Status" in tool_names
    assert "Get Dataset Summary" in tool_names


def test_create_data_pipeline_tasks():
    agent = create_data_agent()
    tasks = create_data_pipeline_tasks(
        agent=agent,
        dataset_id="test_ds_123",
        workspace_id="test_ws_456",
    )
    assert len(tasks) == 3
    assert "test_ds_123" in tasks[0].description
    assert tasks[0].agent == agent


def test_crew_manager_registration():
    mgr = ProductIntelligenceCrew()
    assert "data_agent" in mgr.list_agents()
    agent = mgr.get_agent("data_agent")
    assert agent is not None
    assert agent.role == "Data Operations & Pipeline Specialist"
