"""
IntelCredit - Pydantic Schemas & Data Models
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class DocumentType(str, Enum):
    ANNUAL_REPORT = "annual_report"
    FINANCIAL_STATEMENT = "financial_statement"
    GST_RETURN = "gst_return"
    ITR = "itr"
    BANK_STATEMENT = "bank_statement"
    BOARD_MINUTES = "board_minutes"
    RATING_REPORT = "rating_report"
    SANCTION_LETTER = "sanction_letter"
    LEGAL_NOTICE = "legal_notice"
    MCA_FILING = "mca_filing"
    OTHER = "other"


class LoanDecision(str, Enum):
    APPROVED = "approved"
    CONDITIONAL = "conditional"
    REJECTED = "rejected"


# ===== Company Models =====
class CompanyProfile(BaseModel):
    company_name: str
    cin: Optional[str] = None  # Corporate Identity Number
    pan: Optional[str] = None
    gstin: Optional[str] = None
    industry: Optional[str] = None
    sub_sector: Optional[str] = None
    incorporation_date: Optional[str] = None
    registered_address: Optional[str] = None
    promoters: Optional[List[str]] = []
    authorized_capital: Optional[float] = None
    paid_up_capital: Optional[float] = None


class LoanRequest(BaseModel):
    company: CompanyProfile
    requested_amount: float = Field(..., description="Loan amount requested in INR lakhs")
    loan_purpose: str
    tenure_months: int = 60
    collateral_description: Optional[str] = None
    collateral_value: Optional[float] = None


# ===== Financial Data Models =====
class FinancialData(BaseModel):
    year: str
    revenue: Optional[float] = None
    ebitda: Optional[float] = None
    pat: Optional[float] = None  # Profit After Tax
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    net_worth: Optional[float] = None
    current_assets: Optional[float] = None
    current_liabilities: Optional[float] = None
    total_debt: Optional[float] = None
    cash_and_equivalents: Optional[float] = None
    inventory: Optional[float] = None
    receivables: Optional[float] = None
    payables: Optional[float] = None


class FinancialRatios(BaseModel):
    year: str
    current_ratio: Optional[float] = None
    debt_equity_ratio: Optional[float] = None
    interest_coverage_ratio: Optional[float] = None
    dscr: Optional[float] = None  # Debt Service Coverage Ratio
    roe: Optional[float] = None
    roa: Optional[float] = None
    ebitda_margin: Optional[float] = None
    pat_margin: Optional[float] = None
    asset_turnover: Optional[float] = None
    working_capital_days: Optional[int] = None
    debtor_days: Optional[int] = None
    creditor_days: Optional[int] = None
    inventory_days: Optional[int] = None


class GSTData(BaseModel):
    period: str
    gstr1_revenue: Optional[float] = None
    gstr3b_revenue: Optional[float] = None
    gstr2a_purchases: Optional[float] = None
    itc_claimed: Optional[float] = None
    tax_paid: Optional[float] = None
    mismatch_flag: bool = False
    mismatch_amount: Optional[float] = None


class BankStatementData(BaseModel):
    month: str
    opening_balance: Optional[float] = None
    total_credits: Optional[float] = None
    total_debits: Optional[float] = None
    closing_balance: Optional[float] = None
    avg_balance: Optional[float] = None
    emi_outflows: Optional[float] = None
    cheque_bounces: int = 0
    inward_returns: int = 0


# ===== Research Models =====
class NewsArticle(BaseModel):
    title: str
    source: str
    date: Optional[str] = None
    summary: str
    sentiment: str = "neutral"  # positive, negative, neutral
    relevance_score: float = 0.0
    url: Optional[str] = None


class LitigationRecord(BaseModel):
    case_number: Optional[str] = None
    court: Optional[str] = None
    parties: Optional[str] = None
    subject: Optional[str] = None
    status: str = "pending"  # pending, disposed, settled
    amount_involved: Optional[float] = None
    risk_impact: str = "low"


class ResearchReport(BaseModel):
    company_name: str
    news_articles: List[NewsArticle] = []
    litigation_records: List[LitigationRecord] = []
    regulatory_flags: List[str] = []
    sector_outlook: str = "stable"
    management_reputation: str = "good"
    overall_sentiment: str = "neutral"
    research_summary: str = ""


# ===== Primary Insights =====
class PrimaryInsight(BaseModel):
    category: str  # site_visit, management_interview, other
    observation: str
    severity: str = "info"  # info, warning, critical
    impact_area: str = "general"  # operations, finance, management, compliance
    recorded_by: Optional[str] = None
    recorded_at: Optional[str] = None


# ===== Scoring Models =====
class CreditScoreBreakdown(BaseModel):
    character_score: float = Field(..., ge=0, le=100)
    capacity_score: float = Field(..., ge=0, le=100)
    capital_score: float = Field(..., ge=0, le=100)
    collateral_score: float = Field(..., ge=0, le=100)
    conditions_score: float = Field(..., ge=0, le=100)
    character_factors: List[str] = []
    capacity_factors: List[str] = []
    capital_factors: List[str] = []
    collateral_factors: List[str] = []
    conditions_factors: List[str] = []
    weighted_score: float = 0.0
    risk_level: RiskLevel = RiskLevel.MODERATE


class CreditDecision(BaseModel):
    decision: LoanDecision
    approved_amount: Optional[float] = None
    interest_rate: Optional[float] = None
    risk_premium: Optional[float] = None
    tenure_months: Optional[int] = None
    conditions: List[str] = []
    rejection_reasons: List[str] = []
    explanation: str = ""
    score_breakdown: Optional[CreditScoreBreakdown] = None
    confidence: float = 0.0


# ===== CAM Models =====
class CAMReport(BaseModel):
    report_id: str
    generated_at: str
    company: CompanyProfile
    loan_request: LoanRequest
    financial_summary: List[FinancialData] = []
    ratio_analysis: List[FinancialRatios] = []
    gst_analysis: Optional[Dict[str, Any]] = None
    banking_analysis: Optional[Dict[str, Any]] = None
    research_report: Optional[ResearchReport] = None
    primary_insights: List[PrimaryInsight] = []
    credit_decision: Optional[CreditDecision] = None
    executive_summary: str = ""
    risk_mitigants: List[str] = []
    recommendation: str = ""


# ===== API Response Models =====
class UploadResponse(BaseModel):
    filename: str
    document_type: DocumentType
    extracted_data: Dict[str, Any]
    status: str = "success"
    message: str = ""


class AnalysisResponse(BaseModel):
    status: str
    company_name: str
    analysis_id: str
    financial_data: List[FinancialData] = []
    ratios: List[FinancialRatios] = []
    anomalies: List[str] = []
    flags: List[str] = []


class FullAppraisalRequest(BaseModel):
    company: CompanyProfile
    loan_request: LoanRequest
    financial_data: List[FinancialData] = []
    gst_data: List[GSTData] = []
    bank_data: List[BankStatementData] = []
    primary_insights: List[PrimaryInsight] = []
    additional_notes: Optional[str] = None
