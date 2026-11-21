from typing import Dict, Any, List
from pydantic import BaseModel, Field

class PolicyConfig(BaseModel):
    enforcement_mode: str = Field("AUTO_PATCH", description="AUTO_PATCH, STRICT_BLOCK, or AUDIT_ONLY")
    min_freshness_threshold: int = Field(70, ge=0, le=100)
    pricing_zero_tolerance: bool = Field(True, description="Enforce strict zero tolerance on financial discrepancy")
    api_auto_migration: bool = Field(True, description="Auto-migrate decommissioned API endpoints")
    alert_webhook_url: str = Field("https://hooks.slack.com/services/T00/B00/XXXXX", max_length=500)
    audit_logging_enabled: bool = Field(True)

class PolicyEngine:
    def __init__(self):
        self.config = PolicyConfig()

    def get_policy(self) -> PolicyConfig:
        return self.config

    def update_policy(self, new_config: PolicyConfig) -> PolicyConfig:
        self.config = new_config
        return self.config

    def evaluate(self, freshness_score: int, stale_count: int, has_pricing_discrepancy: bool) -> Dict[str, Any]:
        """
        Evaluates incoming inference against enterprise policy rules.
        """
        if self.config.pricing_zero_tolerance and has_pricing_discrepancy and self.config.enforcement_mode == "STRICT_BLOCK":
            return {
                "decision": "BLOCKED",
                "reason": "Policy Violation: Strict Zero-Tolerance on unverified pricing claims.",
                "action": "Response suppressed and escalated to compliance queue."
            }

        if freshness_score < self.config.min_freshness_threshold:
            if self.config.enforcement_mode == "STRICT_BLOCK":
                return {
                    "decision": "BLOCKED",
                    "reason": f"Freshness Score {freshness_score}% is below required enterprise threshold {self.config.min_freshness_threshold}%.",
                    "action": "Output blocked from delivery."
                }
            elif self.config.enforcement_mode == "AUTO_PATCH":
                return {
                    "decision": "AUTO_PATCHED",
                    "reason": f"Detected {stale_count} stale assertions; self-healed using Tavily ground truth.",
                    "action": "Patched content substituted transparently in response stream."
                }

        return {
            "decision": "PASSED",
            "reason": "Meets enterprise freshness & currency policy.",
            "action": "Delivered without modification."
        }

# Global singleton
policy_engine = PolicyEngine()
