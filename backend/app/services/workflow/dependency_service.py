from __future__ import annotations
from app.core.constants import WorkflowStep
from app.services.workflow.workflow_state import get_step_order

def get_dependencies(step: WorkflowStep) -> list[WorkflowStep]:
    """Get steps that must complete before this step."""
    order = get_step_order()
    try:
        idx = order.index(step)
        return order[:idx]
    except ValueError:
        return []

def is_step_ready(step: WorkflowStep, completed_steps: set[WorkflowStep]) -> bool:
    """Check if all dependencies are met."""
    deps = get_dependencies(step)
    return all(d in completed_steps for d in deps)

def get_next_step(completed_steps: set[WorkflowStep]) -> WorkflowStep | None:
    """Get the next logical step to execute."""
    order = get_step_order()
    for step in order:
        if step not in completed_steps and is_step_ready(step, completed_steps):
            return step
    return None

def get_blocked_steps(completed_steps: set[WorkflowStep]) -> list[WorkflowStep]:
    """Get steps that cannot be started yet."""
    order = get_step_order()
    blocked = []
    for step in order:
        if step not in completed_steps and not is_step_ready(step, completed_steps):
            blocked.append(step)
    return blocked
