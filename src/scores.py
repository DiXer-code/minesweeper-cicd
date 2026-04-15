"""
High score management: reads and writes best completion times per difficulty.
Scores are persisted to scores.json in the project root.
"""
import json
import os
from typing import Optional

_SCORES_FILE = os.path.join(os.path.dirname(__file__), "..", "scores.json")
MAX_ENTRIES = 3


def load_scores() -> dict:
    """Load all scores from the JSON file. Returns empty dict on missing/corrupt file."""
    if not os.path.exists(_SCORES_FILE):
        return {}
    try:
        with open(_SCORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_scores(scores: dict) -> None:
    """Persist the full scores dict to the JSON file."""
    with open(_SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)


def get_best_time(difficulty: str) -> Optional[int]:
    """Return the fastest recorded time (seconds) for the given difficulty, or None."""
    times = load_scores().get(difficulty, [])
    return min(times) if times else None


def record_time(difficulty: str, elapsed: int) -> bool:
    """
    Save a new completion time for the given difficulty.
    Keeps only the top MAX_ENTRIES fastest times.

    Returns True if this is a new personal best.
    """
    scores = load_scores()
    times = scores.get(difficulty, [])
    previous_best = min(times) if times else None
    times.append(elapsed)
    times.sort()
    scores[difficulty] = times[:MAX_ENTRIES]
    save_scores(scores)
    return previous_best is None or elapsed < previous_best
