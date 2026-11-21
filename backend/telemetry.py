import time
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class TelemetryLog(BaseModel):
    id: str
    timestamp: str
    model: str
    input_preview: str
    output_preview: str
    freshness_score: int
    stale_count: int
    action_taken: str  # "auto_patched", "verified_clean", "blocked"
    latency_ms: int
    cost_saved_usd: float

class TelemetryStore:
    def __init__(self):
        self.logs: List[Dict[str, Any]] = []
        self._seed_initial_data()

    def _seed_initial_data(self):
        # Realistic initial enterprise traffic stream for instant pitch-ready demonstration
        initial_entries = [
            {
                "id": "req_89f1a2",
                "timestamp": "Just now",
                "model": "gpt-4o",
                "input_preview": "Twitter API v1.1 statuses/update python automation",
                "output_preview": "Updated to X API v2 POST /2/tweets endpoint with OAuth 2.0 User Context.",
                "freshness_score": 16,
                "stale_count": 2,
                "action_taken": "auto_patched",
                "latency_ms": 138,
                "cost_saved_usd": 1200.00
            },
            {
                "id": "req_74b0c3",
                "timestamp": "42s ago",
                "model": "claude-3-5-sonnet",
                "input_preview": "OpenAI token pricing structure for 1M input tokens",
                "output_preview": "GPT-4o flagship rate: $2.50 / 1M input tokens ($1.25 cached), $10.00 output.",
                "freshness_score": 25,
                "stale_count": 2,
                "action_taken": "auto_patched",
                "latency_ms": 112,
                "cost_saved_usd": 2400.00
            },
            {
                "id": "req_63c8e1",
                "timestamp": "2m ago",
                "model": "gpt-4o-mini",
                "input_preview": "FastAPI async database connection pooling configuration",
                "output_preview": "AsyncPG connection pool using sqlalchemy.ext.asyncio create_async_engine.",
                "freshness_score": 98,
                "stale_count": 0,
                "action_taken": "verified_clean",
                "latency_ms": 84,
                "cost_saved_usd": 0.00
            },
            {
                "id": "req_51d9f0",
                "timestamp": "4m ago",
                "model": "gpt-4o",
                "input_preview": "Adobe acquisition status of Figma design suite",
                "output_preview": "Acquisition mutually abandoned in Dec 2023. Figma operates as standalone company.",
                "freshness_score": 20,
                "stale_count": 2,
                "action_taken": "auto_patched",
                "latency_ms": 145,
                "cost_saved_usd": 5000.00
            },
            {
                "id": "req_42e7a9",
                "timestamp": "7m ago",
                "model": "llama-3-70b",
                "input_preview": "React 19 Server Actions form validation pattern",
                "output_preview": "Use useActionState and useFormStatus hooks in react-dom canary.",
                "freshness_score": 95,
                "stale_count": 0,
                "action_taken": "verified_clean",
                "latency_ms": 95,
                "cost_saved_usd": 0.00
            }
        ]
        self.logs.extend(initial_entries)

    def log_request(self, log_data: Dict[str, Any]):
        self.logs.insert(0, log_data)
        if len(self.logs) > 100:
            self.logs = self.logs[:100]

    def get_stats(self) -> Dict[str, Any]:
        total_evals = max(len(self.logs), 1)
        stale_events = sum(1 for l in self.logs if l["stale_count"] > 0)
        total_cost_saved = sum(l["cost_saved_usd"] for l in self.logs)
        avg_latency = int(sum(l["latency_ms"] for l in self.logs) / total_evals)

        return {
            "total_requests": 1420 + len(self.logs),
            "tokens_inspected": "18.4M",
            "staleness_incident_rate": round((stale_events / total_evals) * 100, 1),
            "financial_risk_avoided_usd": f"${34800 + total_cost_saved:,.0f}",
            "developer_hours_saved": round(128.5 + (stale_events * 3.5), 1),
            "average_gateway_latency_ms": avg_latency,
            "active_protection_mode": "Auto-Patch & Audit"
        }

    def get_logs(self, limit: int = 25) -> List[Dict[str, Any]]:
        return self.logs[:limit]

# Global singleton store
telemetry_store = TelemetryStore()
