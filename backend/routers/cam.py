"""
IntelCredit - CAM Generation & Full Appraisal Routes
This is the main orchestration endpoint that ties everything together.
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

from services.financial_analyzer import financial_analyzer
from services.research_agent import research_agent
from services.scoring_engine import scoring_engine
from services.cam_generator import cam_generator
from models.database import db

router = APIRouter(prefix="/api/cam", tags=["CAM Generator"])


class CompanyInput(BaseModel):
    company_name: str
    cin: Optional[str] = None
    pan: Optional[str] = None
    gstin: Optional[str] = None
    industry: Optional[str] = "Manufacturing"
    sub_sector: Optional[str] = None
    incorporation_date: Optional[str] = None
    registered_address: Optional[str] = None
    promoters: List[str] = []
    authorized_capital: Optional[float] = None
    paid_up_capital: Optional[float] = None


class LoanRequestInput(BaseModel):
    requested_amount: float  # In Lakhs
    loan_purpose: str = "Working Capital"
    tenure_months: int = 60
    collateral_description: Optional[str] = "Hypothecation of plant and machinery"
    collateral_value: Optional[float] = 0


class FinancialYearData(BaseModel):
    year: str = "FY2025"
    revenue: float = 0
    ebitda: float = 0
    pat: float = 0
    total_assets: float = 0
    total_liabilities: float = 0
    net_worth: float = 0
    current_assets: float = 0
    current_liabilities: float = 0
    total_debt: float = 0
    cash_and_equivalents: float = 0
    interest_expense: float = 0
    depreciation: float = 0
    debt_repayment: float = 0
    receivables: float = 0
    payables: float = 0
    inventory: float = 0


class GSTInput(BaseModel):
    period: str
    gstr1_revenue: float = 0
    gstr3b_revenue: float = 0
    gstr2a_purchases: float = 0
    itc_claimed: float = 0


class BankInput(BaseModel):
    month: str
    total_credits: float = 0
    total_debits: float = 0
    avg_balance: float = 0
    cheque_bounces: int = 0
    inward_returns: int = 0


class InsightInput(BaseModel):
    category: str = "site_visit"
    observation: str = ""
    severity: str = "info"
    impact_area: str = "general"


class FullAppraisalRequest(BaseModel):
    company: CompanyInput
    loan_request: LoanRequestInput
    financial_data: List[FinancialYearData] = []
    gst_data: List[GSTInput] = []
    bank_data: List[BankInput] = []
    primary_insights: List[InsightInput] = []


@router.post("/generate")
async def generate_cam(request: FullAppraisalRequest):
    """
    🚀 MAIN ENDPOINT: Generate a complete Credit Appraisal Memo.
    
    This orchestrates the entire pipeline:
    1. Financial Analysis (ratios, GST cross-check, bank analysis)
    2. Secondary Research (news, litigation, regulatory, management)
    3. ML Credit Scoring (Five Cs assessment)
    4. Primary Insight Integration
    5. CAM Report Generation
    
    Returns complete CAM data + HTML report.
    """
    
    company = request.company.model_dump()
    loan = request.loan_request.model_dump()
    
    # Step 1: Financial Analysis
    financial_data = [d.model_dump() for d in request.financial_data]
    gst_data = [d.model_dump() for d in request.gst_data]
    bank_data = [d.model_dump() for d in request.bank_data]
    
    financial_analysis = financial_analyzer.generate_full_analysis(
        financial_data, gst_data, bank_data
    )
    
    # Step 2: Secondary Research
    research_data = await research_agent.conduct_research(
        company_name=company["company_name"],
        promoters=company.get("promoters", []),
        sector=company.get("industry"),
        cin=company.get("cin"),
    )
    
    # Step 3: ML Credit Scoring
    latest_financials = financial_data[-1] if financial_data else {}
    
    scoring_result = scoring_engine.run_full_scoring(
        financial_data=latest_financials,
        financial_ratios=financial_analysis.get("financial_ratios", {}),
        trend_analysis=financial_analysis.get("trend_analysis", {}),
        gst_analysis=financial_analysis.get("gst_analysis", {}),
        bank_analysis=financial_analysis.get("bank_analysis", {}),
        research_data=research_data,
        loan_amount=loan["requested_amount"],
        collateral_value=loan.get("collateral_value", 0),
        collateral_description=loan.get("collateral_description", ""),
    )
    
    # Step 4: Integrate Primary Insights
    primary_insights = [i.model_dump() for i in request.primary_insights]
    if primary_insights:
        weighted_score = scoring_result["score_breakdown"]["weighted_score"]
        insight_adjustment = research_agent.integrate_primary_insights(
            primary_insights, weighted_score
        )
        # Update the score and recalculate risk level
        adjusted_score = insight_adjustment["adjusted_score"]
        scoring_result["score_breakdown"]["weighted_score"] = adjusted_score
        if adjusted_score >= 75:
            scoring_result["score_breakdown"]["risk_level"] = "low"
        elif adjusted_score >= 50:
            scoring_result["score_breakdown"]["risk_level"] = "moderate"
        elif adjusted_score >= 25:
            scoring_result["score_breakdown"]["risk_level"] = "high"
        else:
            scoring_result["score_breakdown"]["risk_level"] = "very_high"
        scoring_result["insight_adjustment"] = insight_adjustment
        
        # Re-generate decision with adjusted score
        scoring_result["decision"] = scoring_engine.generate_decision(
            scoring_result["score_breakdown"],
            loan["requested_amount"],
            latest_financials,
        )
    
    # Step 5: Generate CAM Report
    cam_report = cam_generator.generate_cam(
        company=company,
        loan_request=loan,
        financial_analysis=financial_analysis,
        research_data=research_data,
        scoring_result=scoring_result,
        primary_insights=primary_insights,
    )
    
    # Store in database
    report_id = db.store_cam_report({
        "cam": cam_report,
        "company": company,
        "scoring": scoring_result,
    })
    
    return {
        "status": "success",
        "report_id": cam_report["report_id"],
        "db_id": report_id,
        "executive_summary": cam_report["executive_summary"],
        "score_breakdown": scoring_result["score_breakdown"],
        "decision": scoring_result["decision"],
        "financial_flags": financial_analysis.get("all_flags", []),
        "research_summary": research_data.get("research_summary", ""),
        "insight_adjustment": scoring_result.get("insight_adjustment"),
        "cam_data": cam_report,
    }


@router.post("/generate-html", response_class=HTMLResponse)
async def generate_cam_html(request: FullAppraisalRequest):
    """Generate CAM and return only the HTML report for rendering."""
    result = await generate_cam(request)
    return HTMLResponse(content=result["cam_data"]["html_report"])


@router.get("/report/{report_id}")
async def get_cam_report(report_id: str):
    """Retrieve a previously generated CAM report."""
    report = db.get_cam_report(report_id)
    if not report:
        raise HTTPException(404, "CAM report not found")
    return report


@router.get("/reports")
async def list_cam_reports():
    """List all generated CAM reports."""
    return {"reports": list(db.cam_reports.values())}
