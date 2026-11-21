import re
import uuid
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from backend.models import StalenessStatus, ClaimCategory
from backend.engine import FreshGuardEngine

class RAGChunkAudit(BaseModel):
    chunk_id: str
    chunk_index: int
    content_snippet: str
    freshness_score: int
    status: str  # "HEALTHY", "WARNING", "DECAYED"
    primary_category: str
    detected_stale_facts: List[str]
    suggested_update: str
    action_required: str  # "No action", "Review", "Immediate Re-index"

class RAGAuditReport(BaseModel):
    document_id: str
    total_chunks: int
    overall_health_score: int
    decayed_chunks_count: int
    warning_chunks_count: int
    healthy_chunks_count: int
    chunks: List[RAGChunkAudit]
    audit_summary: str
    estimated_indexing_cost_saved: str

class RAGAuditor:
    def __init__(self, tavily_key: str = None):
        self.engine = FreshGuardEngine(tavily_api_key=tavily_key)

    async def audit_document(self, document_text: str, chunk_size: int = 350) -> RAGAuditReport:
        doc_id = f"doc_{uuid.uuid4().hex[:6]}"
        paragraphs = [p.strip() for p in document_text.split("\n\n") if len(p.strip()) > 20]
        if not paragraphs:
            paragraphs = [document_text[i:i+chunk_size] for i in range(0, len(document_text), chunk_size)]

        audited_chunks: List[RAGChunkAudit] = []
        
        for idx, para in enumerate(paragraphs[:8]):  # Up to 8 chunks for snappy audit response
            chunk_id = f"chk_{idx+1}"
            report = await self.engine.analyze(para)
            
            stale_facts = [c.text_snippet for c in report.claims if c.status == StalenessStatus.STALE]
            
            if report.freshness_score >= 80:
                status = "HEALTHY"
                action = "No action needed (Vector healthy)"
            elif report.freshness_score >= 50:
                status = "WARNING"
                action = "Flagged for periodic review"
            else:
                status = "DECAYED"
                action = "Immediate Re-embedding Recommended"

            audited_chunks.append(
                RAGChunkAudit(
                    chunk_id=chunk_id,
                    chunk_index=idx + 1,
                    content_snippet=para[:180] + ("..." if len(para) > 180 else ""),
                    freshness_score=report.freshness_score,
                    status=status,
                    primary_category=report.claims[0].category.value if report.claims else "General",
                    detected_stale_facts=stale_facts,
                    suggested_update=report.patched_text[:200] + "...",
                    action_required=action
                )
            )

        decayed = sum(1 for c in audited_chunks if c.status == "DECAYED")
        warning = sum(1 for c in audited_chunks if c.status == "WARNING")
        healthy = sum(1 for c in audited_chunks if c.status == "HEALTHY")
        total = len(audited_chunks) or 1
        overall_health = int(((healthy * 1.0 + warning * 0.5) / total) * 100)

        return RAGAuditReport(
            document_id=doc_id,
            total_chunks=total,
            overall_health_score=overall_health,
            decayed_chunks_count=decayed,
            warning_chunks_count=warning,
            healthy_chunks_count=healthy,
            chunks=audited_chunks,
            audit_summary=f"Found {decayed} decayed vector chunks requiring re-indexing to prevent AI hallucination drift.",
            estimated_indexing_cost_saved=f"${decayed * 450 + warning * 120:,.0f} in prevented hallucination support tickets"
        )
