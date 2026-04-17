"""
High score management: reads and writes best completion times per difficulty with player names.
Scores are persisted to scores.json in the project root.
"""
import json
import os
from typing import Optional

_SCORES_FILE = os.path.join(os.path.dirname(__file__), "..", "scores.json")
MAX_ENTRIES = 5


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
    entries = load_scores().get(difficulty, [])
    if not entries:
        return None
    times = [e["time"] if isinstance(e, dict) else e for e in entries]
    return min(times) if times else None


def get_leaderboard(difficulty: str) -> list[dict]:
    """Return sorted list of top scores with player names for the given difficulty."""
    entries = load_scores().get(difficulty, [])
    # Handle both old format (list of times) and new format (list of dicts)
    result = []
    for e in entries:
        if isinstance(e, dict):
            result.append(e)
        else:
            result.append({"name": "Невідомо", "time": e})
    # Sort by time and return top MAX_ENTRIES
    result.sort(key=lambda x: x["time"])
    return result[:MAX_ENTRIES]


def record_time(difficulty: str, elapsed: int, player_name: str = "Невідомо") -> bool:
    """
    Save a new completion time for the given difficulty with player name.
    Keeps only the top MAX_ENTRIES fastest times.

    Returns True if this is a new personal best.
    """
    scores = load_scores()
    entries = scores.get(difficulty, [])
    
    # Migrate old format to new format
    migrated = []
    for e in entries:
        if isinstance(e, dict):
            migrated.append(e)
        else:
            migrated.append({"name": "Невідомо", "time": e})
    
    previous_best = min([e["time"] for e in migrated], default=None)
    
    new_entry = {"name": player_name.strip() or "Невідомо", "time": elapsed}
    migrated.append(new_entry)
    migrated.sort(key=lambda x: x["time"])
    scores[difficulty] = migrated[:MAX_ENTRIES]
    save_scores(scores)
    
    return previous_best is None or elapsed < previous_best
