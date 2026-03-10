"""
IntelCredit - Financial Analysis Routes
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, model_validator

from services.financial_analyzer import financial_analyzer
from models.database import db

router = APIRouter(prefix="/api/analysis", tags=["Financial Analysis"])


class FinancialDataInput(BaseModel):
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


class GSTDataInput(BaseModel):
    period: str
    gstr1_revenue: float = 0
    gstr3b_revenue: float = 0
    gstr2a_purchases: float = 0
    itc_claimed: float = 0


class BankDataInput(BaseModel):
    month: str
    total_credits: float = 0
    total_debits: float = 0
    avg_balance: float = 0
    cheque_bounces: int = 0
    inward_returns: int = 0


class FullAnalysisRequest(BaseModel):
    company_name: str = "Company"
    company_id: Optional[str] = None
    financial_data: List[FinancialDataInput] = []
    financial_years: Optional[List[FinancialDataInput]] = None
    gst_data: List[GSTDataInput] = []
    bank_data: List[BankDataInput] = []


@router.post("/ratios")
async def compute_ratios(data: FinancialDataInput):
    """Compute financial ratios from a single year's data."""
    ratios = financial_analyzer.compute_financial_ratios(data.model_dump())
    return {"status": "success", "ratios": ratios}


@router.post("/gst")
async def analyze_gst(gst_data: List[GSTDataInput]):
    """Analyze GST returns for anomalies and mismatches."""
    data = [d.model_dump() for d in gst_data]
    analysis = financial_analyzer.analyze_gst_data(data)
    return {"status": "success", "gst_analysis": analysis}


@router.post("/banking")
async def analyze_banking(bank_data: List[BankDataInput]):
    """Analyze bank statements for anomalies."""
    data = [d.model_dump() for d in bank_data]
    analysis = financial_analyzer.analyze_bank_statements(data)
    return {"status": "success", "bank_analysis": analysis}


@router.post("/cross-verify")
async def cross_verify(
    gst_revenue: float,
    bank_credits: float,
    reported_revenue: float,
):
    """Cross-verify revenue across GST, banking, and reported figures."""
    verification = financial_analyzer.cross_verify_revenue(
        gst_revenue, bank_credits, reported_revenue
    )
    return {"status": "success", "verification": verification}


@router.post("/full")
async def full_analysis(request: FullAnalysisRequest):
    """Run comprehensive financial analysis across all data sources."""
    # Accept either financial_data or financial_years from frontend
    fin_list = request.financial_years if request.financial_years else request.financial_data
    financial_data = [d.model_dump() for d in fin_list]
    gst_data = [d.model_dump() for d in request.gst_data]
    bank_data = [d.model_dump() for d in request.bank_data]
    
    analysis = financial_analyzer.generate_full_analysis(
        financial_data, gst_data, bank_data
    )
    
    # Store analysis
    company_name = request.company_name or request.company_id or "unknown_company"
    company_id = db.store_company({"company_name": company_name})
    analysis_id = db.store_analysis(company_id, analysis)
    
    # Return with aliases the frontend expects
    return {
        "status": "success",
        "company_id": company_id,
        "analysis_id": analysis_id,
        "ratios": analysis.get("financial_ratios", {}),
        "gst_analysis": analysis.get("gst_analysis", {}),
        "bank_analysis": analysis.get("bank_analysis", {}),
        "cross_verification": analysis.get("cross_verification", {}),
        "trend_analysis": analysis.get("trend_analysis", {}),
        "flags": analysis.get("all_flags", []),
        "overall_health": analysis.get("overall_financial_health", "unknown"),
        "analysis": analysis,
    }
