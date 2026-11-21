from typing import List, Dict, Any

BATTLE_PRESETS = [
    {
        "query": "How do I automate Twitter posting using Python & what is the free tier limit?",
        "models": [
            {
                "name": "Legacy GPT-4 (Static Knowledge)",
                "freshness_score": 28,
                "stale_claims": 3,
                "latency_ms": 1150,
                "verdict": "FAIL (High Risk)",
                "sample_response": "Use `https://api.twitter.com/1.1/statuses/update.json` with Tweepy 3.10. Twitter gives free unlimited access to the standard v1.1 search and update endpoints for developers."
            },
            {
                "name": "Llama-3 (Standard Cutoff)",
                "freshness_score": 45,
                "stale_claims": 2,
                "latency_ms": 980,
                "verdict": "PARTIAL (Moderate Risk)",
                "sample_response": "You can use Tweepy to connect to the Twitter API. Note that Twitter recently transitioned toward Twitter API v2, but v1.1 endpoints are still widely referenced for basic tweet updates."
            },
            {
                "name": "FreshGuard Verified Agent",
                "freshness_score": 98,
                "stale_claims": 0,
                "latency_ms": 1420,
                "verdict": "VERIFIED FRESH",
                "sample_response": "Use X API v2 at `POST https://api.x.com/2/tweets` with Tweepy 4.14+. Free tier is restricted to write-only 1,500 posts/month; Basic tier starts at $100/month."
            }
        ]
    },
    {
        "query": "What is OpenAI GPT-4 API pricing for 1M input tokens?",
        "models": [
            {
                "name": "Legacy GPT-4 (Static Knowledge)",
                "freshness_score": 15,
                "stale_claims": 2,
                "latency_ms": 1100,
                "verdict": "FAIL (Severe Staleness)",
                "sample_response": "OpenAI charges $30.00 per 1 million input tokens for GPT-4 with an 8k context window, and $60.00 per 1M tokens for the 32k version."
            },
            {
                "name": "Claude 3 Sonnet (Unaugmented)",
                "freshness_score": 55,
                "stale_claims": 1,
                "latency_ms": 890,
                "verdict": "PARTIAL",
                "sample_response": "OpenAI introduced GPT-4 Turbo with lower pricing ($10/1M input tokens), but pricing changes frequently across tiers."
            },
            {
                "name": "FreshGuard Verified Agent",
                "freshness_score": 100,
                "stale_claims": 0,
                "latency_ms": 1350,
                "verdict": "VERIFIED FRESH",
                "sample_response": "OpenAI's flagship GPT-4o costs $2.50 per 1M input tokens ($1.25 for cached inputs) and $10.00 per 1M output tokens. GPT-4o-mini is priced at $0.15/1M."
            }
        ]
    }
]

def get_battle_scenarios() -> List[Dict[str, Any]]:
    return BATTLE_PRESETS
