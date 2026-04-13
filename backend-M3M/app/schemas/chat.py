from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User message")
    session_id: str | None = Field(default=None, description="Conversation session id")


class ProjectCard(BaseModel):
    name: str
    location: str | None = None
    bhk_options: list[str] = Field(default_factory=list)
    price_range: str | None = None
    amenities: list[str] = Field(default_factory=list)
    link: str | None = None
    image: str | None = None


class ChatResponse(BaseModel):
    session_id: str
    answer: str
    projects: list[ProjectCard] = Field(default_factory=list)