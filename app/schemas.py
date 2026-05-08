from typing import List, Literal

from pydantic import BaseModel, Field


class MessageItem(BaseModel):
    role: Literal["user", "assistant"] = Field(..., description="Role of the message author.")
    content: str = Field(..., description="Message content.")


class ChatRequest(BaseModel):
    messages: List[MessageItem] = Field(..., description="Conversation messages array.")


class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str


class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Recommendation]
    end_of_conversation: bool
