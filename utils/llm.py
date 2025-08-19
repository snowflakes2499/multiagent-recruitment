# utils/llm.py
import requests
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"

def ollama_generate(prompt: str, model: str = "gemma:2b", temperature: float = 0.2, timeout: int = 120) -> str:
    """
    Query local Ollama server. If Ollama isn't reachable or times out,
    returns an informative fallback string (not an exception).
    """
    try:
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature}
        }
        r = requests.post(OLLAMA_URL, json=payload, timeout=timeout)
        r.raise_for_status()
        data = r.json()
        # Ollama responses vary; try common shapes
        if isinstance(data, dict) and "response" in data:
            return data.get("response", "").strip()
        # fallback - convert to str safely
        return str(data)
    except Exception as e:
        return f"[LLM Fallback] Model not available.\nError: {e}\nPrompt head: {prompt[:200]}"
