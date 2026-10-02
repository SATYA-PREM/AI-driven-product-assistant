from __future__ import annotations
from app.core.constants import WorkflowStepStatus, WorkflowStep
from app.services.workflow.workflow_state import can_transition
from app.services.workflow.dependency_service import is_step_ready

def validate_step_transition(workflow: dict, step_name: str, target_status: str) -> tuple[bool, str]:
    """
    Validate if a workflow step can change status.
    """
    steps = workflow.get("steps", {})
    if step_name not in steps:
        return False, f"Step {step_name} not found in workflow"
        
    current_status_str = steps[step_name].get("status", "NOT_STARTED")
    try:
        current_status = WorkflowStepStatus[current_status_str]
        target_stat = WorkflowStepStatus[target_status]
    except KeyError:
        return False, "Invalid status enum"
        
    if not can_transition(current_status, target_stat):
        return False, f"Cannot transition from {current_status.name} to {target_status}"
        
    if target_stat in [WorkflowStepStatus.IN_PROGRESS, WorkflowStepStatus.COMPLETED]:
        step_enum = WorkflowStep[step_name]
        completed = {
            WorkflowStep[s] for s, data in steps.items() 
            if data.get("status") == WorkflowStepStatus.COMPLETED.name
        }
        if not is_step_ready(step_enum, completed):
            return False, f"Dependencies not met for step {step_name}"
            
    return True, ""
