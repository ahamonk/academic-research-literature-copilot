from pydantic import BaseModel


class SlackConnectResponse(BaseModel):
    authorize_url: str


class SlackStatusResponse(BaseModel):
    connected: bool
    enabled: bool
    workspace_name: str | None = None


class SlackToggleRequest(BaseModel):
    enabled: bool


class ScheduledUserItem(BaseModel):
    user_id: int
    email: str


class SendReviewResponse(BaseModel):
    success: bool
    detail: str