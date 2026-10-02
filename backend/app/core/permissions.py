"""
permissions.py
---------------
RBAC permission definitions and checking utilities.

Maps each role to its allowed actions. The permission_service
uses this to enforce access control.
"""

from __future__ import annotations

from app.core.constants import Permission, UserRole


# ──────────────────────────────────────────────
# Role → Permission mapping
# ──────────────────────────────────────────────

ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.PRODUCT_MANAGER: {
        # Workspace
        Permission.CREATE_WORKSPACE,
        Permission.VIEW_WORKSPACE,
        Permission.UPDATE_WORKSPACE,
        Permission.DELETE_WORKSPACE,
        Permission.MANAGE_MEMBERS,
        # Product
        Permission.CREATE_PRODUCT,
        Permission.VIEW_PRODUCT,
        Permission.UPDATE_PRODUCT,
        # Data
        Permission.UPLOAD_DATASET,
        Permission.VIEW_DATASET,
        Permission.DELETE_DATASET,
        Permission.RUN_PIPELINE,
        # Intelligence
        Permission.VIEW_INTELLIGENCE,
        # PM-specific
        Permission.GENERATE_PRD,
        Permission.ASSIGN_TASKS,
        Permission.VALIDATE_PLAN,
        # Tasks
        Permission.COMPLETE_TASK,
        Permission.VIEW_TASKS,
    },
    UserRole.DATA_ENGINEER: {
        # Workspace (read-only)
        Permission.VIEW_WORKSPACE,
        # Product (read-only)
        Permission.VIEW_PRODUCT,
        # Data (full pipeline control)
        Permission.UPLOAD_DATASET,
        Permission.VIEW_DATASET,
        Permission.DELETE_DATASET,
        Permission.RUN_PIPELINE,
        # Intelligence & Tasks
        Permission.VIEW_INTELLIGENCE,
        Permission.COMPLETE_TASK,
        Permission.VIEW_TASKS,
    },
    UserRole.PRODUCT_DESIGNER: {
        Permission.VIEW_WORKSPACE,
        Permission.VIEW_PRODUCT,
        Permission.VIEW_DATASET,
        Permission.VIEW_INTELLIGENCE,
        Permission.COMPLETE_TASK,
        Permission.VIEW_TASKS,
    },
    UserRole.ENGINEERING_LEAD: {
        Permission.VIEW_WORKSPACE,
        Permission.VIEW_PRODUCT,
        Permission.VIEW_DATASET,
        Permission.VIEW_INTELLIGENCE,
        Permission.ASSIGN_TASKS,
        Permission.COMPLETE_TASK,
        Permission.VIEW_TASKS,
    },
    UserRole.CUSTOMER_SUCCESS: {
        Permission.VIEW_WORKSPACE,
        Permission.VIEW_PRODUCT,
        Permission.UPLOAD_DATASET,
        Permission.VIEW_DATASET,
        Permission.VIEW_INTELLIGENCE,
        Permission.COMPLETE_TASK,
        Permission.VIEW_TASKS,
    },
    UserRole.MEMBER: {
        # Workspace (read-only)
        Permission.VIEW_WORKSPACE,
        # Product (read-only)
        Permission.VIEW_PRODUCT,
        # Data (read-only)
        Permission.VIEW_DATASET,
        # Intelligence
        Permission.VIEW_INTELLIGENCE,
        # Tasks
        Permission.COMPLETE_TASK,
        Permission.VIEW_TASKS,
    },
}

# Link PM alias to PRODUCT_MANAGER permissions
ROLE_PERMISSIONS[UserRole.PM] = ROLE_PERMISSIONS[UserRole.PRODUCT_MANAGER]



def has_permission(role: UserRole | str, permission: Permission) -> bool:
    """
    Check whether a role has a specific permission.

    Args:
        role: The user's role (as enum or string).
        permission: The action to check.

    Returns:
        True if the role is permitted to perform the action.
    """
    if isinstance(role, str):
        try:
            role = UserRole(role)
        except ValueError:
            return False

    allowed = ROLE_PERMISSIONS.get(role, set())
    return permission in allowed


def get_role_permissions(role: UserRole | str) -> set[Permission]:
    """
    Get all permissions for a given role.

    Args:
        role: The user's role.

    Returns:
        Set of permitted actions.
    """
    if isinstance(role, str):
        try:
            role = UserRole(role)
        except ValueError:
            return set()

    return ROLE_PERMISSIONS.get(role, set())
