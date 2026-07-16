from pydantic import BaseModel


class TopicResponse(BaseModel):
    id: int
    code: str
    name: str
    discipline: str | None = None


class TopicSelectRequest(BaseModel):
    topic_ids: list[int]


class MessageResponse(BaseModel):
    message: str