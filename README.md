# SHL AI Intern FastAPI Project

A minimal FastAPI project for the SHL AI Intern assignment.

## Endpoints

- `GET /health`
  - Returns service status.
  - Example response: `{ "status": "ok" }`

- `POST /chat`
  - Accepts a stateless JSON request with a `messages` array.
  - Returns a chat-style response with:
    - `reply`
    - `recommendations`
    - `end_of_conversation`

## Request Schema

The `/chat` endpoint expects a payload like:

```json
{
  "messages": [
    {"role": "user", "content": "I need a Python assessment recommendation."}
  ]
}
```

## Response Schema

```json
{
  "reply": "...",
  "recommendations": [
    {
      "name": "...",
      "url": "...",
      "test_type": "..."
    }
  ],
  "end_of_conversation": false
}
```

## Project Structure

- `app/main.py` - FastAPI application entrypoint
- `app/schemas.py` - Pydantic request/response models
- `app/recommender.py` - keyword scoring and recommendation logic
- `app/catalog.json` - sample SHL assessment catalog

## Installation

1. Create and activate a Python virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn app.main:app --reload
```

## Example Usage

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Recommend a Python assessment."}]}'
```

## Example Response

```json
{
  "reply": "Here are the SHL assessment recommendations based on your query.",
  "recommendations": [
    {
      "name": "Python Developer Assessment",
      "url": "https://example.com/shl/python-assessment",
      "test_type": "technical"
    }
  ],
  "end_of_conversation": false
}
```

## Notes

- The recommendation engine scores catalog entries by relevance.
- Only the top 3 matching assessments are returned.
- Vague queries return a clarification prompt and empty recommendations.
