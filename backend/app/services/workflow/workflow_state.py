from __future__ import annotations
from app.core.constants import WorkflowStepStatus, WorkflowStep

VALID_TRANSITIONS = {
    WorkflowStepStatus.NOT_STARTED: [WorkflowStepStatus.READY, WorkflowStepStatus.IN_PROGRESS],
    WorkflowStepStatus.READY: [WorkflowStepStatus.IN_PROGRESS, WorkflowStepStatus.BLOCKED],
    WorkflowStepStatus.IN_PROGRESS: [WorkflowStepStatus.COMPLETED, WorkflowStepStatus.FAILED, WorkflowStepStatus.BLOCKED],
    WorkflowStepStatus.FAILED: [WorkflowStepStatus.READY, WorkflowStepStatus.IN_PROGRESS],
    WorkflowStepStatus.BLOCKED: [WorkflowStepStatus.READY, WorkflowStepStatus.NOT_STARTED],
    WorkflowStepStatus.COMPLETED: []
}

def can_transition(current: WorkflowStepStatus, target: WorkflowStepStatus) -> bool:
    """Check if a workflow step can transition to the target state."""
    if current == target:
        return True
    return target in VALID_TRANSITIONS.get(current, [])

def get_step_order() -> list[WorkflowStep]:
    """Returns steps in pipeline order."""
    return [
        WorkflowStep.AUTH,
        WorkflowStep.WORKSPACE,
        WorkflowStep.PRODUCT,
        WorkflowStep.UPLOAD,
        WorkflowStep.INGESTION,
        WorkflowStep.VALIDATION,
        WorkflowStep.CLEANING,
        WorkflowStep.NORMALIZATION,
        WorkflowStep.PREPROCESSING,
        WorkflowStep.AI_ANALYSIS
    ]
