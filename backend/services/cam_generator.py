"""
IntelCredit - CAM (Credit Appraisal Memo) Generator Service
Produces professional, structured CAM reports in HTML/PDF format.
Covers the Five Cs of Credit with comprehensive analysis.
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid


class CAMGenerator:
    """
    Generates professional Credit Appraisal Memorandum (CAM) reports.
    Output includes:
    - Executive Summary
    - Company Overview
    - Financial Analysis (ratios, trends, cross-verification)
    - Five Cs Assessment
    - Research Findings
    - Primary Due Diligence Insights
    - Risk Mitigants
    - Recommendation & Decision
    """
    
    def generate_cam(
        self,
        company: Dict[str, Any],
        loan_request: Dict[str, Any],
        financial_analysis: Dict[str, Any],
        research_data: Dict[str, Any],
        scoring_result: Dict[str, Any],
        primary_insights: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate complete CAM report data structure."""
        
        report_id = f"CAM-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"
        
        score_breakdown = scoring_result.get("score_breakdown", {})
        decision = scoring_result.get("decision", {})
        
        cam = {
            "report_id": report_id,
            "generated_at": datetime.now().isoformat(),
            "generated_by": "IntelCredit AI Engine v1.0",
            
            # Section 1: Header
            "header": {
                "title": "CREDIT APPRAISAL MEMORANDUM",
                "subtitle": f"Comprehensive Credit Assessment for {company.get('company_name', 'N/A')}",
                "date": datetime.now().strftime("%d %B %Y"),
                "confidential": True,
            },
            
            # Section 2: Executive Summary
            "executive_summary": self._generate_executive_summary(
                company, loan_request, decision, score_breakdown
            ),
            
            # Section 3: Company Overview
            "company_overview": self._generate_company_overview(company),
            
            # Section 4: Loan Proposal
            "loan_proposal": self._generate_loan_proposal(loan_request, decision),
            
            # Section 5: Financial Analysis
            "financial_analysis": self._generate_financial_section(financial_analysis),
            
            # Section 6: Five Cs Assessment
            "five_cs_assessment": self._generate_five_cs_section(score_breakdown),
            
            # Section 7: Secondary Research
            "research_findings": self._generate_research_section(research_data),
            
            # Section 8: Primary Due Diligence
            "due_diligence": self._generate_due_diligence_section(primary_insights or []),
            
            # Section 9: Risk Assessment
            "risk_assessment": self._generate_risk_section(
                financial_analysis, research_data, score_breakdown
            ),
            
            # Section 10: Recommendation
            "recommendation": self._generate_recommendation(decision, score_breakdown),
            
            # Section 11: Terms & Conditions
            "terms_conditions": decision.get("conditions", []),
            
            # Section 12: Annexures
            "annexures": {
                "scoring_methodology": self._scoring_methodology_text(),
                "disclaimer": self._disclaimer_text(),
            }
        }
        
        # Generate HTML report
        cam["html_report"] = self._render_html(cam)
        
        return cam
    
    def _generate_executive_summary(
        self, company: Dict, loan_request: Dict, decision: Dict, scores: Dict
    ) -> str:
        """Generate executive summary paragraph."""
        company_name = company.get("company_name", "The Company")
        amount = loan_request.get("requested_amount", 0)
        purpose = loan_request.get("loan_purpose", "business expansion")
        verdict = decision.get("decision", "pending").upper()
        approved_amount = decision.get("approved_amount", 0)
        rate = decision.get("interest_rate", 0)
        weighted_score = scores.get("weighted_score", 0)
        risk_level = scores.get("risk_level", "moderate")
        
        if verdict == "APPROVED":
            summary = (
                f"{company_name} has applied for a credit facility of ₹{amount:.2f} Lakhs for {purpose}. "
                f"Based on comprehensive analysis of the Five Cs of Credit, secondary research, and "
                f"primary due diligence, the application has been APPROVED.\n\n"
                f"The IntelCredit AI Engine assigns a weighted credit score of {weighted_score:.1f}/100, "
                f"corresponding to a '{risk_level}' risk classification. "
                f"The recommended facility amount is ₹{approved_amount:.2f} Lakhs at an interest rate "
                f"of {rate:.2f}% p.a., subject to conditions outlined in this memo.\n\n"
                f"Key Strengths: Strong financial ratios, clean promoter background, and positive sector outlook. "
                f"Key Concerns: Moderate litigation exposure requiring monitoring."
            )
        elif verdict == "CONDITIONAL":
            summary = (
                f"{company_name} has applied for a credit facility of ₹{amount:.2f} Lakhs for {purpose}. "
                f"The application is CONDITIONALLY APPROVED with enhanced monitoring requirements.\n\n"
                f"Credit score: {weighted_score:.1f}/100 ('{risk_level}' risk). "
                f"Recommended facility: ₹{approved_amount:.2f} Lakhs at {rate:.2f}% p.a., "
                f"subject to additional covenants and enhanced security coverage.\n\n"
                f"The conditional approval reflects areas requiring close monitoring, "
                f"including financial leverage and/or market conditions."
            )
        else:
            reasons = "; ".join(decision.get("rejection_reasons", ["Score below threshold"]))
            summary = (
                f"{company_name} has applied for a credit facility of ₹{amount:.2f} Lakhs for {purpose}. "
                f"After comprehensive analysis, the application is REJECTED.\n\n"
                f"Credit score: {weighted_score:.1f}/100 ('{risk_level}' risk classification). "
                f"Primary rejection reasons: {reasons}.\n\n"
                f"The applicant may reapply after addressing the identified concerns."
            )
        
        return summary
    
    def _generate_company_overview(self, company: Dict) -> Dict[str, Any]:
        """Generate company overview section."""
        return {
            "company_name": company.get("company_name", "N/A"),
            "cin": company.get("cin", "N/A"),
            "pan": company.get("pan", "N/A"),
            "gstin": company.get("gstin", "N/A"),
            "industry": company.get("industry", "N/A"),
            "sub_sector": company.get("sub_sector", "N/A"),
            "incorporation_date": company.get("incorporation_date", "N/A"),
            "registered_address": company.get("registered_address", "N/A"),
            "promoters": company.get("promoters", []),
            "authorized_capital": company.get("authorized_capital", "N/A"),
            "paid_up_capital": company.get("paid_up_capital", "N/A"),
        }
    
    def _generate_loan_proposal(self, loan_request: Dict, decision: Dict) -> Dict[str, Any]:
        """Generate loan proposal section."""
        return {
            "requested_amount": loan_request.get("requested_amount", 0),
            "approved_amount": decision.get("approved_amount", 0),
            "loan_purpose": loan_request.get("loan_purpose", "N/A"),
            "requested_tenure": loan_request.get("tenure_months", 60),
            "approved_tenure": decision.get("tenure_months", 0),
            "collateral_offered": loan_request.get("collateral_description", "N/A"),
            "collateral_value": loan_request.get("collateral_value", 0),
            "interest_rate": decision.get("interest_rate", 0),
            "risk_premium": decision.get("risk_premium", 0),
        }
    
    def _generate_financial_section(self, analysis: Dict) -> Dict[str, Any]:
        """Generate financial analysis section."""
        return {
            "ratios": analysis.get("financial_ratios", {}),
            "gst_analysis_summary": {
                "total_gstr1_revenue": analysis.get("gst_analysis", {}).get("total_gstr1_revenue", 0),
                "total_gstr3b_revenue": analysis.get("gst_analysis", {}).get("total_gstr3b_revenue", 0),
                "mismatches_found": len(analysis.get("gst_analysis", {}).get("mismatches", [])),
                "circular_trading_risk": analysis.get("gst_analysis", {}).get("circular_trading_risk", "low"),
            },
            "bank_analysis_summary": {
                "avg_credits": analysis.get("bank_analysis", {}).get("avg_monthly_credits", 0),
                "avg_balance": analysis.get("bank_analysis", {}).get("avg_balance", 0),
                "cheque_bounces": analysis.get("bank_analysis", {}).get("total_cheque_bounces", 0),
            },
            "cross_verification": analysis.get("cross_verification", {}),
            "trend_analysis": analysis.get("trend_analysis", {}),
            "flags": analysis.get("all_flags", []),
            "overall_health": analysis.get("overall_financial_health", "adequate"),
        }
    
    def _generate_five_cs_section(self, scores: Dict) -> Dict[str, Any]:
        """Generate Five Cs assessment section."""
        return {
            "character": {
                "score": scores.get("character_score", 0),
                "weight": "20%",
                "factors": scores.get("character_factors", []),
                "summary": self._summarize_c("character", scores.get("character_score", 0)),
            },
            "capacity": {
                "score": scores.get("capacity_score", 0),
                "weight": "25%",
                "factors": scores.get("capacity_factors", []),
                "summary": self._summarize_c("capacity", scores.get("capacity_score", 0)),
            },
            "capital": {
                "score": scores.get("capital_score", 0),
                "weight": "20%",
                "factors": scores.get("capital_factors", []),
                "summary": self._summarize_c("capital", scores.get("capital_score", 0)),
            },
            "collateral": {
                "score": scores.get("collateral_score", 0),
                "weight": "15%",
                "factors": scores.get("collateral_factors", []),
                "summary": self._summarize_c("collateral", scores.get("collateral_score", 0)),
            },
            "conditions": {
                "score": scores.get("conditions_score", 0),
                "weight": "20%",
                "factors": scores.get("conditions_factors", []),
                "summary": self._summarize_c("conditions", scores.get("conditions_score", 0)),
            },
            "weighted_score": scores.get("weighted_score", 0),
            "risk_level": scores.get("risk_level", "moderate"),
        }
    
    def _summarize_c(self, c_name: str, score: float) -> str:
        """Generate summary text for a C score."""
        if score >= 75:
            return f"Strong {c_name} assessment. Score indicates low risk in this dimension."
        elif score >= 50:
            return f"Adequate {c_name} assessment. Some areas require monitoring."
        elif score >= 25:
            return f"Weak {c_name} assessment. Significant concerns identified."
        else:
            return f"Critical {c_name} assessment. Major red flags identified."
    
    def _generate_research_section(self, research: Dict) -> Dict[str, Any]:
        """Generate secondary research findings section."""
        return {
            "news_summary": {
                "total_articles": research.get("news_analysis", {}).get("articles_found", 0),
                "sentiment": research.get("overall_sentiment", "neutral"),
                "key_articles": research.get("news_analysis", {}).get("key_articles", [])[:5],
            },
            "litigation_summary": {
                "total_cases": research.get("litigation_check", {}).get("total_cases_found", 0),
                "active_cases": research.get("litigation_check", {}).get("active_cases", 0),
                "total_exposure": research.get("litigation_check", {}).get("total_exposure", 0),
                "cases": research.get("litigation_check", {}).get("cases", []),
            },
            "sector_outlook": research.get("sector_analysis", {}).get("outlook", "stable"),
            "management_assessment": {
                "wilful_defaulter": research.get("management_check", {}).get("wilful_defaulter_check", "clear"),
                "disqualification": research.get("management_check", {}).get("director_disqualification", False),
            },
            "regulatory_flags": research.get("regulatory_check", {}).get("flags", []),
            "overall_research_summary": research.get("research_summary", ""),
        }
    
    def _generate_due_diligence_section(self, insights: List[Dict]) -> Dict[str, Any]:
        """Generate primary due diligence section."""
        if not insights:
            return {
                "site_visits": [],
                "management_interviews": [],
                "other_observations": [],
                "summary": "No primary due diligence insights recorded.",
            }
        
        site_visits = [i for i in insights if i.get("category") == "site_visit"]
        interviews = [i for i in insights if i.get("category") == "management_interview"]
        others = [i for i in insights if i.get("category") not in ["site_visit", "management_interview"]]
        
        critical = [i for i in insights if i.get("severity") == "critical"]
        warnings = [i for i in insights if i.get("severity") == "warning"]
        
        summary = f"Total {len(insights)} primary observations recorded. "
        if critical:
            summary += f"{len(critical)} critical finding(s). "
        if warnings:
            summary += f"{len(warnings)} warning(s). "
        
        return {
            "site_visits": site_visits,
            "management_interviews": interviews,
            "other_observations": others,
            "critical_findings": critical,
            "warnings": warnings,
            "summary": summary,
        }
    
    def _generate_risk_section(
        self, financial_analysis: Dict, research: Dict, scores: Dict
    ) -> Dict[str, Any]:
        """Generate risk assessment section."""
        all_risks = []
        mitigants = []
        
        # Collect all flags
        for flag in financial_analysis.get("all_flags", []):
            severity = "high" if "ALERT" in flag or "HIGH" in flag else ("medium" if "WARNING" in flag else "low")
            all_risks.append({"description": flag, "severity": severity, "source": "financial_analysis"})
        
        for flag in research.get("risk_flags", []):
            severity = "high" if "CRITICAL" in flag else "medium"
            all_risks.append({"description": flag, "severity": severity, "source": "secondary_research"})
        
        # Risk mitigants
        if scores.get("character_score", 0) >= 60:
            mitigants.append("Clean promoter background and track record")
        if scores.get("collateral_score", 0) >= 60:
            mitigants.append("Adequate collateral coverage")
        if scores.get("capacity_score", 0) >= 60:
            mitigants.append("Demonstrated ability to service debt from cash flows")
        if scores.get("conditions_score", 0) >= 60:
            mitigants.append("Favorable industry conditions and outlook")
        
        for indicator in research.get("positive_indicators", []):
            mitigants.append(indicator)
        
        return {
            "total_risks": len(all_risks),
            "high_severity": sum(1 for r in all_risks if r["severity"] == "high"),
            "medium_severity": sum(1 for r in all_risks if r["severity"] == "medium"),
            "low_severity": sum(1 for r in all_risks if r["severity"] == "low"),
            "risk_details": all_risks,
            "mitigants": mitigants,
        }
    
    def _generate_recommendation(self, decision: Dict, scores: Dict) -> Dict[str, Any]:
        """Generate final recommendation section."""
        verdict = decision.get("decision", "rejected").upper()
        
        return {
            "verdict": verdict,
            "approved_amount": decision.get("approved_amount", 0),
            "interest_rate": decision.get("interest_rate", 0),
            "tenure_months": decision.get("tenure_months", 0),
            "risk_premium": decision.get("risk_premium", 0),
            "conditions": decision.get("conditions", []),
            "rejection_reasons": decision.get("rejection_reasons", []),
            "explanation_steps": decision.get("explanation_steps", []),
            "confidence": decision.get("confidence", 0),
            "weighted_score": scores.get("weighted_score", 0),
            "risk_level": scores.get("risk_level", "moderate"),
        }
    
    def _scoring_methodology_text(self) -> str:
        return (
            "The IntelCredit scoring model evaluates creditworthiness across Five Cs of Credit:\n"
            "1. Character (20%): Promoter integrity, compliance history, litigation, management quality\n"
            "2. Capacity (25%): Cash flow adequacy, debt service coverage, revenue trends\n"
            "3. Capital (20%): Net worth, leverage ratios, liquidity position\n"
            "4. Collateral (15%): Security coverage, asset quality, existing encumbrances\n"
            "5. Conditions (20%): Industry outlook, regulatory environment, economic conditions\n\n"
            "Each dimension is scored 0-100 based on quantitative metrics and qualitative factors. "
            "The weighted score determines the risk category and informs the lending decision.\n\n"
            "Risk Categories: Low (75-100), Moderate (50-74), High (25-49), Very High (0-24)"
        )
    
    def _disclaimer_text(self) -> str:
        return (
            "DISCLAIMER: This Credit Appraisal Memo has been generated by the IntelCredit AI Engine. "
            "While AI-assisted analysis provides comprehensive and data-driven insights, the final "
            "lending decision should be reviewed and approved by authorized credit officers. "
            "The AI recommendation serves as a decision-support tool and should not be the sole "
            "basis for credit approval. All data sources should be independently verified.\n\n"
            "This document is confidential and meant for internal use only."
        )
    
    def _render_html(self, cam: Dict[str, Any]) -> str:
        """Render the CAM report as a professional HTML document."""
        header = cam["header"]
        summary = cam["executive_summary"]
        company = cam["company_overview"]
        proposal = cam["loan_proposal"]
        financial = cam["financial_analysis"]
        five_cs = cam["five_cs_assessment"]
        research = cam["research_findings"]
        dd = cam["due_diligence"]
        risk = cam["risk_assessment"]
        rec = cam["recommendation"]
        terms = cam["terms_conditions"]
        
        verdict_color = "#28a745" if rec["verdict"] == "APPROVED" else ("#ff9800" if rec["verdict"] == "CONDITIONAL" else "#dc3545")
        
        # Build Five Cs table rows
        five_cs_rows = ""
        for c_name in ["character", "capacity", "capital", "collateral", "conditions"]:
            c_data = five_cs.get(c_name, {})
            score = c_data.get("score", 0)
            bar_color = "#28a745" if score >= 70 else ("#ff9800" if score >= 40 else "#dc3545")
            factors_html = "".join([f"<li>{f}</li>" for f in c_data.get("factors", [])])
            five_cs_rows += f"""
            <tr>
                <td><strong>{c_name.title()}</strong><br><small>{c_data.get('weight', '')}</small></td>
                <td>
                    <div style="display:flex;align-items:center;gap:10px;">
                        <div style="width:60px;font-weight:bold;color:{bar_color}">{score:.0f}/100</div>
                        <div style="flex:1;background:#e9ecef;border-radius:4px;height:20px;">
                            <div style="width:{score}%;height:100%;background:{bar_color};border-radius:4px;"></div>
                        </div>
                    </div>
                </td>
                <td><ul style="margin:0;padding-left:20px;font-size:12px;">{factors_html}</ul></td>
                <td><small>{c_data.get('summary', '')}</small></td>
            </tr>"""
        
        # Build risk rows
        risk_rows = ""
        for r in risk.get("risk_details", [])[:10]:
            sev_color = "#dc3545" if r["severity"] == "high" else ("#ff9800" if r["severity"] == "medium" else "#6c757d")
            risk_rows += f"""
            <tr>
                <td><span style="color:{sev_color};font-weight:bold;">{r['severity'].upper()}</span></td>
                <td>{r['description']}</td>
                <td>{r['source']}</td>
            </tr>"""
        
        # Build conditions list
        conditions_html = "".join([f"<li>{c}</li>" for c in terms])
        
        # Build explanation steps
        steps_html = "".join([f"<li>{s}</li>" for s in rec.get("explanation_steps", [])])
        
        # News articles
        news_html = ""
        for article in research.get("news_summary", {}).get("key_articles", [])[:5]:
            sent_color = "#28a745" if article.get("sentiment") == "positive" else ("#dc3545" if article.get("sentiment") == "negative" else "#6c757d")
            news_html += f"""
            <div style="border-left:3px solid {sent_color};padding:8px 12px;margin:8px 0;background:#fafafa;">
                <strong>{article.get('title', '')}</strong>
                <br><small>{article.get('source', '')} | {article.get('date', '')} | 
                <span style="color:{sent_color}">{article.get('sentiment', '').upper()}</span></small>
                <br><small>{article.get('summary', '')}</small>
            </div>"""
        
        # Litigation
        lit_html = ""
        for case in research.get("litigation_summary", {}).get("cases", [])[:5]:
            lit_html += f"""
            <tr>
                <td>{case.get('case_number', 'N/A')}</td>
                <td>{case.get('court', 'N/A')}</td>
                <td>{case.get('subject', 'N/A')}</td>
                <td>₹{case.get('amount_involved', 0)} Cr</td>
                <td>{case.get('status', 'N/A').upper()}</td>
            </tr>"""
        
        # Financial flags
        flags_html = "".join([f"<li style='color:#dc3545;'>{f}</li>" for f in financial.get("flags", [])[:10]])
        
        # Mitigants
        mitigants_html = "".join([f"<li style='color:#28a745;'>{m}</li>" for m in risk.get("mitigants", [])])
        
        # Extract nested dicts before f-string ({{}} in f-strings produces a set, not a dict)
        fin_ratios = financial.get('ratios', {})
        fin_gst = financial.get('gst_analysis_summary', {})
        fin_bank = financial.get('bank_analysis_summary', {})
        res_news = research.get('news_summary', {})
        res_mgmt = research.get('management_assessment', {})
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{header['title']} - {company.get('company_name', '')}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333; line-height: 1.6; background: #fff; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 40px; }}
        .header {{ text-align: center; border-bottom: 3px solid #1a237e; padding-bottom: 20px; margin-bottom: 30px; }}
        .header h1 {{ color: #1a237e; font-size: 24px; letter-spacing: 2px; }}
        .header h2 {{ color: #455a64; font-size: 16px; margin-top: 5px; }}
        .header .meta {{ margin-top: 10px; font-size: 12px; color: #78909c; }}
        .confidential {{ background: #ffebee; color: #c62828; padding: 4px 12px; display: inline-block; font-size: 11px; font-weight: bold; letter-spacing: 1px; border-radius: 3px; }}
        .section {{ margin: 30px 0; }}
        .section h3 {{ color: #1a237e; font-size: 18px; border-bottom: 2px solid #e8eaf6; padding-bottom: 8px; margin-bottom: 15px; }}
        .verdict-box {{ background: linear-gradient(135deg, {verdict_color}11, {verdict_color}22); border: 2px solid {verdict_color}; border-radius: 8px; padding: 20px; text-align: center; margin: 20px 0; }}
        .verdict-box .verdict {{ font-size: 28px; font-weight: bold; color: {verdict_color}; }}
        .verdict-box .score {{ font-size: 16px; color: #555; margin-top: 5px; }}
        .summary-box {{ background: #f5f5f5; padding: 20px; border-radius: 8px; border-left: 4px solid #1a237e; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th {{ background: #1a237e; color: white; padding: 10px 12px; text-align: left; font-size: 13px; }}
        td {{ padding: 10px 12px; border-bottom: 1px solid #e0e0e0; font-size: 13px; }}
        tr:nth-child(even) {{ background: #fafafa; }}
        .metric-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 15px 0; }}
        .metric-card {{ background: #f8f9fa; border: 1px solid #e0e0e0; border-radius: 8px; padding: 15px; text-align: center; }}
        .metric-card .value {{ font-size: 24px; font-weight: bold; color: #1a237e; }}
        .metric-card .label {{ font-size: 12px; color: #78909c; margin-top: 5px; }}
        .score-bar {{ display: flex; align-items: center; gap: 8px; margin: 5px 0; }}
        .score-bar .bar-bg {{ flex: 1; background: #e9ecef; border-radius: 4px; height: 24px; }}
        .score-bar .bar-fill {{ height: 100%; border-radius: 4px; transition: width 0.3s; }}
        ul {{ margin: 10px 0; padding-left: 25px; }}
        li {{ margin: 4px 0; font-size: 13px; }}
        .footer {{ margin-top: 40px; padding-top: 20px; border-top: 2px solid #e8eaf6; font-size: 11px; color: #78909c; }}
        @media print {{ .container {{ padding: 20px; }} }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <div class="confidential">CONFIDENTIAL</div>
            <h1>{header['title']}</h1>
            <h2>{header['subtitle']}</h2>
            <div class="meta">
                Report ID: {cam['report_id']} | Generated: {header['date']} | Engine: IntelCredit AI v1.0
            </div>
        </div>

        <!-- Verdict Box -->
        <div class="verdict-box">
            <div class="verdict">{rec['verdict']}</div>
            <div class="score">
                Credit Score: {rec['weighted_score']:.1f}/100 | Risk Level: {rec['risk_level'].upper()} | 
                Confidence: {rec['confidence']:.0f}%
            </div>
            {'<div style="margin-top:10px;font-size:14px;">Approved Amount: <strong>₹' + f"{rec['approved_amount']:.2f}" + ' Lakhs</strong> | Rate: <strong>' + f"{rec['interest_rate']:.2f}" + '% p.a.</strong> | Tenure: <strong>' + str(rec['tenure_months']) + ' months</strong></div>' if rec['verdict'] != 'REJECTED' else '<div style="margin-top:10px;font-size:14px;color:#c62828;">Application does not meet minimum credit criteria</div>'}
        </div>

        <!-- Executive Summary -->
        <div class="section">
            <h3>1. Executive Summary</h3>
            <div class="summary-box">
                <p>{summary.replace(chr(10), '<br>')}</p>
            </div>
        </div>

        <!-- Company Overview -->
        <div class="section">
            <h3>2. Company Overview</h3>
            <div class="metric-grid">
                <div class="metric-card"><div class="label">Company Name</div><div class="value" style="font-size:16px;">{company.get('company_name', 'N/A')}</div></div>
                <div class="metric-card"><div class="label">CIN</div><div class="value" style="font-size:14px;">{company.get('cin', 'N/A')}</div></div>
                <div class="metric-card"><div class="label">Industry</div><div class="value" style="font-size:14px;">{company.get('industry', 'N/A')}</div></div>
                <div class="metric-card"><div class="label">GSTIN</div><div class="value" style="font-size:12px;">{company.get('gstin', 'N/A')}</div></div>
                <div class="metric-card"><div class="label">PAN</div><div class="value" style="font-size:14px;">{company.get('pan', 'N/A')}</div></div>
                <div class="metric-card"><div class="label">Incorporated</div><div class="value" style="font-size:14px;">{company.get('incorporation_date', 'N/A')}</div></div>
            </div>
            <p><strong>Promoters:</strong> {', '.join(company.get('promoters', ['N/A']))}</p>
            <p><strong>Address:</strong> {company.get('registered_address', 'N/A')}</p>
        </div>

        <!-- Loan Proposal -->
        <div class="section">
            <h3>3. Loan Proposal & Recommendation</h3>
            <table>
                <tr><th>Parameter</th><th>Requested</th><th>Recommended</th></tr>
                <tr><td>Facility Amount</td><td>₹{proposal['requested_amount']:.2f} Lakhs</td><td>₹{proposal['approved_amount']:.2f} Lakhs</td></tr>
                <tr><td>Interest Rate</td><td>-</td><td>{proposal['interest_rate']:.2f}% p.a.</td></tr>
                <tr><td>Tenure</td><td>{proposal['requested_tenure']} months</td><td>{proposal['approved_tenure']} months</td></tr>
                <tr><td>Purpose</td><td colspan="2">{proposal['loan_purpose']}</td></tr>
                <tr><td>Collateral</td><td colspan="2">{proposal['collateral_offered']}</td></tr>
                <tr><td>Collateral Value</td><td colspan="2">₹{proposal['collateral_value']:.2f} Lakhs</td></tr>
                <tr><td>Risk Premium</td><td>-</td><td>{proposal['risk_premium']:.2f}%</td></tr>
            </table>
        </div>

        <!-- Financial Analysis -->
        <div class="section">
            <h3>4. Financial Analysis</h3>
            <div class="metric-grid">
                <div class="metric-card"><div class="label">EBITDA Margin</div><div class="value">{fin_ratios.get('ebitda_margin', 'N/A')}%</div></div>
                <div class="metric-card"><div class="label">Current Ratio</div><div class="value">{fin_ratios.get('current_ratio', 'N/A')}</div></div>
                <div class="metric-card"><div class="label">Debt/Equity</div><div class="value">{fin_ratios.get('debt_equity_ratio', 'N/A')}</div></div>
                <div class="metric-card"><div class="label">Interest Coverage</div><div class="value">{fin_ratios.get('interest_coverage', 'N/A')}x</div></div>
                <div class="metric-card"><div class="label">DSCR</div><div class="value">{fin_ratios.get('dscr', 'N/A')}x</div></div>
                <div class="metric-card"><div class="label">ROE</div><div class="value">{fin_ratios.get('roe', 'N/A')}%</div></div>
            </div>

            <h4 style="margin-top:20px;">GST Cross-Verification</h4>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>GSTR-1 Revenue</td><td>₹{fin_gst.get('total_gstr1_revenue', 0):.2f} Lakhs</td></tr>
                <tr><td>GSTR-3B Revenue</td><td>₹{fin_gst.get('total_gstr3b_revenue', 0):.2f} Lakhs</td></tr>
                <tr><td>Mismatches Found</td><td>{fin_gst.get('mismatches_found', 0)}</td></tr>
                <tr><td>Circular Trading Risk</td><td>{fin_gst.get('circular_trading_risk', 'N/A').upper()}</td></tr>
            </table>

            <h4 style="margin-top:20px;">Bank Statement Analysis</h4>
            <table>
                <tr><th>Metric</th><th>Value</th></tr>
                <tr><td>Avg Monthly Credits</td><td>₹{fin_bank.get('avg_credits', 0):.2f} Lakhs</td></tr>
                <tr><td>Avg Balance</td><td>₹{fin_bank.get('avg_balance', 0):.2f} Lakhs</td></tr>
                <tr><td>Cheque Bounces</td><td>{fin_bank.get('cheque_bounces', 0)}</td></tr>
            </table>

            {'<h4 style="margin-top:20px;color:#c62828;">⚠ Flags & Anomalies</h4><ul>' + flags_html + '</ul>' if flags_html else ''}
        </div>

        <!-- Five Cs Assessment -->
        <div class="section">
            <h3>5. Five Cs of Credit Assessment</h3>
            <table>
                <tr><th style="width:120px;">Dimension</th><th style="width:200px;">Score</th><th>Key Factors</th><th style="width:200px;">Assessment</th></tr>
                {five_cs_rows}
            </table>
            <div style="margin-top:15px;text-align:center;">
                <strong>Weighted Credit Score: <span style="font-size:24px;color:{verdict_color};">{five_cs['weighted_score']:.1f}</span>/100</strong>
                <br><span style="color:{verdict_color};font-weight:bold;">Risk Level: {five_cs['risk_level'].upper()}</span>
            </div>
        </div>

        <!-- Secondary Research -->
        <div class="section">
            <h3>6. Secondary Research Findings</h3>
            <h4>News Analysis</h4>
            <p>Sentiment: <strong>{res_news.get('sentiment', 'N/A').upper()}</strong> 
            ({res_news.get('total_articles', 0)} articles analyzed)</p>
            {news_html}

            <h4 style="margin-top:20px;">Litigation History</h4>
            <table>
                <tr><th>Case No.</th><th>Court</th><th>Subject</th><th>Exposure</th><th>Status</th></tr>
                {lit_html}
            </table>

            <h4 style="margin-top:20px;">Management Assessment</h4>
            <p>Wilful Defaulter Check: <strong>{res_mgmt.get('wilful_defaulter', 'N/A').upper()}</strong></p>
            <p>Director Disqualification: <strong>{'YES' if res_mgmt.get('disqualification') else 'NO'}</strong></p>
        </div>

        <!-- Due Diligence -->
        <div class="section">
            <h3>7. Primary Due Diligence</h3>
            <p>{dd.get('summary', 'No insights recorded.')}</p>
            {'<h4 style="color:#c62828;">Critical Findings</h4><ul>' + ''.join(['<li style="color:#c62828;">' + f.get('observation', '') + '</li>' for f in dd.get('critical_findings', [])]) + '</ul>' if dd.get('critical_findings') else ''}
            {'<h4>Warnings</h4><ul>' + ''.join(['<li style="color:#ff9800;">' + f.get('observation', '') + '</li>' for f in dd.get('warnings', [])]) + '</ul>' if dd.get('warnings') else ''}
        </div>

        <!-- Risk Assessment -->
        <div class="section">
            <h3>8. Risk Assessment & Mitigants</h3>
            <p><strong>Total Risks Identified:</strong> {risk['total_risks']} 
            (High: {risk['high_severity']}, Medium: {risk['medium_severity']}, Low: {risk['low_severity']})</p>
            
            <table>
                <tr><th style="width:80px;">Severity</th><th>Description</th><th style="width:150px;">Source</th></tr>
                {risk_rows}
            </table>

            <h4 style="margin-top:20px;color:#28a745;">Risk Mitigants</h4>
            <ul>{mitigants_html}</ul>
        </div>

        <!-- Decision Logic -->
        <div class="section">
            <h3>9. Decision Logic (Explainability)</h3>
            <div style="background:#f5f5f5;padding:20px;border-radius:8px;">
                <h4>AI Decision Walkthrough:</h4>
                <ol style="padding-left:20px;">
                    {steps_html}
                </ol>
            </div>
        </div>

        <!-- Terms & Conditions -->
        {'<div class="section"><h3>10. Terms & Conditions</h3><ol>' + conditions_html + '</ol></div>' if conditions_html else ''}

        <!-- Footer -->
        <div class="footer">
            <p><strong>Scoring Methodology:</strong></p>
            <p style="white-space:pre-line;">{cam['annexures']['scoring_methodology']}</p>
            <br>
            <p><strong>{cam['annexures']['disclaimer']}</strong></p>
            <br>
            <p style="text-align:center;">--- End of Credit Appraisal Memo ---</p>
        </div>
    </div>
</body>
</html>"""
        
        return html


# Global CAM generator instance
cam_generator = CAMGenerator()
