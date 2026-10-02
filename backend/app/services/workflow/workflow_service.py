from __future__ import annotations
from app.models.workflow import WorkflowModel
from app.repositories.workflow_repository import workflow_repository
from app.services.workflow.workflow_validator import validate_step_transition
from app.services.workflow.workflow_state import get_step_order
from app.core.constants import WorkflowStepStatus, WorkflowStep
from app.core.exceptions import NotFoundError

def create_workflow(workspace_id: str, product_id: str, dataset_id: str) -> dict:
    """Create a new workflow tracking document."""
    doc = WorkflowModel.create_document(
        workspace_id=workspace_id,
        product_id=product_id,
        dataset_id=dataset_id
    )
    # Initialize steps
    order = get_step_order()
    doc["steps"] = {
        step.name: {"status": WorkflowStepStatus.NOT_STARTED.name, "metadata": {}}
        for step in order
    }
    doc["steps"][order[0].name]["status"] = WorkflowStepStatus.READY.name
    doc["current_step"] = order[0].name
    doc["progress_percentage"] = 0.0
    
    return workflow_repository.create(doc)

def get_workflow(workflow_id: str) -> dict:
    """Get workflow by ID."""
    workflow = workflow_repository.get_by_id(workflow_id)
    if not workflow:
        raise NotFoundError(f"Workflow {workflow_id} not found")
    return workflow

def get_workspace_workflow(workspace_id: str, dataset_id: str) -> dict | None:
    """Get workflow by workspace and dataset."""
    return workflow_repository.get_by_workspace_and_dataset(workspace_id, dataset_id)

def advance_step(workflow_id: str, step_name: str, status: str, metadata: dict = None) -> dict:
    """Advance workflow step."""
    workflow = get_workflow(workflow_id)
    
    is_valid, err = validate_step_transition(workflow, step_name, status)
    if not is_valid:
        raise ValueError(err)
        
    workflow["steps"][step_name]["status"] = status
    if metadata:
        workflow["steps"][step_name]["metadata"] = metadata
        
    workflow["progress_percentage"] = calculate_progress(workflow)
    
    # Update current_step logic
    if status == WorkflowStepStatus.COMPLETED.name:
        order = get_step_order()
        completed = {
            WorkflowStep[s] for s, data in workflow["steps"].items() 
            if data.get("status") == WorkflowStepStatus.COMPLETED.name
        }
        for s in order:
            if s not in completed:
                workflow["current_step"] = s.name
                workflow["steps"][s.name]["status"] = WorkflowStepStatus.READY.name
                break
                
    workflow_repository.update(workflow_id, workflow)
    return workflow

def calculate_progress(workflow: dict) -> float:
    """Calculate completion percentage."""
    steps = workflow.get("steps", {})
    if not steps:
        return 0.0
        
    completed = sum(1 for s in steps.values() if s.get("status") == WorkflowStepStatus.COMPLETED.name)
    return (completed / len(steps)) * 100.0


class WorkflowService:
    def create_workflow(self, workspace_id: str, product_id: str, dataset_id: str) -> dict:
        return create_workflow(workspace_id, product_id, dataset_id)

    def get_workflow(self, workflow_id: str) -> dict:
        return get_workflow(workflow_id)

    def get_workspace_workflow(self, workspace_id: str, dataset_id: str = None) -> dict | None:
        return get_workspace_workflow(workspace_id, dataset_id)

    def advance_step(self, workflow_id: str, step_name: str, status: str, metadata: dict = None) -> dict:
        return advance_step(workflow_id, step_name, status, metadata)

    def calculate_progress(self, workflow: dict) -> float:
        return calculate_progress(workflow)


workflow_service = WorkflowService()
