import json
import os

LEADERBOARD_FILE = "leaderboard.json"

def load_leaderboard() -> list[dict]:
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
            return sorted(data, key=lambda entry: entry["score"], reverse=True)[:10]
    except (json.JSONDecodeError, OSError):
        return []

def save_score(initials: str, score: int) -> list[dict]:
    scores = load_leaderboard()
    scores.append({"initials": initials.upper(), "score": score})
    scores.sort(key=lambda entry: entry["score"], reverse=True)
    top_scores = scores[:10]
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(top_scores, f, indent=2)
    except OSError as e:
        print(f"Failed to save score: {e}")
    return top_scores
