from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from app.schemas.chat import ChatRequest, ChatResponse, ProjectCard
from app.services.assistant_service import get_answer

router = APIRouter()


@router.post("", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    """
    Main chatbot endpoint.

    Frontend sends:
    {
      "message": "Show me 3BHK in Gurgaon",
      "session_id": "optional-previous-id"
    }

    Backend returns answer + session_id for continuity.
    """
    try:
        session_id, answer, projects = get_answer(payload.message, payload.session_id)

        project_cards: list[ProjectCard] = []
        for item in projects:
          try:
            project_cards.append(ProjectCard(**item))
          except (TypeError, ValidationError):
            continue

        return ChatResponse(session_id=session_id, answer=answer, projects=project_cards)
    except Exception as exc:
        # Keep error message controlled for API consumers
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(exc)}")
