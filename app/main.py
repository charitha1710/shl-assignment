from fastapi import FastAPI

from .recommender import is_query_vague, recommend_from_catalog
from .schemas import ChatRequest, ChatResponse

app = FastAPI(title="SHL AI Intern Assignment")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest):
    """Stateless chat endpoint that returns catalog recommendations."""
    user_message = get_latest_user_message(payload.messages)
    recommendations = get_recommendations(user_message)
    reply = build_reply(user_message, recommendations)
    end_of_conversation = False

    return ChatResponse(
        reply=reply,
        recommendations=recommendations,
        end_of_conversation=end_of_conversation,
    )


def get_latest_user_message(messages: list) -> str:
    """Extract the last user message from the messages list."""
    for message in reversed(messages):
        if message.role == "user":
            return message.content.strip()
    return ""


def build_reply(message: str, recommendations: list) -> str:
    """Create a reply based on whether the query produced relevant recommendations."""
    if is_query_vague(message) or not recommendations:
        return "Could you please clarify which SHL assessment type you want recommendations for?"
    return "Here are the SHL assessment recommendations based on your query."


def get_recommendations(message: str):
    """Get top recommendations from the catalog or return an empty list when there are no relevant matches."""
    if is_query_vague(message):
        return []
    return recommend_from_catalog(message)
