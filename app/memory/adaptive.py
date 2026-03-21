from app.memory.hindsight import reflect_on_user

def get_adaptive_context(user_id: str, problem_topic: str) -> dict:
    """
    Uses Hindsight reflect to reason about the user's
    past patterns and return adaptive instructions for the LLM.
    """
    question = (
        f"Based on this user's history, what are their weak areas "
        f"and how should I adapt my hints for a problem about {problem_topic}?"
    )

    reflection = reflect_on_user(user_id=user_id, question=question)

    return {
        "user_id": user_id,
        "topic": problem_topic,
        "adaptive_instruction": reflection
    }

def build_llm_prompt(user_id: str, problem: str, user_code: str, topic: str) -> str:
    """
    Builds a memory-aware prompt for the LLM (Person 3 will call this).
    """
    context = get_adaptive_context(user_id, topic)
    instruction = context.get("adaptive_instruction", "")

    prompt = f"""
You are an adaptive coding mentor.

User Memory Context:
{instruction}

Problem:
{problem}

User's Code:
{user_code}

Based on the user's past behavior patterns, give a personalized hint.
Do NOT give away the answer. Adapt your tone and depth to their weak areas.
"""
    return prompt.strip()