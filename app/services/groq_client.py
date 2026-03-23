"""
groq_client.py — Person 3 (LLM & Feedback Service)
Handles all communication with the Groq API.
Place: app/services/groq_client.py
"""

import os
import httpx
from typing import Optional


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"


class GroqClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not set. Add it to your .env file.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> str:
        """
        Send a chat request to Groq and return the response text.
        """
        payload = {
            "model": GROQ_MODEL,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    GROQ_API_URL, headers=self.headers, json=payload
                )
                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"].strip()

        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Groq API error {e.response.status_code}: {e.response.text}"
            )
        except httpx.RequestError as e:
            raise RuntimeError(f"Network error calling Groq: {str(e)}")
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Unexpected Groq response format: {str(e)}")