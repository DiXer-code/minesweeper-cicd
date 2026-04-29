"""Utilities for persisting high scores."""
import json
import os
from typing import Optional

DEFAULT_PLAYER_NAME = "Unknown"
MAX_ENTRIES = 5
_SCORES_FILE = os.path.join(os.path.dirname(__file__), "..", "scores.json")


def load_scores() -> dict:
    """Load all scores from disk. Return an empty dict on missing or invalid data."""
    if not os.path.exists(_SCORES_FILE):
        return {}
    try:
        with open(_SCORES_FILE, "r", encoding="utf-8") as file_handle:
            return json.load(file_handle)
    except (json.JSONDecodeError, OSError):
        return {}


def save_scores(scores: dict) -> None:
    """Persist the full score mapping to disk."""
    with open(_SCORES_FILE, "w", encoding="utf-8") as file_handle:
        json.dump(scores, file_handle, indent=2, ensure_ascii=False)


def get_best_time(difficulty: str) -> Optional[int]:
    """Return the best recorded time for the given difficulty."""
    entries = load_scores().get(difficulty, [])
    if not entries:
        return None

    times = [entry["time"] if isinstance(entry, dict) else entry for entry in entries]
    return min(times) if times else None


def get_leaderboard(difficulty: str) -> list[dict]:
    """Return the sorted leaderboard for the given difficulty."""
    entries = load_scores().get(difficulty, [])
    normalized_entries = []

    for entry in entries:
        if isinstance(entry, dict):
            normalized_entries.append(entry)
        else:
            normalized_entries.append({"name": DEFAULT_PLAYER_NAME, "time": entry})

    normalized_entries.sort(key=lambda item: item["time"])
    return normalized_entries[:MAX_ENTRIES]


def record_time(
    difficulty: str,
    elapsed: int,
    player_name: str = DEFAULT_PLAYER_NAME,
) -> bool:
    """Save a new score and return True when it is a new best time."""
    scores = load_scores()
    entries = scores.get(difficulty, [])
    normalized_entries = []

    for entry in entries:
        if isinstance(entry, dict):
            normalized_entries.append(entry)
        else:
            normalized_entries.append({"name": DEFAULT_PLAYER_NAME, "time": entry})

    previous_best = min((entry["time"] for entry in normalized_entries), default=None)
    normalized_entries.append(
        {
            "name": player_name.strip() or DEFAULT_PLAYER_NAME,
            "time": elapsed,
        }
    )
    normalized_entries.sort(key=lambda item: item["time"])
    scores[difficulty] = normalized_entries[:MAX_ENTRIES]
    save_scores(scores)

    return previous_best is None or elapsed < previous_best
