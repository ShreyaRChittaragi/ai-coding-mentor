import os
import json
import re
import uuid
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROBLEMS_FILE = os.path.join(os.path.dirname(__file__), "problems.json")

# In-memory cache for generated problems
_generated_cache: dict = {}

def get_generated_problem(problem_id: str):
    return _generated_cache.get(problem_id, None)

def generate_problem(topic: str, difficulty: str) -> dict:
    prompt = f"""
Generate a Python coding problem with the following:
- topic: {topic}
- difficulty: {difficulty}

CRITICAL RULES — follow exactly or the output is unusable:
1. The function must take ONLY simple parameters that match the test case inputs exactly
2. test_cases input keys must be ALL the parameters the function needs — nothing missing
3. Do NOT create functions with default source/target/auxiliary parameters
4. Keep functions simple — 1 or 2 parameters maximum
5. expected values must be the exact Python return value (int, list, str, bool)
6. Respond ONLY with valid JSON — no explanation, no markdown

Format:
{{
  "id": "gen_001",
  "title": "Problem Title",
  "description": "Clear problem description",
  "difficulty": "{difficulty}",
  "topic": "{topic}",
  "examples": [
    {{"input": "example input", "output": "example output"}}
  ],
  "test_cases": [
    {{"input": {{"param1": value}}, "expected": value}},
    {{"input": {{"param1": value}}, "expected": value}},
    {{"input": {{"param1": value}}, "expected": value}}
  ],
  "function_name": "function_name",
  "starter_code": "def function_name(param1):\\n    pass"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    problem = json.loads(raw)

    # Give it a unique id
    problem["id"] = "gen_" + str(uuid.uuid4())[:8]

    # Save to cache so submit_code can find it
    _generated_cache[problem["id"]] = problem

    with open(PROBLEMS_FILE, "r") as f:
        existing = json.load(f)

    existing.append(problem)

    # Only add if title doesn't already exist
    titles = [p["title"] for p in existing]
    if problem["title"] not in titles:
        existing.append(problem)
        with open(PROBLEMS_FILE, "w") as f:
            json.dump(existing, f, indent=2)

    return problem