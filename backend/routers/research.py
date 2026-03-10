"""
IntelCredit - Research Agent Routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel

from services.research_agent import research_agent
from models.database import db

router = APIRouter(prefix="/api/research", tags=["Research Agent"])


class ResearchRequest(BaseModel):
    company_name: str
    promoters: List[str] = []
    sector: Optional[str] = "manufacturing"
    cin: Optional[str] = None


class PrimaryInsightInput(BaseModel):
    company_id: str
    category: str = "site_visit"  # site_visit, management_interview, other
    observation: str
    severity: str = "info"  # info, warning, critical, positive
    impact_area: str = "general"  # operations, finance, management, compliance
    recorded_by: Optional[str] = None


@router.post("/secondary")
async def conduct_secondary_research(request: ResearchRequest):
    """
    Conduct automated secondary research on a company.
    Searches news, litigation, regulatory filings, sector analysis, and management background.
    """
    research = await research_agent.conduct_research(
        company_name=request.company_name,
        promoters=request.promoters,
        sector=request.sector,
        cin=request.cin,
    )
    
    return {
        "status": "success",
        "research": research,
    }


@router.post("/insights")
async def add_primary_insight(insight: PrimaryInsightInput):
    """
    Add a primary due diligence insight (site visit observation, management interview notes, etc.).
    These qualitative notes are integrated into the final risk score.
    """
    db.add_primary_insight(insight.company_id, insight.model_dump())
    
    return {
        "status": "success",
        "message": f"Insight added for company {insight.company_id}",
        "insight": insight.model_dump(),
    }


@router.get("/insights/{company_id}")
async def get_insights(company_id: str):
    """Get all primary insights for a company."""
    insights = db.get_insights(company_id)
    return {
        "status": "success",
        "company_id": company_id,
        "total_insights": len(insights),
        "insights": insights,
    }


@router.post("/insights/adjust-score")
async def adjust_score_with_insights(
    company_id: str,
    current_score: float,
):
    """
    Adjust the credit score based on accumulated primary insights.
    Returns the adjusted score with explanation of each insight's impact.
    """
    insights = db.get_insights(company_id)
    
    if not insights:
        return {
            "status": "success",
            "message": "No insights to process",
            "original_score": current_score,
            "adjusted_score": current_score,
        }
    
    result = research_agent.integrate_primary_insights(insights, current_score)
    
    return {
        "status": "success",
        **result,
    }
