import json
import re
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from .schemas import Recommendation

CATALOG_PATH = Path(__file__).resolve().parent / "catalog.json"
TARGET_KEYWORDS = [
    "java",
    "python",
    "sql",
    "personality",
    "numerical",
    "verbal",
    "customer service",
    "sales",
]


def load_catalog() -> List[Dict[str, Any]]:
    """Load the assessment catalog from the JSON file."""
    with CATALOG_PATH.open("r", encoding="utf-8") as catalog_file:
        return json.load(catalog_file)


COMMON_TOKENS_TO_IGNORE = {"assessment", "assessments", "skill", "skills"}


def tokenize_text(text: str) -> Set[str]:
    """Convert a string into a set of normalized keyword tokens."""
    return set(re.findall(r"\b[a-z0-9]+\b", text.lower()))


def calculate_entry_score(entry: Dict[str, Any], message_lower: str, tokens: Set[str]) -> int:
    """Score a catalog entry based on keyword matches in the user query."""
    score = 0

    # Phrase and tag matches are the strongest signal.
    for tag in entry.get("tags", []):
        tag_text = tag.lower()
        tag_tokens = tokenize_text(tag_text) - COMMON_TOKENS_TO_IGNORE

        if tag_text in message_lower:
            score += 5
        elif tokens.intersection(tag_tokens):
            score += 2

    # Match the explicit test_type field as a helpful signal.
    test_type = entry.get("test_type", "").lower()
    if test_type in message_lower:
        score += 3

    # Only count strong keyword matches from the assessment name.
    name_tokens = tokenize_text(entry.get("name", "")) - COMMON_TOKENS_TO_IGNORE
    score += sum(1 for token in tokens.intersection(name_tokens) if token in TARGET_KEYWORDS)

    return score


def recommend_from_catalog(message: str) -> List[Recommendation]:
    """Return the top three relevant catalog recommendations for the user query."""
    message_lower = message.lower()
    tokens = tokenize_text(message_lower)
    catalog = load_catalog()
    scored_matches: List[Tuple[int, Recommendation]] = []

    for entry in catalog:
        score = calculate_entry_score(entry, message_lower, tokens)
        if score <= 0:
            continue

        scored_matches.append(
            (
                score,
                Recommendation(
                    name=entry["name"],
                    url=entry["url"],
                    test_type=entry["test_type"],
                ),
            )
        )

    # Sort by relevance score and return only the top 3 matches.
    scored_matches.sort(key=lambda item: item[0], reverse=True)
    return [recommendation for _, recommendation in scored_matches[:3]]


def is_query_vague(message: str) -> bool:
    """Detect vague queries that do not mention a supported assessment type."""
    if not message.strip():
        return True

    message_lower = message.lower()
    return not any(keyword in message_lower for keyword in TARGET_KEYWORDS)
