from app.memory.hindsight import retrieve_memory
from app.services.problem_store import (
    get_all_problems,
    get_problems_by_difficulty,
    get_problems_by_topic
)

# Pattern → what kind of problem to give next
PATTERN_STRATEGY = {
    "overthinking": {
        "difficulty": "easy",
        "reason": "Simpler problem to build confidence and reduce overanalysis"
    },
    "guessing": {
        "difficulty": "easy",
        "reason": "Easy problem to force deliberate step-by-step thinking"
    },
    "rushing": {
        "difficulty": "medium",
        "reason": "Harder problem that punishes rushing and rewards careful reading"
    },
    "concept_gap": {
        "difficulty": "easy",
        "reason": "Back to basics to fill the knowledge gap"
    },
    "boundary_weakness": {
        "difficulty": "medium",
        "reason": "Medium problem with tricky edge cases to practice boundary thinking"
    },
    "gives_up_early": {
        "difficulty": "easy",
        "reason": "Easy win to rebuild confidence and persistence"
    }
}

def get_dominant_pattern(user_id: str) -> str:
    """Get the most frequent recent pattern for a user."""
    memory = retrieve_memory(user_id)
    patterns = memory.get("patterns", [])

    if not patterns:
        return "none"

    # Count pattern frequency from last 5 sessions
    recent = patterns[-5:]
    freq = {}
    for p in recent:
        name = p.get("pattern", "none")
        freq[name] = freq.get(name, 0) + 1

    return max(freq, key=freq.get)

def get_next_problem(user_id: str, current_problem_id: str = None) -> dict:
    """
    Pick the best next problem based on user's behavioral memory.
    Avoids repeating the current problem.
    """
    dominant = get_dominant_pattern(user_id)
    strategy = PATTERN_STRATEGY.get(dominant)

    all_problems = get_all_problems()

    # Filter out current problem
    candidates = [
        p for p in all_problems
        if p["id"] != current_problem_id
    ]

    if not candidates:
        return {
            "problem": None,
            "reason": "No other problems available",
            "pattern_used": dominant
        }

    # If we have a strategy, filter by difficulty
    if strategy:
        filtered = [
            p for p in candidates
            if p["difficulty"] == strategy["difficulty"]
        ]
        # If filtered list is empty fall back to all candidates
        if filtered:
            candidates = filtered

    # Pick the first candidate
    # (can be made smarter with topic-based filtering later)
    chosen = candidates[0]

    return {
        "problem": chosen,
        "reason": strategy["reason"] if strategy else "No pattern detected yet — starting with a default problem",
        "pattern_used": dominant
    }