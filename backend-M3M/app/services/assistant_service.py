from __future__ import annotations

import json
import re
from uuid import uuid4

# Reuse your existing LangGraph app from assistant.py
from assistant import app as assistant_graph

# In-memory store for per-session chat history/state.
# For production, replace with Redis/DB.
_session_state: dict[str, dict] = {}


def _parse_llm_json(raw: str) -> tuple[str, list[dict]]:
    if not raw:
        return "I am processing your request...", []

    cleaned = re.sub(r"```json\s*", "", raw, flags=re.IGNORECASE)
    cleaned = re.sub(r"```", "", cleaned).strip()

    try:
        payload = json.loads(cleaned)
    except Exception:
        return cleaned, []

    answer = str(payload.get("answer") or "").strip() or "I am processing your request..."
    projects = payload.get("projects")
    if not isinstance(projects, list):
        return answer, []

    filtered_projects: list[dict] = []
    for item in projects:
        if not isinstance(item, dict):
            continue
        # Only include projects with image for actual image rendering in UI
        if not item.get("image"):
            continue
        if not item.get("name"):
            continue
        filtered_projects.append(item)

    return answer, filtered_projects


def _new_state(user_message: str, session_id: str) -> dict:
    """Create initial graph state shape compatible with assistant.py GraphState."""
    existing = _session_state.get(session_id, {})
    return {
        "query": user_message,
        "retrieved_docs": [],
        "response": "",
        "history": existing.get("history", []),
        "summary": existing.get("summary", ""),
        "filters": existing.get("filters", {}),
    }


def get_answer(message: str, session_id: str | None = None) -> tuple[str, str, list[dict]]:
    """
    Run chatbot graph and return (session_id, answer).

    Why service layer?
    - keeps route function clean
    - easy to test and replace logic later
    """
    sid = session_id or str(uuid4())
    state = _new_state(user_message=message, session_id=sid)

    # Execute the LangGraph pipeline
    result = assistant_graph.invoke(state)

    # Persist minimal memory for next user turn in same session
    _session_state[sid] = {
        "history": result.get("history", []),
        "summary": result.get("summary", ""),
        "filters": result.get("filters", {}),
    }

    raw_answer = result.get("response", "")
    answer, projects = _parse_llm_json(raw_answer)
    return sid, answer, projects
