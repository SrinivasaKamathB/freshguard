"""
Pre-packaged high-impact scenarios showcasing temporal staleness across:
1. API & Developer Tech
2. SaaS & AI Pricing
3. Corporate Leadership & Mergers
4. Legal & Regulatory Compliance
"""

from typing import Dict, Any

PRESET_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "api_twitter": {
        "title": "Twitter / X API v1.1 Deprecation",
        "category": "API & Technology",
        "prompt": "How do I automate tweets using the Twitter API in Python?",
        "sample_text": (
            "To post a tweet in Python, you should use the Twitter API v1.1 endpoint `https://api.twitter.com/1.1/statuses/update.json`. "
            "You can use Tweepy version 3.10 and authenticate using your consumer API key and secret. "
            "Twitter offers free unlimited access to the standard v1.1 search and post endpoints for hobbyists and developers. "
            "Make sure your HTTP POST request sends the tweet content as the `status` URL parameter."
        ),
        "claims": [
            {
                "claim_id": "c1",
                "text_snippet": "Twitter API v1.1 endpoint `https://api.twitter.com/1.1/statuses/update.json`",
                "category": "API & Technology",
                "status": "stale",
                "confidence": 0.99,
                "explanation": "Twitter completely shut down the v1.1 statuses/update endpoint in 2023. Developers must now use X API v2 at `https://api.x.com/2/tweets`.",
                "current_truth": "Use X API v2 endpoint `POST https://api.x.com/2/tweets` with a JSON payload `{\"text\": \"your tweet\"}`.",
                "sources": [
                    {
                        "title": "X API v2 Migration Guide - Manage Tweets",
                        "url": "https://developer.x.com/en/docs/x-api/tweets/manage-tweets/migrate",
                        "snippet": "The v1.1 statuses/update endpoint has been retired. All developers must use POST /2/tweets.",
                        "published_date": "2024-03-15",
                        "domain_trust": 0.99
                    }
                ],
                "time_history": {
                    "year_2022": "Standard active v1.1 endpoint used by millions.",
                    "year_2024": "Deprecated and read-only; developers urged to migrate.",
                    "year_2026": "Permanently decommissioned. Returns HTTP 410 Gone."
                },
                "impact_warning": "Immediate HTTP 410/403 failure in production pipelines."
            },
            {
                "claim_id": "c2",
                "text_snippet": "Twitter offers free unlimited access to the standard v1.1 search and post endpoints",
                "category": "Pricing & Financial",
                "status": "stale",
                "confidence": 0.98,
                "explanation": "Free API access was drastically restricted to write-only 1,500 tweets/month. Basic tier costs $100/mo, and Pro tier costs $5,000/mo.",
                "current_truth": "X API Free Tier is write-only limited to 1,500 posts/month; Basic tier is $100/mo.",
                "sources": [
                    {
                        "title": "X Developer Platform Access Tiers & Pricing",
                        "url": "https://developer.x.com/en/portal/products",
                        "snippet": "Free tier permits 1,500 Tweets/month posting only. Basic tier starts at $100/month.",
                        "published_date": "2024-01-10",
                        "domain_trust": 0.99
                    }
                ],
                "time_history": {
                    "year_2022": "Free unlimited standard API for hobbyists.",
                    "year_2024": "Introduction of paywalled tiers ($100/mo Basic).",
                    "year_2026": "Strict rate caps, Enterprise tiers up to $42k/mo."
                },
                "impact_warning": "Rate-limit blocks and surprise paywalls."
            },
            {
                "claim_id": "c3",
                "text_snippet": "You can use Tweepy version 3.10",
                "category": "API & Technology",
                "status": "updated",
                "confidence": 0.92,
                "explanation": "Tweepy 3.x only supports v1.1 API. Modern applications require Tweepy 4.14+ with `tweepy.Client` for API v2 support.",
                "current_truth": "Use Tweepy 4.14+ with `tweepy.Client(bearer_token=...)`.",
                "sources": [
                    {
                        "title": "Tweepy Documentation - API v2 Client",
                        "url": "https://docs.tweepy.org/en/stable/client.html",
                        "snippet": "Tweepy v4 introduced Client class specifically supporting Twitter API v2 endpoints.",
                        "published_date": "2024-05-20",
                        "domain_trust": 0.95
                    }
                ],
                "time_history": {
                    "year_2022": "Tweepy 3.10 was the standard package.",
                    "year_2024": "Tweepy 4.x required for OAuth 2.0 and v2 endpoints.",
                    "year_2026": "Tweepy 4.14+ required with updated rate-handling."
                },
                "impact_warning": "Import errors and missing client classes."
            }
        ],
        "patched_text": (
            "To post a post on X (formerly Twitter) in Python, you must use the **X API v2** endpoint `POST https://api.x.com/2/tweets` [Source: developer.x.com]. "
            "You should use **Tweepy version 4.14+** and initialize the client via `tweepy.Client` using OAuth 1.0a User Context or OAuth 2.0 User Token. "
            "Note that free API access is restricted to write-only (1,500 posts/month), while higher volume access requires the Basic tier at $100/month. "
            "Your HTTP request must send a JSON body formatted as `{\"text\": \"your post content\"}` instead of legacy URL parameters."
        ),
        "risk": {
            "downtime_hours": 4.5,
            "financial_risk_usd": "$100/mo unexpected fee",
            "compliance_severity": "Critical",
            "business_impact": "Total bot downtime; HTTP 410 errors blocking customer notification dispatch."
        }
    },
    "pricing_openai": {
        "title": "OpenAI LLM Token Pricing Shift",
        "category": "Pricing & Financial",
        "prompt": "What is the cost of running GPT-4 in production via OpenAI API?",
        "sample_text": (
            "OpenAI charges $30.00 per 1 million input tokens and $60.00 per 1 million output tokens for GPT-4 with an 8k context window. "
            "For the 32k context model, prices rise to $60.00 per 1 million input tokens. "
            "There is no model called GPT-4o, and multi-modal audio input is not supported directly in the API. "
            "OpenAI enforces a strict 128k context ceiling only on preview experimental checkpoints."
        ),
        "claims": [
            {
                "claim_id": "p1",
                "text_snippet": "OpenAI charges $30.00 per 1 million input tokens and $60.00 per 1 million output tokens for GPT-4",
                "category": "Pricing & Financial",
                "status": "stale",
                "confidence": 0.99,
                "explanation": "Legacy GPT-4 (8k) pricing ($30/$60) is obsolete. GPT-4o has slashed pricing down to ~$2.50 per 1M input and $10.00 per 1M output tokens (over 80% cheaper).",
                "current_truth": "Flagship GPT-4o costs ~$2.50 / 1M input tokens and $10.00 / 1M output tokens; GPT-4o-mini is $0.15 / 1M input.",
                "sources": [
                    {
                        "title": "OpenAI API Official Pricing",
                        "url": "https://openai.com/api/pricing/",
                        "snippet": "GPT-4o: $2.50 / 1M input tokens, $10.00 / 1M output tokens. Cached inputs: $1.25 / 1M tokens.",
                        "published_date": "2024-10-01",
                        "domain_trust": 0.99
                    }
                ],
                "time_history": {
                    "year_2022": "GPT-3 Davinci at $20/1M tokens.",
                    "year_2024": "GPT-4 at $30/$60; GPT-4 Turbo dropped to $10/$30.",
                    "year_2026": "GPT-4o at $2.50/$10.00, GPT-4o-mini at $0.15/$0.60."
                },
                "impact_warning": "Severely distorted budget forecasting and 10x over-budget estimates."
            },
            {
                "claim_id": "p2",
                "text_snippet": "There is no model called GPT-4o, and multi-modal audio input is not supported directly in the API",
                "category": "API & Technology",
                "status": "stale",
                "confidence": 0.99,
                "explanation": "GPT-4o was released in May 2024 as OpenAI's omni flagship model, with native Realtime Audio API support.",
                "current_truth": "GPT-4o is the primary model and supports text, vision, and real-time audio modalities via the Realtime API.",
                "sources": [
                    {
                        "title": "Hello GPT-4o - OpenAI Announcement",
                        "url": "https://openai.com/index/hello-gpt-4o/",
                        "snippet": "GPT-4o ('omni') is our new flagship model that can reason across audio, vision, and text in real time.",
                        "published_date": "2024-05-13",
                        "domain_trust": 0.99
                    }
                ],
                "time_history": {
                    "year_2022": "Text-only GPT-3.",
                    "year_2024": "GPT-4o launched with omni-modal audio/vision.",
                    "year_2026": "GPT-4o and o1 reasoning models standard in production."
                },
                "impact_warning": "Missing high-speed multimodal capabilities."
            }
        ],
        "patched_text": (
            "As of current pricing, OpenAI's flagship model **GPT-4o** costs **$2.50 per 1 million input tokens** and **$10.00 per 1 million output tokens** [Source: openai.com/api/pricing], with discounted cached tokens at $1.25. "
            "For cost-sensitive applications, **GPT-4o-mini** offers intelligence at just **$0.15 per 1 million input tokens**. "
            "GPT-4o is fully multimodal, natively processing audio, vision, and text, with real-time audio interaction available via the OpenAI Realtime API."
        ),
        "risk": {
            "downtime_hours": 0.0,
            "financial_risk_usd": "$27,500/yr over-budget error",
            "compliance_severity": "High",
            "business_impact": "Massive budget misallocation; opting out of viable AI projects due to phantom cost barriers."
        }
    },
    "leadership_tech": {
        "title": "Tech Leadership & Corporate Structure",
        "category": "Leadership & People",
        "prompt": "Who is leading Twitter and Figma today?",
        "sample_text": (
            "Twitter is publicly traded on the New York Stock Exchange under the ticker TWTR, with Parag Agrawal serving as Chief Executive Officer. "
            "Meanwhile, Figma has completed its $20 billion merger and is now an official subsidiary of Adobe Inc., governed by Adobe's creative cloud division."
        ),
        "claims": [
            {
                "claim_id": "l1",
                "text_snippet": "Twitter is publicly traded on the New York Stock Exchange under the ticker TWTR, with Parag Agrawal serving as Chief Executive Officer",
                "category": "Leadership & People",
                "status": "stale",
                "confidence": 0.99,
                "explanation": "Twitter was taken private in October 2022 by Elon Musk, delisted from the NYSE, rebranded as X Corp, and Linda Yaccarino was appointed CEO in 2023.",
                "current_truth": "Twitter is now X Corp (private company, delisted from NYSE), with Linda Yaccarino as CEO and Elon Musk as CTO/Owner.",
                "sources": [
                    {
                        "title": "SEC Filing - Twitter Delisting",
                        "url": "https://www.sec.gov/edgar/browse/?CIK=0001418091",
                        "snippet": "Twitter Inc common stock delisted from NYSE following merger into X Holdings.",
                        "published_date": "2022-11-08",
                        "domain_trust": 0.99
                    }
                ],
                "time_history": {
                    "year_2022": "Publicly traded TWTR; Parag Agrawal CEO.",
                    "year_2024": "Privatized as X Corp; Linda Yaccarino named CEO.",
                    "year_2026": "X Corp integrated with xAI Grok ecosystem."
                },
                "impact_warning": "Inaccurate executive communications and SEC regulatory blunders."
            },
            {
                "claim_id": "l2",
                "text_snippet": "Figma has completed its $20 billion merger and is now an official subsidiary of Adobe Inc.",
                "category": "Rules & Regulations",
                "status": "stale",
                "confidence": 0.99,
                "explanation": "Adobe and Figma mutually terminated their $20 billion merger agreement in December 2023 due to antitrust roadblocks from EU and UK regulators. Figma paid a $1B reverse termination fee and remains independent.",
                "current_truth": "Adobe and Figma abandoned the merger in December 2023; Figma remains an independent standalone company led by Dylan Field.",
                "sources": [
                    {
                        "title": "Adobe and Figma Mutually Terminate Merger Agreement",
                        "url": "https://news.adobe.com/news/news-details/2023/Adobe-and-Figma-Mutually-Agree-to-Terminate-Merger-Agreement/default.aspx",
                        "snippet": "Adobe and Figma announced they have entered into a mutual agreement to terminate their previously announced merger.",
                        "published_date": "2023-12-18",
                        "domain_trust": 0.99
                    }
                ],
                "time_history": {
                    "year_2022": "Acquisition announced for $20B pending regulatory approval.",
                    "year_2024": "Merger formally blocked and cancelled; Figma stays independent.",
                    "year_2026": "Figma files for independent IPO."
                },
                "impact_warning": "Legal, contractual, and corporate strategy misinformation."
            }
        ],
        "patched_text": (
            "Twitter was taken private in October 2022 and rebranded under **X Corp** [Source: SEC filings], officially delisting from the NYSE. **Linda Yaccarino** serves as CEO, with Elon Musk as Chief Technology Officer. "
            "Regarding Figma: Adobe and Figma **mutually abandoned the $20 billion acquisition in December 2023** due to antitrust scrutiny in the UK and EU. Figma remains an independent private company led by CEO Dylan Field."
        ),
        "risk": {
            "downtime_hours": 0.0,
            "financial_risk_usd": "Severe M&A legal liability",
            "compliance_severity": "Critical",
            "business_impact": "Executive embarrassment in investor pitch decks and faulty enterprise contracts."
        }
    }
}
