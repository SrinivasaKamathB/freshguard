import time
import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from fastapi import Request, Response
from backend.engine import FreshGuardEngine
from backend.telemetry import telemetry_store
from backend.policy_engine import policy_engine
from backend.presets import PRESET_SCENARIOS

class GatewayMessage(BaseModel):
    role: str = "user"
    content: str

class GatewayChatCompletionRequest(BaseModel):
    model: str = "gpt-4o"
    messages: List[GatewayMessage]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000
    stream: Optional[bool] = False

class GatewayHandler:
    def __init__(self):
        self.engine = FreshGuardEngine()

    async def handle_completion(self, request: GatewayChatCompletionRequest, raw_req: Request, response: Response) -> Dict[str, Any]:
        start_time = time.time()
        session_id = f"chatcmpl-fg-{uuid.uuid4().hex[:8]}"

        # Extract last user query
        user_prompt = ""
        for msg in reversed(request.messages):
            if msg.role == "user":
                user_prompt = msg.content
                break

        if not user_prompt:
            user_prompt = "Hello from AI"

        # Check for simulated legacy response or evaluate content
        # For demonstration, map query or run through engine
        simulated_legacy_text = ""
        t_low = user_prompt.lower()
        if "twitter" in t_low or "tweet" in t_low or "tweepy" in t_low:
            simulated_legacy_text = PRESET_SCENARIOS["api_twitter"]["sample_text"]
        elif "pricing" in t_low or "token" in t_low or "cost" in t_low:
            simulated_legacy_text = PRESET_SCENARIOS["pricing_openai"]["sample_text"]
        elif "figma" in t_low or "adobe" in t_low:
            simulated_legacy_text = PRESET_SCENARIOS["leadership_tech"]["sample_text"]
        else:
            simulated_legacy_text = user_prompt

        report = await self.engine.analyze(simulated_legacy_text, prompt=user_prompt)
        
        # Policy evaluation
        policy_verdict = policy_engine.evaluate(
            freshness_score=report.freshness_score,
            stale_count=report.stale_count,
            has_pricing_discrepancy=(report.freshness_score < 50 and "price" in user_prompt.lower())
        )

        # Decide delivered content based on policy
        if policy_verdict["decision"] == "BLOCKED":
            delivered_content = f"⛔ [FreshGuard Security Gateway Block] Response blocked: {policy_verdict['reason']}"
            action_label = "blocked"
            cost_saved = 0.0
        elif policy_verdict["decision"] == "AUTO_PATCHED":
            delivered_content = report.patched_text
            action_label = "auto_patched"
            cost_saved = float(report.stale_count * 1200.0)
        else:
            delivered_content = simulated_legacy_text
            action_label = "verified_clean"
            cost_saved = 0.0

        latency_ms = int((time.time() - start_time) * 1000)

        # Inject HTTP telemetry headers for client inspection
        response.headers["X-FreshGuard-Session-ID"] = session_id
        response.headers["X-FreshGuard-Freshness-Score"] = str(report.freshness_score)
        response.headers["X-FreshGuard-Status"] = action_label
        response.headers["X-FreshGuard-Latency-MS"] = str(latency_ms)

        # Log into real-time telemetry store
        telemetry_store.log_request({
            "id": session_id,
            "timestamp": "Just now",
            "model": request.model,
            "input_preview": user_prompt[:80],
            "output_preview": delivered_content[:100] + "...",
            "freshness_score": report.freshness_score,
            "stale_count": report.stale_count,
            "action_taken": action_label,
            "latency_ms": latency_ms,
            "cost_saved_usd": cost_saved
        })

        # Return standard OpenAI completion schema
        return {
            "id": session_id,
            "object": "chat.completion",
            "created": int(time.time()),
            "model": f"freshguard-{request.model}-verified",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": delivered_content
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(user_prompt.split()),
                "completion_tokens": len(delivered_content.split()),
                "total_tokens": len(user_prompt.split()) + len(delivered_content.split())
            },
            "freshguard": {
                "freshness_score": report.freshness_score,
                "status": action_label,
                "stale_claims_detected": report.stale_count,
                "latency_ms": latency_ms,
                "policy_decision": policy_verdict["decision"],
                "policy_reason": policy_verdict["reason"]
            }
        }

gateway_handler = GatewayHandler()
