from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any
from enum import Enum
import re

class StalenessStatus(str, Enum):
    FRESH = "fresh"         # Verified up-to-date
    UPDATED = "updated"     # Nuance or minor detail changed
    STALE = "stale"         # Obsolete, deprecated, or incorrect

class ClaimCategory(str, Enum):
    API_TECH = "API & Technology"
    PRICING = "Pricing & Financial"
    LEADERSHIP = "Leadership & People"
    REGULATION = "Rules & Regulations"
    GENERAL = "General Fact"

class Evidence(BaseModel):
    title: str = Field(..., max_length=500)
    url: str = Field(..., max_length=2000)
    snippet: str = Field(..., max_length=2000)
    published_date: Optional[str] = Field(None, max_length=100)
    domain_trust: float = Field(0.95, ge=0.0, le=1.0)

class ClaimHistory(BaseModel):
    year_2022: str = Field(..., max_length=1000)
    year_2024: str = Field(..., max_length=1000)
    year_2026: str = Field(..., max_length=1000)

class VerifiedClaim(BaseModel):
    claim_id: str = Field(..., max_length=50)
    text_snippet: str = Field(..., max_length=2000)
    category: ClaimCategory
    status: StalenessStatus
    confidence: float = Field(..., ge=0.0, le=1.0)
    explanation: str = Field(..., max_length=2000)
    current_truth: str = Field(..., max_length=2000)
    sources: List[Evidence] = Field(default_factory=list, max_length=20)
    time_history: Optional[ClaimHistory] = None
    impact_warning: Optional[str] = Field(None, max_length=500)

class RiskAnalysis(BaseModel):
    downtime_hours: float = Field(..., ge=0.0)
    financial_risk_usd: str = Field(..., max_length=100)
    compliance_severity: str = Field(..., max_length=50)
    business_impact: str = Field(..., max_length=1000)

class FreshnessReport(BaseModel):
    session_id: str = Field(..., max_length=50)
    timestamp: str = Field(..., max_length=50)
    original_text: str = Field(..., max_length=50000)
    freshness_score: int = Field(..., ge=0, le=100)
    stale_count: int = Field(..., ge=0)
    updated_count: int = Field(..., ge=0)
    fresh_count: int = Field(..., ge=0)
    claims: List[VerifiedClaim] = Field(default_factory=list)
    patched_text: str = Field(..., max_length=100000)
    risk_analysis: RiskAnalysis
    execution_time_ms: int = Field(..., ge=0)
    search_queries_used: List[str] = Field(default_factory=list, max_length=50)

class ScanRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=50000, description="Text to scan for factual currency")
    prompt: Optional[str] = Field(None, max_length=2000, description="Optional user prompt")
    tavily_api_key: Optional[str] = Field(None, max_length=150, description="Optional Tavily API key")
    model_name: Optional[str] = Field("gpt-4o", max_length=100)

    @field_validator("tavily_api_key")
    @classmethod
    def validate_api_key(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        # Strict validation: prevent CRLF, shell, or header injection
        if not re.match(r"^[A-Za-z0-9_-]{10,128}$", v):
            raise ValueError("Invalid API key format. Must be alphanumeric (10-128 chars).")
        return v
