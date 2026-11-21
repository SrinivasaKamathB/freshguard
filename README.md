# FreshGuard

FreshGuard is a real-time verification proxy and knowledge auditor that detects outdated information in large language model responses and automatically patches it using live web ground truth from the Tavily Search API.

Developed for the Global AI Hackathon under the theme **AI Agents & Intelligent Systems** (Problem Statement 6: Stale-Answer Detector).

---

## Overview

Language models cannot update their internal weights after training cutoffs. Consequently, they often deliver answers containing obsolete API endpoints, superseded pricing schedules, or outdated regulations.

FreshGuard acts as an intermediary layer between your application and your language model:
1. Decomposes model outputs into atomic factual assertions.
2. Identifies time-sensitive entities (versions, pricing, leadership, policies).
3. Queries live web sources using Tavily Search to verify current status.
4. Generates an objective freshness score (0-100%).
5. Provides an automated patch replacing stale assertions with verified facts and source citations.

---

## Core Features

- **OpenAI-Compatible Proxy (`/v1/chat/completions`)**: A drop-in replacement endpoint for OpenAI client libraries that transparently intercepts, verifies, and patches model outputs.
- **Interactive Staleness Radar**: A web dashboard displaying a radial freshness score gauge, color-coded claim heatmaps, and a side-by-side verification diff.
- **Tavily Evidence Drawer**: Displays external web citations, publication timestamps, and snippet proofs for all evaluated assertions.
- **RAG Knowledge Base Auditor**: Scans document excerpts and vector chunks to identify decaying knowledge before it gets retrieved by an AI pipeline.
- **Telemetry Stream**: Tracks request throughput, model drift, evaluated latency, and financial risk mitigation.
- **Knowledge Decay Simulation**: A time slider allowing users to observe how assertions transition from active standards to deprecated states over time.
- **Policy Engine**: Configurable rules for automated patching versus strict blocking of unverified claims.

---

## Project Structure

```
freshguard/
├── app.py                 # FastAPI application, proxy router, and static file mount
├── backend/
│   ├── gateway.py         # OpenAI-compatible /v1/chat/completions handler
│   ├── engine.py          # Claim decomposition and staleness evaluation
│   ├── search_service.py  # Tavily Search API client and fallback store
│   ├── telemetry.py       # Metrics collection and request logging
│   ├── rag_auditor.py     # Document chunk freshness auditor
│   ├── policy_engine.py   # Guardrail policy configuration
│   ├── models.py          # Data models and validation schemas
│   ├── presets.py         # Standard test scenarios
│   └── models_battle.py   # Model comparison data
├── static/
│   └── index.html         # Web console interface
├── sdk/
│   └── freshguard.py      # Client middleware wrapper
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Optional: Tavily Search API key (for live web queries)

### Installation

```bash
git clone https://github.com/SrinivasaKamathB/freshguard.git
cd freshguard
pip install -r requirements.txt
```

### Configuration

To enable live web searches via Tavily, export your API key:

```bash
export TAVILY_API_KEY="your-tavily-api-key"
```

If no key is configured, the system uses built-in grounded reference scenarios.

### Running the Server

```bash
python3 -m uvicorn app:app --port 7860
```

Access the interface in your browser at `http://localhost:7860`.

---

## Usage Examples

### Using the Gateway Proxy

Configure any OpenAI-compatible client to route requests through FreshGuard:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:7860/v1",
    api_key="placeholder-key"
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "How do I post tweets with Twitter API v1.1?"}]
)

print(response.choices[0].message.content)
```

### Direct HTTP Request

```bash
curl http://localhost:7860/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"OpenAI GPT-4 token pricing"}]}'
```

---

## Security and Validation

- **Input Sanitization**: HTML entity escaping is enforced prior to DOM insertion to prevent script injection.
- **Payload Limits**: HTTP request bodies are limited to 1 MB to prevent resource exhaustion.
- **Header Protection**: Standard security headers are configured, including `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY`.
- **Credential Hygiene**: API tokens are validated with strict character constraints and are omitted from telemetry logs and error responses.

---

## License

This project is released under the MIT License.
