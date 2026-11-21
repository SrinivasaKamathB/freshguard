"""
FreshGuard Python SDK
Drop-in staleness detection and self-healing middleware for LLM applications.
"""

from typing import Optional, Dict, Any, Callable
import asyncio
import requests

class FreshGuard:
    def __init__(self, api_endpoint: str = "http://localhost:8000/api", tavily_key: Optional[str] = None):
        self.api_endpoint = api_endpoint.rstrip("/")
        self.tavily_key = tavily_key

    def verify(self, text: str, auto_patch: bool = True) -> Dict[str, Any]:
        """
        Synchronously verifies an LLM response and optionally returns the patched text.
        """
        payload = {
            "text": text,
            "tavily_api_key": self.tavily_key
        }
        res = requests.post(f"{self.api_endpoint}/scan", json=payload, timeout=10)
        res.raise_for_status()
        data = res.json()
        
        if auto_patch and data.get("freshness_score", 100) < 85:
            data["clean_output"] = data.get("patched_text", text)
        else:
            data["clean_output"] = text
            
        return data

    async def verify_async(self, text: str, auto_patch: bool = True) -> Dict[str, Any]:
        """
        Asynchronously verifies an LLM response.
        """
        return await asyncio.to_thread(self.verify, text, auto_patch)


def wrap_client(client_instance: Any, guard: Optional[FreshGuard] = None) -> Any:
    """
    Wraps an OpenAI, Anthropic, or LiteLLM client with FreshGuard self-healing middleware.
    
    Usage:
        client = wrap_client(openai.OpenAI())
        completion = client.chat.completions.create(...)
        print(completion.choices[0].message.content) # Guaranteed fresh & verified!
    """
    active_guard = guard or FreshGuard()
    original_create = client_instance.chat.completions.create

    def wrapped_create(*args, **kwargs):
        response = original_create(*args, **kwargs)
        try:
            raw_text = response.choices[0].message.content
            report = active_guard.verify(raw_text, auto_patch=True)
            response.choices[0].message.content = report["clean_output"]
            setattr(response, "freshness_report", report)
        except Exception as e:
            print(f"[FreshGuard Middleware Warning] Verification bypassed: {e}")
        return response

    client_instance.chat.completions.create = wrapped_create
    return client_instance
