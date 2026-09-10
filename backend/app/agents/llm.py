"""
llm.py
------
Centralized LLM initialization and configuration for CrewAI agents.
Ensures consistent model settings and authentication across all agents in the multi-agent system.
"""

from __future__ import annotations

from typing import Optional
from crewai import LLM

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


def get_llm(model: Optional[str] = None, temperature: float = 0.2) -> Optional[LLM]:
    """
    Get a configured CrewAI LLM instance.

    Uses Gemini by default via LiteLLM provider syntax ('gemini/<model_name>').
    If GEMINI_API_KEY is not configured, returns None so agents can run
    in tool-only or mock execution modes.

    Args:
        model: Specific model name to override the default settings.GEMINI_MODEL.
        temperature: Sampling temperature for generation.

    Returns:
        Configured CrewAI LLM instance, or None if no API key is set.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        logger.warning("GEMINI_API_KEY not set; LLM capabilities for CrewAI agents will be disabled.")
        return None

    model_name = model or settings.GEMINI_MODEL
    # CrewAI / LiteLLM expects 'gemini/' prefix for Google Gemini models
    if not model_name.startswith("gemini/"):
        model_name = f"gemini/{model_name}"

    try:
        llm = LLM(
            model=model_name,
            api_key=api_key,
            temperature=temperature,
        )
        return llm
    except Exception as e:
        logger.error(f"Failed to initialize CrewAI LLM with model {model_name}: {e}")
        return None

