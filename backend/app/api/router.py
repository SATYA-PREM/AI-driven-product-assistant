"""
router.py
---------
Central API Router aggregating all v1 endpoints for the Product Intelligence Platform.
Powers the full Swagger UI documentation at /docs.
"""

from fastapi import APIRouter
from app.api.v1 import (
    auth,
    users,
    workspaces,
    products,
    data,
    validation,
    cleaning,
    preprocessing,
    pm_validation,
    analysis,
    intelligence,
    assistant,
    phases,
    reports,
    tasks,
    jobs,
    workflow,
    health,
)

api_router = APIRouter(prefix="/api/v1")

# Core & Administration
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(workspaces.router)
api_router.include_router(products.router)

# Data Ingestion & Preprocessing Pipeline
api_router.include_router(data.router)
api_router.include_router(validation.router)
api_router.include_router(cleaning.router)
api_router.include_router(preprocessing.router)
api_router.include_router(pm_validation.router)

# AI Intelligence & Strategy
api_router.include_router(analysis.router)
api_router.include_router(intelligence.router)
api_router.include_router(assistant.router)

# Operations, Reporting & Lifecycle
api_router.include_router(phases.router)
api_router.include_router(reports.router)
api_router.include_router(tasks.router)
api_router.include_router(jobs.router)
api_router.include_router(workflow.router)
api_router.include_router(health.router)