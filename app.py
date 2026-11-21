import os
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from backend.models import ScanRequest, FreshnessReport
from backend.engine import FreshGuardEngine
from backend.presets import PRESET_SCENARIOS
from backend.models_battle import get_battle_scenarios
from backend.telemetry import telemetry_store
from backend.rag_auditor import RAGAuditor
from backend.policy_engine import policy_engine, PolicyConfig
from backend.gateway import gateway_handler, GatewayChatCompletionRequest

MAX_REQUEST_SIZE = 1_048_576  # 1 MB limit to prevent memory exhaustion DoS

app = FastAPI(
    title="FreshGuard Enterprise AI Gateway & Staleness Firewall",
    description="Drop-in LLM proxy, temporal knowledge firewall, and continuous RAG auditor.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url=None
)

# 1. Security Headers Middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://fonts.googleapis.com https://fonts.gstatic.com https://unpkg.com; "
            "img-src 'self' data: https:; "
            "connect-src 'self' http: https:;"
        )
        return response

app.add_middleware(SecurityHeadersMiddleware)

# 2. Request Size Limiting Middleware
class RequestSizeLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_REQUEST_SIZE:
            return JSONResponse(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                content={"detail": "Payload exceeds maximum allowed size (1MB)."}
            )
        return await call_next(request)

app.add_middleware(RequestSizeLimiterMiddleware)

# 3. CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# --- 1. OpenAI-Compatible Gateway Endpoint (/v1/chat/completions) ---
@app.post("/v1/chat/completions")
async def openai_chat_completions(req_body: GatewayChatCompletionRequest, raw_req: Request, response: Response):
    """
    Drop-in replacement for OpenAI API: https://api.openai.com/v1/chat/completions
    Intercepts LLM requests, evaluates temporal currency, and auto-patches or blocks stale output.
    """
    return await gateway_handler.handle_completion(req_body, raw_req, response)

# --- 2. Enterprise Telemetry & Observability Endpoints ---
@app.get("/api/telemetry/stats")
async def get_telemetry_stats():
    return telemetry_store.get_stats()

@app.get("/api/telemetry/logs")
async def get_telemetry_logs():
    return {"logs": telemetry_store.get_logs(30)}

# --- 3. Continuous RAG Vector Knowledge Base Auditor ---
from pydantic import BaseModel
class DocumentAuditInput(BaseModel):
    document_text: str
    tavily_api_key: str = None

@app.post("/api/rag/audit")
async def audit_rag_document(input_data: DocumentAuditInput):
    auditor = RAGAuditor(tavily_key=input_data.tavily_api_key)
    return await auditor.audit_document(input_data.document_text)

# --- 4. Policy & Compliance Firewall Endpoints ---
@app.get("/api/policy")
async def get_policy():
    return policy_engine.get_policy()

@app.post("/api/policy")
async def update_policy(config: PolicyConfig):
    return policy_engine.update_policy(config)

# --- 5. Core Verification & Preset Endpoints ---
@app.get("/api/health")
async def health_check():
    return {"status": "ok", "service": "FreshGuard Enterprise Gateway", "version": "2.0.0"}

@app.get("/api/presets")
async def get_presets():
    return {
        "presets": [
            {
                "id": k,
                "title": v["title"],
                "category": v["category"],
                "prompt": v["prompt"],
                "sample_text": v["sample_text"]
            }
            for k, v in PRESET_SCENARIOS.items()
        ]
    }

@app.get("/api/presets/{preset_id}")
async def get_preset_detail(preset_id: str):
    if preset_id not in PRESET_SCENARIOS:
        raise HTTPException(status_code=404, detail="Preset scenario not found")
    return PRESET_SCENARIOS[preset_id]

@app.post("/api/scan", response_model=FreshnessReport)
async def scan_text(request: ScanRequest):
    cleaned_text = request.text.strip()
    if not cleaned_text:
        raise HTTPException(status_code=400, detail="Input text cannot be blank")
    
    engine = FreshGuardEngine(tavily_api_key=request.tavily_api_key)
    report = await engine.analyze(cleaned_text, prompt=request.prompt)
    return report

@app.get("/api/battle")
async def get_battles():
    return {"battles": get_battle_scenarios()}

# Mount Static Files (Frontend UI)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse({"message": "FreshGuard Enterprise API active."})

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 7860))
    host = os.getenv("HOST", "127.0.0.1")
    uvicorn.run("app:app", host=host, port=port, reload=False)
