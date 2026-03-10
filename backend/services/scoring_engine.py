"""
IntelCredit - ML-Based Credit Scoring Engine
Transparent, explainable scoring model based on the Five Cs of Credit.
Uses weighted scoring with clear factor attribution.
"""
import math
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class CreditScoringEngine:
    """
    Explainable ML-based credit scoring engine.
    Evaluates companies on the Five Cs of Credit:
    1. Character - Promoter integrity, compliance history, management quality
    2. Capacity - Revenue, cash flow, debt service ability
    3. Capital - Net worth, leverage, capital adequacy
    4. Collateral - Security coverage, asset quality
    5. Conditions - Industry outlook, economic environment, regulatory landscape
    
    Each C is scored 0-100 and weighted to produce a final score.
    """
    
    def __init__(self):
        self.weights = {
            "character": 0.20,
            "capacity": 0.25,
            "capital": 0.20,
            "collateral": 0.15,
            "conditions": 0.20,
        }
        
        # Benchmark thresholds for Indian mid-size corporates
        self.benchmarks = {
            "current_ratio": {"excellent": 2.0, "good": 1.5, "acceptable": 1.2, "poor": 1.0},
            "debt_equity": {"excellent": 0.5, "good": 1.0, "acceptable": 2.0, "poor": 3.0},
            "interest_coverage": {"excellent": 5.0, "good": 3.0, "acceptable": 1.5, "poor": 1.0},
            "dscr": {"excellent": 2.5, "good": 1.75, "acceptable": 1.25, "poor": 1.0},
            "ebitda_margin": {"excellent": 20.0, "good": 12.0, "acceptable": 8.0, "poor": 3.0},
            "pat_margin": {"excellent": 12.0, "good": 7.0, "acceptable": 3.0, "poor": 0.0},
            "roe": {"excellent": 20.0, "good": 15.0, "acceptable": 10.0, "poor": 5.0},
            "revenue_growth": {"excellent": 20.0, "good": 10.0, "acceptable": 5.0, "poor": -5.0},
            "asset_turnover": {"excellent": 2.0, "good": 1.2, "acceptable": 0.8, "poor": 0.4},
        }
    
    def score_character(
        self,
        management_data: Dict[str, Any],
        litigation_data: Dict[str, Any],
        compliance_data: Dict[str, Any],
        news_sentiment: Dict[str, Any],
    ) -> Tuple[float, List[str]]:
        """
        Score Character (0-100): Assesses promoter/management integrity and reliability.
        """
        score = 75  # Start with base score
        factors = []
        
        # Wilful defaulter check (-50 points automatic)
        if management_data.get("wilful_defaulter_check") != "clear":
            score -= 50
            factors.append("CRITICAL: Wilful defaulter flag detected (-50)")
        else:
            factors.append("Wilful defaulter check: Clear (+0)")
        
        # Director disqualification check
        if management_data.get("director_disqualification"):
            score -= 30
            factors.append("Director disqualification found (-30)")
        
        # Litigation assessment
        active_cases = litigation_data.get("active_cases", 0)
        total_exposure = litigation_data.get("active_exposure", 0)
        
        if active_cases == 0:
            score += 10
            factors.append("No active litigation (+10)")
        elif active_cases <= 2 and total_exposure < 5:
            score += 0
            factors.append(f"{active_cases} active cases, exposure ₹{total_exposure} Cr (neutral)")
        elif active_cases <= 5:
            score -= 10
            factors.append(f"{active_cases} active cases, exposure ₹{total_exposure} Cr (-10)")
        else:
            score -= 20
            factors.append(f"High litigation: {active_cases} cases, exposure ₹{total_exposure} Cr (-20)")
        
        # Compliance track record
        roc_status = compliance_data.get("roc_compliance", "compliant")
        if roc_status == "compliant":
            score += 5
            factors.append("ROC compliance: Regular (+5)")
        else:
            score -= 10
            factors.append(f"ROC compliance: {roc_status} (-10)")
        
        gst_status = compliance_data.get("gst_compliance", "compliant")
        if gst_status != "compliant":
            score -= 5
            factors.append(f"GST compliance issues noted (-5)")
        
        # News sentiment
        sentiment = news_sentiment.get("sentiment_breakdown", {})
        total_articles = max(sum(sentiment.values()), 1)
        neg_ratio = sentiment.get("negative", 0) / total_articles
        
        if neg_ratio > 0.5:
            score -= 15
            factors.append(f"Predominantly negative news coverage ({neg_ratio*100:.0f}%) (-15)")
        elif neg_ratio > 0.3:
            score -= 5
            factors.append(f"Some negative news coverage ({neg_ratio*100:.0f}%) (-5)")
        elif neg_ratio < 0.15:
            score += 5
            factors.append("Positive news sentiment (+5)")
        
        # Management experience
        for detail in management_data.get("details", []):
            exp = detail.get("experience_years", 0)
            if exp > 20:
                score += 5
                factors.append(f"Experienced management (>{exp} years) (+5)")
                break
            elif exp > 10:
                score += 2
                factors.append(f"Adequate management experience ({exp} years) (+2)")
                break
        
        return max(0, min(100, score)), factors
    
    def score_capacity(
        self,
        financial_ratios: Dict[str, Any],
        trend_analysis: Dict[str, Any],
        gst_analysis: Dict[str, Any],
        bank_analysis: Dict[str, Any],
    ) -> Tuple[float, List[str]]:
        """
        Score Capacity (0-100): Assesses ability to repay from cash flows.
        """
        score = 50  # Start at midpoint
        factors = []
        
        # EBITDA Margin
        ebitda_margin = financial_ratios.get("ebitda_margin", 0)
        if ebitda_margin >= self.benchmarks["ebitda_margin"]["excellent"]:
            score += 15
            factors.append(f"Excellent EBITDA margin: {ebitda_margin}% (+15)")
        elif ebitda_margin >= self.benchmarks["ebitda_margin"]["good"]:
            score += 10
            factors.append(f"Good EBITDA margin: {ebitda_margin}% (+10)")
        elif ebitda_margin >= self.benchmarks["ebitda_margin"]["acceptable"]:
            score += 5
            factors.append(f"Acceptable EBITDA margin: {ebitda_margin}% (+5)")
        elif ebitda_margin >= self.benchmarks["ebitda_margin"]["poor"]:
            score -= 5
            factors.append(f"Low EBITDA margin: {ebitda_margin}% (-5)")
        else:
            score -= 15
            factors.append(f"Very low/negative EBITDA margin: {ebitda_margin}% (-15)")
        
        # Interest Coverage Ratio
        icr = financial_ratios.get("interest_coverage", 0)
        if icr >= self.benchmarks["interest_coverage"]["excellent"]:
            score += 15
            factors.append(f"Strong interest coverage: {icr}x (+15)")
        elif icr >= self.benchmarks["interest_coverage"]["good"]:
            score += 10
            factors.append(f"Good interest coverage: {icr}x (+10)")
        elif icr >= self.benchmarks["interest_coverage"]["acceptable"]:
            score += 5
            factors.append(f"Adequate interest coverage: {icr}x (+5)")
        else:
            score -= 15
            factors.append(f"Weak interest coverage: {icr}x (-15)")
        
        # DSCR
        dscr = financial_ratios.get("dscr", 0)
        if dscr >= self.benchmarks["dscr"]["excellent"]:
            score += 10
            factors.append(f"Strong DSCR: {dscr}x (+10)")
        elif dscr >= self.benchmarks["dscr"]["good"]:
            score += 5
            factors.append(f"Good DSCR: {dscr}x (+5)")
        elif dscr >= self.benchmarks["dscr"]["acceptable"]:
            score += 0
            factors.append(f"Adequate DSCR: {dscr}x (+0)")
        else:
            score -= 15
            factors.append(f"Weak DSCR: {dscr}x (-15)")
        
        # Revenue Growth Trend
        growth_rate = trend_analysis.get("growth_rate", 0)
        trajectory = trend_analysis.get("overall_trajectory", "stable")
        
        if trajectory in ["strong_growth"]:
            score += 10
            factors.append(f"Strong revenue growth: {growth_rate}% CAGR (+10)")
        elif trajectory == "moderate_growth":
            score += 5
            factors.append(f"Moderate revenue growth: {growth_rate}% CAGR (+5)")
        elif trajectory == "declining":
            score -= 10
            factors.append(f"Declining revenue: {growth_rate}% CAGR (-10)")
        elif trajectory == "sharp_decline":
            score -= 20
            factors.append(f"Sharp revenue decline: {growth_rate}% CAGR (-20)")
        
        # Cheque bounces from bank analysis
        bounces = bank_analysis.get("total_cheque_bounces", 0)
        if bounces == 0:
            score += 5
            factors.append("No cheque bounces (+5)")
        elif bounces <= 3:
            score -= 5
            factors.append(f"{bounces} cheque bounces detected (-5)")
        else:
            score -= 15
            factors.append(f"High cheque bounces: {bounces} (-15)")
        
        # GST mismatch flags
        gst_flags = gst_analysis.get("flags", [])
        if gst_flags:
            score -= min(len(gst_flags) * 3, 15)
            factors.append(f"{len(gst_flags)} GST anomalies flagged (-{min(len(gst_flags)*3, 15)})")
        
        return max(0, min(100, score)), factors
    
    def score_capital(
        self,
        financial_ratios: Dict[str, Any],
        financial_data: Dict[str, Any],
    ) -> Tuple[float, List[str]]:
        """
        Score Capital (0-100): Assesses financial cushion and leverage.
        """
        score = 50
        factors = []
        
        # Debt-to-Equity Ratio
        de_ratio = financial_ratios.get("debt_equity_ratio", 0)
        if de_ratio <= self.benchmarks["debt_equity"]["excellent"]:
            score += 20
            factors.append(f"Low leverage - D/E: {de_ratio} (+20)")
        elif de_ratio <= self.benchmarks["debt_equity"]["good"]:
            score += 10
            factors.append(f"Moderate leverage - D/E: {de_ratio} (+10)")
        elif de_ratio <= self.benchmarks["debt_equity"]["acceptable"]:
            score += 0
            factors.append(f"Acceptable leverage - D/E: {de_ratio} (+0)")
        elif de_ratio <= self.benchmarks["debt_equity"]["poor"]:
            score -= 15
            factors.append(f"High leverage - D/E: {de_ratio} (-15)")
        else:
            score -= 25
            factors.append(f"Very high leverage - D/E: {de_ratio} (-25)")
        
        # Net Worth
        net_worth = financial_data.get("net_worth", 0)
        if net_worth > 500:
            score += 15
            factors.append(f"Strong net worth: ₹{net_worth} Cr (+15)")
        elif net_worth > 100:
            score += 10
            factors.append(f"Adequate net worth: ₹{net_worth} Cr (+10)")
        elif net_worth > 25:
            score += 0
            factors.append(f"Moderate net worth: ₹{net_worth} Cr (+0)")
        elif net_worth > 0:
            score -= 10
            factors.append(f"Low net worth: ₹{net_worth} Cr (-10)")
        else:
            score -= 25
            factors.append(f"Negative net worth: ₹{net_worth} Cr (-25)")
        
        # Current Ratio (liquidity)
        current_ratio = financial_ratios.get("current_ratio", 0)
        if current_ratio >= self.benchmarks["current_ratio"]["excellent"]:
            score += 10
            factors.append(f"Strong liquidity - CR: {current_ratio} (+10)")
        elif current_ratio >= self.benchmarks["current_ratio"]["good"]:
            score += 5
            factors.append(f"Good liquidity - CR: {current_ratio} (+5)")
        elif current_ratio >= self.benchmarks["current_ratio"]["acceptable"]:
            score += 0
            factors.append(f"Adequate liquidity - CR: {current_ratio} (+0)")
        else:
            score -= 15
            factors.append(f"Weak liquidity - CR: {current_ratio} (-15)")
        
        # ROE
        roe = financial_ratios.get("roe", 0)
        if roe >= self.benchmarks["roe"]["excellent"]:
            score += 5
            factors.append(f"Excellent ROE: {roe}% (+5)")
        elif roe >= self.benchmarks["roe"]["good"]:
            score += 3
            factors.append(f"Good ROE: {roe}% (+3)")
        elif roe < 0:
            score -= 10
            factors.append(f"Negative ROE: {roe}% (-10)")
        
        return max(0, min(100, score)), factors
    
    def score_collateral(
        self,
        collateral_value: float,
        loan_amount: float,
        collateral_description: str,
        existing_charges: List[Dict[str, Any]],
    ) -> Tuple[float, List[str]]:
        """
        Score Collateral (0-100): Assesses security coverage.
        """
        score = 50
        factors = []
        
        # Collateral Coverage Ratio
        if loan_amount > 0 and collateral_value > 0:
            coverage = collateral_value / loan_amount
            
            if coverage >= 2.0:
                score += 25
                factors.append(f"Strong collateral coverage: {coverage:.1f}x (+25)")
            elif coverage >= 1.5:
                score += 15
                factors.append(f"Good collateral coverage: {coverage:.1f}x (+15)")
            elif coverage >= 1.0:
                score += 5
                factors.append(f"Adequate collateral coverage: {coverage:.1f}x (+5)")
            elif coverage >= 0.5:
                score -= 10
                factors.append(f"Weak collateral coverage: {coverage:.1f}x (-10)")
            else:
                score -= 25
                factors.append(f"Insufficient collateral: {coverage:.1f}x (-25)")
        else:
            score -= 15
            factors.append("Collateral value not specified (-15)")
        
        # Type of collateral
        collateral_lower = collateral_description.lower() if collateral_description else ""
        if "immovable" in collateral_lower or "property" in collateral_lower or "land" in collateral_lower:
            score += 10
            factors.append("Immovable property as collateral (+10)")
        elif "plant" in collateral_lower or "machinery" in collateral_lower or "equipment" in collateral_lower:
            score += 5
            factors.append("Plant & machinery as collateral (+5)")
        elif "inventory" in collateral_lower or "receivable" in collateral_lower:
            score += 0
            factors.append("Current assets as collateral (+0)")
        elif "personal guarantee" in collateral_lower:
            score += 3
            factors.append("Personal guarantee of promoters (+3)")
        
        # Existing charges
        active_charges = sum(1 for c in existing_charges if c.get("status") == "active")
        if active_charges > 3:
            score -= 10
            factors.append(f"Multiple existing charges ({active_charges}) on assets (-10)")
        elif active_charges > 1:
            score -= 5
            factors.append(f"{active_charges} existing charges on assets (-5)")
        
        return max(0, min(100, score)), factors
    
    def score_conditions(
        self,
        sector_analysis: Dict[str, Any],
        regulatory_data: Dict[str, Any],
        macro_conditions: Dict[str, Any] = None,
    ) -> Tuple[float, List[str]]:
        """
        Score Conditions (0-100): Assesses external environment.
        """
        score = 60
        factors = []
        
        # Sector outlook
        outlook = sector_analysis.get("outlook", "stable").lower()
        if outlook in ["strong", "positive"]:
            score += 15
            factors.append(f"Positive sector outlook (+15)")
        elif outlook == "stable":
            score += 5
            factors.append(f"Stable sector outlook (+5)")
        elif outlook in ["cautious", "neutral"]:
            score += 0
            factors.append(f"Cautious sector outlook (+0)")
        elif outlook in ["negative", "weak"]:
            score -= 15
            factors.append(f"Negative sector outlook (-15)")
        
        # Regulatory environment
        reg_flags = regulatory_data.get("flags", [])
        if not reg_flags:
            score += 5
            factors.append("Clean regulatory environment (+5)")
        else:
            score -= min(len(reg_flags) * 5, 15)
            factors.append(f"{len(reg_flags)} regulatory concerns (-{min(len(reg_flags)*5, 15)})")
        
        # Industry peer comparison
        peer_data = sector_analysis.get("peer_comparison", {})
        if peer_data:
            factors.append(f"Industry avg margin: {peer_data.get('industry_avg_margin', 'N/A')}%")
            factors.append(f"Industry avg D/E: {peer_data.get('industry_avg_de_ratio', 'N/A')}")
        
        # Sector-specific risks
        sector_risks = sector_analysis.get("key_risks", [])
        if len(sector_risks) > 3:
            score -= 5
            factors.append(f"Multiple sector-specific risks identified (-5)")
        
        # Growth forecast
        growth = sector_analysis.get("growth_forecast", "")
        if "decline" in growth.lower() or "negative" in growth.lower():
            score -= 10
            factors.append(f"Sector growth forecast negative (-10)")
        elif "high" in growth.lower() or ">15" in growth:
            score += 5
            factors.append(f"Strong sector growth forecast (+5)")
        
        return max(0, min(100, score)), factors
    
    def compute_final_score(
        self,
        character_result: Tuple[float, List[str]],
        capacity_result: Tuple[float, List[str]],
        capital_result: Tuple[float, List[str]],
        collateral_result: Tuple[float, List[str]],
        conditions_result: Tuple[float, List[str]],
    ) -> Dict[str, Any]:
        """
        Compute weighted final credit score with full explainability.
        """
        char_score, char_factors = character_result
        cap_score, cap_factors = capacity_result
        capital_score, capital_factors = capital_result
        coll_score, coll_factors = collateral_result
        cond_score, cond_factors = conditions_result
        
        # Weighted score
        weighted = (
            char_score * self.weights["character"] +
            cap_score * self.weights["capacity"] +
            capital_score * self.weights["capital"] +
            coll_score * self.weights["collateral"] +
            cond_score * self.weights["conditions"]
        )
        
        # Determine risk level
        if weighted >= 75:
            risk_level = "low"
        elif weighted >= 50:
            risk_level = "moderate"
        elif weighted >= 25:
            risk_level = "high"
        else:
            risk_level = "very_high"
        
        return {
            "character_score": round(char_score, 1),
            "capacity_score": round(cap_score, 1),
            "capital_score": round(capital_score, 1),
            "collateral_score": round(coll_score, 1),
            "conditions_score": round(cond_score, 1),
            "character_factors": char_factors,
            "capacity_factors": cap_factors,
            "capital_factors": capital_factors,
            "collateral_factors": coll_factors,
            "conditions_factors": cond_factors,
            "weighted_score": round(weighted, 1),
            "risk_level": risk_level,
            "weights_used": self.weights,
        }
    
    def generate_decision(
        self,
        score_breakdown: Dict[str, Any],
        loan_amount: float,
        company_financials: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate final loan decision with amount, rate, and conditions.
        Fully explainable decision logic.
        """
        weighted_score = score_breakdown["weighted_score"]
        risk_level = score_breakdown["risk_level"]
        
        decision = {
            "score": weighted_score,
            "risk_level": risk_level,
            "decision": "rejected",
            "approved_amount": 0,
            "interest_rate": None,
            "risk_premium": None,
            "tenure_months": None,
            "conditions": [],
            "rejection_reasons": [],
            "explanation_steps": [],
            "confidence": 0,
        }
        
        # Base rate (RBI repo rate + bank spread)
        base_rate = 8.50
        
        # Decision logic with explanation
        decision["explanation_steps"].append(
            f"Step 1: Weighted credit score computed as {weighted_score:.1f}/100"
        )
        decision["explanation_steps"].append(
            f"Step 2: Risk level determined as '{risk_level}' based on score thresholds"
        )
        
        # Automatic rejection triggers
        rejection_triggers = []
        
        if score_breakdown["character_score"] < 25:
            rejection_triggers.append(
                f"Character score critically low ({score_breakdown['character_score']:.1f}/100) - "
                "indicates integrity/compliance concerns"
            )
        
        if score_breakdown["capacity_score"] < 20:
            rejection_triggers.append(
                f"Capacity score critically low ({score_breakdown['capacity_score']:.1f}/100) - "
                "insufficient cash flow for debt service"
            )
        
        if weighted_score < 25:
            rejection_triggers.append(
                f"Overall weighted score ({weighted_score:.1f}) below minimum threshold of 25"
            )
        
        if rejection_triggers:
            decision["decision"] = "rejected"
            decision["rejection_reasons"] = rejection_triggers
            decision["explanation_steps"].append(
                f"Step 3: REJECTED - {len(rejection_triggers)} automatic rejection trigger(s) activated"
            )
            for i, reason in enumerate(rejection_triggers):
                decision["explanation_steps"].append(f"  Trigger {i+1}: {reason}")
            decision["confidence"] = min(95, 60 + (50 - weighted_score))
            return decision
        
        # Determine approved amount and rate
        net_worth = company_financials.get("net_worth", 0)
        ebitda = company_financials.get("ebitda", 0)
        
        if risk_level == "low":
            # Up to 100% of requested amount
            approved_pct = 1.0
            risk_premium = 1.50
            decision["conditions"] = [
                "Standard security package",
                "Annual review of facilities",
                "Submission of quarterly financials",
            ]
        elif risk_level == "moderate":
            # Up to 75% of requested amount
            approved_pct = 0.75
            risk_premium = 3.00
            decision["conditions"] = [
                "Enhanced security coverage (min 1.5x)",
                "Quarterly review of facilities",
                "Monthly submission of GST returns and bank statements",
                "Personal guarantee of promoter directors",
                "Minimum DSCR covenant of 1.25x",
            ]
        elif risk_level == "high":
            # Up to 50% or conditional approval
            approved_pct = 0.50
            risk_premium = 5.00
            decision["decision"] = "conditional"
            decision["conditions"] = [
                "Enhanced collateral coverage (min 2.0x)",
                "Monthly monitoring of account",
                "Escrow mechanism for cash flows",
                "Personal guarantee with net worth statement",
                "DSCR covenant of 1.50x",
                "No dividend distribution without bank consent",
                "Quarterly independent audit of utilizaton",
            ]
        else:
            decision["decision"] = "rejected"
            decision["rejection_reasons"].append(
                f"Risk score ({weighted_score:.1f}) too low for credit approval"
            )
            decision["confidence"] = 85
            return decision
        
        # Cap approved amount based on financials
        max_by_networth = net_worth * 2.5  # Max 2.5x net worth
        max_by_ebitda = ebitda * 4  # Max 4x EBITDA
        financial_cap = min(max_by_networth, max_by_ebitda) if max_by_networth > 0 else loan_amount
        
        approved_amount = min(loan_amount * approved_pct, financial_cap)
        approved_amount = max(0, round(approved_amount, 2))
        
        interest_rate = base_rate + risk_premium
        
        decision["decision"] = "approved" if risk_level in ["low", "moderate"] else "conditional"
        decision["approved_amount"] = approved_amount
        decision["interest_rate"] = interest_rate
        decision["risk_premium"] = risk_premium
        decision["tenure_months"] = 60 if risk_level == "low" else (48 if risk_level == "moderate" else 36)
        decision["confidence"] = min(95, 50 + weighted_score * 0.4)
        
        decision["explanation_steps"].append(
            f"Step 3: Decision = {decision['decision'].upper()}"
        )
        decision["explanation_steps"].append(
            f"Step 4: Approved amount = ₹{approved_amount:.2f} Lakhs "
            f"({approved_pct*100:.0f}% of requested ₹{loan_amount:.2f} Lakhs, "
            f"capped by financial metrics)"
        )
        decision["explanation_steps"].append(
            f"Step 5: Interest rate = {interest_rate:.2f}% "
            f"(Base rate {base_rate}% + Risk premium {risk_premium}%)"
        )
        decision["explanation_steps"].append(
            f"Step 6: Tenure = {decision['tenure_months']} months"
        )
        
        if decision["conditions"]:
            decision["explanation_steps"].append(
                f"Step 7: {len(decision['conditions'])} conditions attached to approval"
            )
        
        return decision
    
    def run_full_scoring(
        self,
        financial_data: Dict[str, Any],
        financial_ratios: Dict[str, Any],
        trend_analysis: Dict[str, Any],
        gst_analysis: Dict[str, Any],
        bank_analysis: Dict[str, Any],
        research_data: Dict[str, Any],
        loan_amount: float,
        collateral_value: float,
        collateral_description: str,
    ) -> Dict[str, Any]:
        """
        Run the complete scoring pipeline end-to-end.
        Returns full score breakdown and decision.
        """
        # Extract sub-data from research
        management_data = research_data.get("management_check", {})
        litigation_data = research_data.get("litigation_check", {})
        compliance_data = research_data.get("regulatory_check", {})
        news_data = research_data.get("news_analysis", {})
        sector_data = research_data.get("sector_analysis", {})
        
        existing_charges = compliance_data.get("charge_details", [])
        
        # Score each C
        character_result = self.score_character(
            management_data, litigation_data, compliance_data, news_data
        )
        capacity_result = self.score_capacity(
            financial_ratios, trend_analysis, gst_analysis, bank_analysis
        )
        capital_result = self.score_capital(financial_ratios, financial_data)
        collateral_result = self.score_collateral(
            collateral_value, loan_amount, collateral_description, existing_charges
        )
        conditions_result = self.score_conditions(sector_data, compliance_data)
        
        # Compute final score
        score_breakdown = self.compute_final_score(
            character_result, capacity_result, capital_result,
            collateral_result, conditions_result
        )
        
        # Generate decision
        decision = self.generate_decision(score_breakdown, loan_amount, financial_data)
        
        return {
            "score_breakdown": score_breakdown,
            "decision": decision,
            "generated_at": datetime.now().isoformat(),
        }


# Global scoring engine instance
scoring_engine = CreditScoringEngine()
