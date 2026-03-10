"""
IntelCredit - Research Agent Service (The "Digital Credit Manager")
Performs secondary research via web crawling and integrates primary insights.
Crawls news, regulatory filings, litigation history for the company.
"""
import re
import json
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime


class ResearchAgent:
    """
    The Digital Credit Manager - performs automated secondary research:
    - News sentiment analysis for company and promoters
    - Sector-specific headwinds/tailwinds
    - Litigation history from e-Courts
    - MCA filing analysis
    - Regulatory risk assessment
    - Primary insight integration
    """
    
    def __init__(self):
        self.risk_keywords = {
            "high_risk": [
                "fraud", "scam", "default", "NPA", "wilful defaulter", "money laundering",
                "SFIO investigation", "ED raid", "CBI probe", "SEBI ban", "insider trading",
                "ponzi", "shell company", "benami", "tax evasion", "prosecution"
            ],
            "medium_risk": [
                "litigation", "dispute", "NCLT", "insolvency", "IBC", "debt restructuring",
                "downgrade", "rating watch", "regulatory action", "penalty", "fine",
                "audit qualification", "going concern", "stressed asset", "RBI caution"
            ],
            "low_risk": [
                "slowdown", "competition", "margin pressure", "delayed project",
                "management change", "promoter pledge", "related party", "contingent liability"
            ],
            "positive": [
                "expansion", "new order", "contract win", "rating upgrade", "profit growth",
                "debt reduction", "capacity addition", "market leader", "innovation",
                "government contract", "PLI scheme", "Make in India"
            ]
        }
        
        self.sector_risk_map = {
            "nbfc": ["RBI regulations", "NBFC liquidity crisis", "asset quality concerns"],
            "real_estate": ["RERA compliance", "unsold inventory", "delayed projects"],
            "infrastructure": ["government spending", "project delays", "working capital pressure"],
            "manufacturing": ["raw material costs", "capacity utilization", "export demand"],
            "it_services": ["deal pipeline", "attrition rate", "visa regulations"],
            "textiles": ["raw material volatility", "export incentives", "seasonal demand"],
            "pharma": ["FDA observations", "price control", "API dependency on China"],
            "steel": ["commodity cycle", "dumping concerns", "environmental norms"],
            "power": ["fuel availability", "tariff rationalization", "discom health"],
            "telecom": ["AGR dues", "spectrum cost", "competitive intensity"],
        }
    
    async def conduct_research(self, company_name: str, promoters: List[str] = None,
                                sector: str = None, cin: str = None) -> Dict[str, Any]:
        """
        Conduct comprehensive secondary research on a company.
        In production, this would use actual web APIs. For prototype, uses simulation.
        """
        research = {
            "company_name": company_name,
            "research_date": datetime.now().isoformat(),
            "news_analysis": await self._analyze_news(company_name, promoters),
            "litigation_check": await self._check_litigation(company_name, cin),
            "regulatory_check": await self._check_regulatory(company_name, cin),
            "sector_analysis": self._analyze_sector(sector),
            "management_check": await self._check_management(promoters or []),
            "mca_filing_check": await self._check_mca_filings(cin),
            "overall_sentiment": "neutral",
            "risk_flags": [],
            "positive_indicators": [],
            "research_summary": "",
        }
        
        # Consolidate findings
        research = self._consolidate_research(research)
        
        return research
    
    async def _analyze_news(self, company_name: str, promoters: List[str] = None) -> Dict[str, Any]:
        """
        Analyze news articles related to the company and promoters.
        Simulated for prototype - in production would use NewsAPI, Google News, etc.
        """
        # Simulated news analysis based on company characteristics
        news_data = {
            "articles_found": 15,
            "time_period": "Last 12 months",
            "sentiment_breakdown": {
                "positive": 6,
                "neutral": 5,
                "negative": 4,
            },
            "key_articles": [
                {
                    "title": f"{company_name} reports strong Q3 results, revenue up 15%",
                    "source": "Economic Times",
                    "date": "2026-01-15",
                    "sentiment": "positive",
                    "relevance": 0.92,
                    "summary": f"{company_name} reported a 15% YoY increase in revenue driven by strong domestic demand and new client wins."
                },
                {
                    "title": f"Sector outlook remains cautious amid global headwinds",
                    "source": "Business Standard",
                    "date": "2026-02-01",
                    "sentiment": "neutral",
                    "relevance": 0.78,
                    "summary": "Industry analysts flag concern over global trade tensions impacting export-oriented companies."
                },
                {
                    "title": f"{company_name} faces GST scrutiny for input tax credit claims",
                    "source": "Mint",
                    "date": "2025-11-20",
                    "sentiment": "negative",
                    "relevance": 0.85,
                    "summary": f"GST authorities have initiated inquiry into {company_name}'s ITC claims for FY2024-25."
                },
                {
                    "title": f"{company_name} bags ₹200 Cr order from government PSU",
                    "source": "Financial Express",
                    "date": "2026-02-15",
                    "sentiment": "positive",
                    "relevance": 0.88,
                    "summary": f"{company_name} secured a major government contract worth ₹200 Cr, boosting order book."
                },
                {
                    "title": f"Banks tighten lending norms for mid-sized corporates",
                    "source": "Reuters India",
                    "date": "2026-01-05",
                    "sentiment": "negative",
                    "relevance": 0.65,
                    "summary": "Several banks have increased collateral requirements and tightened credit appraisal processes."
                }
            ],
            "promoter_news": [],
        }
        
        if promoters:
            for promoter in promoters[:3]:
                news_data["promoter_news"].append({
                    "promoter": promoter,
                    "articles_found": 3,
                    "negative_flags": [],
                    "summary": f"No significant adverse news found for {promoter}. Clean track record in public domain."
                })
        
        return news_data
    
    async def _check_litigation(self, company_name: str, cin: str = None) -> Dict[str, Any]:
        """
        Check litigation history from e-Courts, NCLT, etc.
        Simulated for prototype.
        """
        return {
            "total_cases_found": 4,
            "active_cases": 2,
            "disposed_cases": 2,
            "cases": [
                {
                    "case_number": "CS/2024/1234",
                    "court": "High Court of Karnataka",
                    "parties": f"{company_name} vs M/s ABC Traders",
                    "subject": "Recovery of trade receivables",
                    "status": "pending",
                    "amount_involved": 3.45,  # In Crores
                    "risk_impact": "low",
                    "filed_date": "2024-06-15",
                },
                {
                    "case_number": "NCLT/BNG/2025/567",
                    "court": "NCLT Bangalore Bench",
                    "parties": f"M/s XYZ Corp vs {company_name}",
                    "subject": "Disputed payment for services rendered",
                    "status": "pending",
                    "amount_involved": 8.75,
                    "risk_impact": "medium",
                    "filed_date": "2025-03-22",
                },
                {
                    "case_number": "IT/APPEAL/2024/890",
                    "court": "Income Tax Appellate Tribunal",
                    "parties": f"CIT vs {company_name}",
                    "subject": "Disputed tax demand for AY 2022-23",
                    "status": "disposed",
                    "amount_involved": 1.20,
                    "risk_impact": "low",
                    "resolution": "Resolved in favor of company",
                },
                {
                    "case_number": "GST/ADJ/2025/345",
                    "court": "GST Appellate Authority",
                    "parties": f"DGGI vs {company_name}",
                    "subject": "Input tax credit eligibility dispute",
                    "status": "disposed",
                    "amount_involved": 0.56,
                    "risk_impact": "low",
                    "resolution": "Partial relief granted",
                }
            ],
            "total_exposure": 13.96,  # Total amount at risk in Crores
            "active_exposure": 12.20,
            "litigation_risk": "moderate",
        }
    
    async def _check_regulatory(self, company_name: str, cin: str = None) -> Dict[str, Any]:
        """Check regulatory filings and compliance status."""
        return {
            "roc_compliance": "compliant",
            "gst_compliance": "minor_issues",
            "income_tax_compliance": "compliant",
            "labour_law_compliance": "compliant",
            "environmental_clearance": "valid",
            "sebi_compliance": "not_applicable",
            "rbi_compliance": "not_applicable",
            "flags": [
                "GST returns filed with minor delays in 2 out of 12 months"
            ],
            "last_annual_return_filed": "2024-25",
            "charges_registered": 3,
            "charge_details": [
                {
                    "charge_holder": "State Bank of India",
                    "amount": 500.00,
                    "type": "Hypothecation of movable assets",
                    "status": "active",
                },
                {
                    "charge_holder": "HDFC Bank",
                    "amount": 300.00,
                    "type": "Mortgage of immovable property",
                    "status": "active",
                },
                {
                    "charge_holder": "Punjab National Bank",
                    "amount": 150.00,
                    "type": "Term loan facility",
                    "status": "satisfied",
                }
            ]
        }
    
    def _analyze_sector(self, sector: str = None) -> Dict[str, Any]:
        """Analyze sector-specific risks and outlook."""
        if not sector:
            sector = "manufacturing"
        
        sector_key = sector.lower().replace(" ", "_")
        risks = self.sector_risk_map.get(sector_key, ["general market conditions"])
        
        sector_data = {
            "sector": sector,
            "outlook": "stable",
            "growth_forecast": "5-8% YoY",
            "key_risks": risks,
            "key_drivers": [
                "Government infrastructure spending",
                "Domestic demand recovery",
                "Digital transformation initiatives",
            ],
            "regulatory_changes": [
                "New compliance requirements under Companies Act 2013 amendments",
                "Updated transfer pricing regulations",
                "ESG reporting requirements for large corporates",
            ],
            "peer_comparison": {
                "industry_avg_margin": 12.5,
                "industry_avg_de_ratio": 1.8,
                "industry_avg_roe": 14.0,
            }
        }
        
        return sector_data
    
    async def _check_management(self, promoters: List[str]) -> Dict[str, Any]:
        """Check management/promoter background."""
        management_data = {
            "promoters_checked": len(promoters),
            "director_disqualification": False,
            "wilful_defaulter_check": "clear",
            "cibil_check": "satisfactory",
            "political_exposure": False,
            "related_entities": [],
            "details": [],
        }
        
        for promoter in promoters:
            management_data["details"].append({
                "name": promoter,
                "din_status": "active",
                "disqualified": False,
                "wilful_defaulter": False,
                "other_directorships": 3,
                "past_company_defaults": 0,
                "experience_years": 15,
                "background": f"Experienced professional with track record in the industry",
            })
        
        return management_data
    
    async def _check_mca_filings(self, cin: str = None) -> Dict[str, Any]:
        """Check Ministry of Corporate Affairs filings."""
        return {
            "filing_status": "regular",
            "last_agm_date": "2025-09-30",
            "balance_sheet_filed": True,
            "annual_return_filed": True,
            "director_changes": [
                {"date": "2025-04-01", "type": "appointment", "name": "Mr. Rajesh Kumar", "designation": "Independent Director"}
            ],
            "share_capital_changes": [],
            "registered_charges": 3,
            "strike_off_status": "not_applicable",
            "flags": [],
        }
    
    def _consolidate_research(self, research: Dict[str, Any]) -> Dict[str, Any]:
        """Consolidate all research findings into summary."""
        risk_flags = []
        positive_indicators = []
        
        # News sentiment
        news = research.get("news_analysis", {})
        sentiment = news.get("sentiment_breakdown", {})
        neg_ratio = sentiment.get("negative", 0) / max(sum(sentiment.values()), 1)
        
        if neg_ratio > 0.4:
            risk_flags.append("High proportion of negative news coverage")
            research["overall_sentiment"] = "negative"
        elif neg_ratio < 0.2:
            positive_indicators.append("Predominantly positive/neutral news coverage")
            research["overall_sentiment"] = "positive"
        else:
            research["overall_sentiment"] = "mixed"
        
        # Litigation
        litigation = research.get("litigation_check", {})
        active_exposure = litigation.get("active_exposure", 0)
        if active_exposure > 10:
            risk_flags.append(f"Significant litigation exposure of ₹{active_exposure} Cr")
        
        # Regulatory
        regulatory = research.get("regulatory_check", {})
        for flag in regulatory.get("flags", []):
            risk_flags.append(f"Regulatory: {flag}")
        
        # Management
        mgmt = research.get("management_check", {})
        if mgmt.get("wilful_defaulter_check") != "clear":
            risk_flags.append("CRITICAL: Wilful defaulter flag on promoter/director")
        if mgmt.get("director_disqualification"):
            risk_flags.append("CRITICAL: Director disqualification found")
        
        # Positive signals
        for article in news.get("key_articles", []):
            if article.get("sentiment") == "positive" and article.get("relevance", 0) > 0.8:
                positive_indicators.append(f"Positive: {article['title']}")
        
        sector = research.get("sector_analysis", {})
        if sector.get("outlook") in ["positive", "strong"]:
            positive_indicators.append(f"Sector outlook: {sector['outlook']}")
        
        research["risk_flags"] = risk_flags
        research["positive_indicators"] = positive_indicators
        
        # Generate summary
        summary_parts = []
        summary_parts.append(f"Secondary research on {research['company_name']} reveals {research['overall_sentiment']} overall sentiment.")
        
        if risk_flags:
            summary_parts.append(f"\n\nKey Risk Flags ({len(risk_flags)}):")
            for flag in risk_flags:
                summary_parts.append(f"  • {flag}")
        
        if positive_indicators:
            summary_parts.append(f"\n\nPositive Indicators ({len(positive_indicators)}):")
            for ind in positive_indicators[:5]:
                summary_parts.append(f"  • {ind}")
        
        lit_summary = f"\n\nLitigation: {litigation.get('total_cases_found', 0)} cases found, " \
                      f"{litigation.get('active_cases', 0)} active, " \
                      f"total exposure ₹{litigation.get('total_exposure', 0)} Cr"
        summary_parts.append(lit_summary)
        
        summary_parts.append(f"\n\nSector Outlook: {sector.get('outlook', 'stable')} " \
                           f"with {sector.get('growth_forecast', 'N/A')} growth forecast")
        
        research["research_summary"] = "\n".join(summary_parts)
        
        return research
    
    def integrate_primary_insights(
        self,
        insights: List[Dict[str, Any]],
        current_score: float
    ) -> Dict[str, Any]:
        """
        Integrate primary due diligence insights (site visits, management interviews)
        into the risk assessment. Adjusts the score based on qualitative observations.
        """
        adjustment = 0
        insight_impacts = []
        
        severity_weights = {
            "critical": -15,
            "warning": -8,
            "info": 0,
            "positive": 5,
        }
        
        # Keyword-based sentiment for insights
        negative_keywords = [
            "low capacity", "idle", "poor condition", "outdated", "non-operational",
            "vacant", "resigned", "dispute", "uncooperative", "evasive",
            "discrepancy", "inconsistent", "shell", "no activity",
        ]
        
        positive_keywords = [
            "well maintained", "high capacity", "modern", "expansion",
            "transparent", "cooperative", "strong team", "good governance",
            "clean", "organized", "growth", "profitable",
        ]
        
        for insight in insights:
            observation = insight.get("observation", "").lower()
            severity = insight.get("severity", "info")
            category = insight.get("category", "general")
            
            # Base adjustment from severity
            base_adj = severity_weights.get(severity, 0)
            
            # Keyword analysis
            neg_count = sum(1 for kw in negative_keywords if kw in observation)
            pos_count = sum(1 for kw in positive_keywords if kw in observation)
            
            keyword_adj = (pos_count * 3) - (neg_count * 5)
            
            total_adj = base_adj + keyword_adj
            adjustment += total_adj
            
            impact_desc = "positive" if total_adj > 0 else ("negative" if total_adj < 0 else "neutral")
            
            insight_impacts.append({
                "observation": insight.get("observation", ""),
                "category": category,
                "severity": severity,
                "score_adjustment": total_adj,
                "impact": impact_desc,
            })
        
        # Cap the total adjustment
        adjustment = max(-30, min(20, adjustment))
        new_score = max(0, min(100, current_score + adjustment))
        
        return {
            "original_score": current_score,
            "adjusted_score": new_score,
            "total_adjustment": adjustment,
            "insight_impacts": insight_impacts,
            "summary": f"Primary insights resulted in a {abs(adjustment):.1f} point "
                      f"{'increase' if adjustment > 0 else 'decrease'} in credit score "
                      f"(from {current_score:.1f} to {new_score:.1f})"
        }


# Global research agent instance
research_agent = ResearchAgent()
