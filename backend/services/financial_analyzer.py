"""
IntelCredit - Financial Analyzer Service
Cross-leverages GST returns, bank statements, and financial data
to detect anomalies like circular trading, revenue inflation, etc.
"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import math


class FinancialAnalyzer:
    """
    Performs deep financial analysis including:
    - GST vs Bank Statement cross-verification
    - Circular trading detection
    - Revenue inflation checks
    - Financial ratio computation
    - Trend analysis
    - Anomaly flagging
    """
    
    def __init__(self):
        self.anomaly_thresholds = {
            "gst_mismatch_pct": 10.0,      # >10% mismatch between GSTR-1 and GSTR-3B
            "revenue_vs_banking_pct": 20.0,  # >20% gap between revenue and bank credits
            "circular_trading_ratio": 0.80,  # If top 5 debtors are also top 5 creditors
            "current_ratio_min": 1.0,
            "debt_equity_max": 3.0,
            "interest_coverage_min": 1.5,
            "dscr_min": 1.25,
            "cheque_bounce_max": 3,          # Per quarter
        }
    
    def compute_financial_ratios(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute key financial ratios from financial data."""
        ratios = {}
        factors = []
        
        revenue = financial_data.get("revenue", 0)
        ebitda = financial_data.get("ebitda", 0)
        pat = financial_data.get("pat", 0)
        total_assets = financial_data.get("total_assets", 0)
        total_liabilities = financial_data.get("total_liabilities", 0)
        net_worth = financial_data.get("net_worth", 0)
        current_assets = financial_data.get("current_assets", 0)
        current_liabilities = financial_data.get("current_liabilities", 0)
        total_debt = financial_data.get("total_debt", 0)
        interest_expense = financial_data.get("interest_expense", 0)
        depreciation = financial_data.get("depreciation", 0)
        debt_repayment = financial_data.get("debt_repayment", 0)
        receivables = financial_data.get("receivables", 0)
        payables = financial_data.get("payables", 0)
        inventory = financial_data.get("inventory", 0)
        cash = financial_data.get("cash_and_equivalents", 0)
        
        # Profitability Ratios
        if revenue > 0:
            ratios["ebitda_margin"] = round((ebitda / revenue) * 100, 2)
            ratios["pat_margin"] = round((pat / revenue) * 100, 2)
            ratios["asset_turnover"] = round(revenue / total_assets, 2) if total_assets > 0 else 0
            factors.append(f"EBITDA Margin: {ratios['ebitda_margin']}%")
            factors.append(f"PAT Margin: {ratios['pat_margin']}%")
        
        # Liquidity Ratios
        if current_liabilities > 0:
            ratios["current_ratio"] = round(current_assets / current_liabilities, 2)
            ratios["quick_ratio"] = round((current_assets - inventory) / current_liabilities, 2)
            factors.append(f"Current Ratio: {ratios['current_ratio']}")
        
        # Leverage Ratios
        if net_worth > 0:
            ratios["debt_equity_ratio"] = round(total_debt / net_worth, 2)
            ratios["roe"] = round((pat / net_worth) * 100, 2)
            factors.append(f"Debt/Equity: {ratios['debt_equity_ratio']}")
            factors.append(f"ROE: {ratios['roe']}%")
        
        if total_assets > 0:
            ratios["roa"] = round((pat / total_assets) * 100, 2)
            ratios["leverage_ratio"] = round(total_debt / total_assets, 2)
        
        # Coverage Ratios
        if interest_expense > 0:
            ratios["interest_coverage"] = round(ebitda / interest_expense, 2)
            factors.append(f"Interest Coverage: {ratios['interest_coverage']}x")
        
        # DSCR
        if (interest_expense + debt_repayment) > 0:
            cash_accruals = pat + depreciation
            ratios["dscr"] = round(cash_accruals / (interest_expense + debt_repayment), 2)
            factors.append(f"DSCR: {ratios['dscr']}x")
        
        # Working Capital Days
        if revenue > 0:
            daily_revenue = revenue / 365
            if receivables > 0:
                ratios["debtor_days"] = round(receivables / daily_revenue)
            if inventory > 0:
                ratios["inventory_days"] = round(inventory / daily_revenue)
            if payables > 0:
                cogs = revenue * 0.7  # Approximate
                ratios["creditor_days"] = round(payables / (cogs / 365))
            
            wc_days = ratios.get("debtor_days", 0) + ratios.get("inventory_days", 0) - ratios.get("creditor_days", 0)
            ratios["working_capital_cycle"] = wc_days
            factors.append(f"Working Capital Cycle: {wc_days} days")
        
        ratios["analysis_factors"] = factors
        return ratios
    
    def analyze_gst_data(self, gst_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze GST returns for mismatches and anomalies.
        Cross-checks GSTR-1 vs GSTR-3B, identifies circular trading patterns.
        """
        analysis = {
            "total_periods": len(gst_data),
            "mismatches": [],
            "anomalies": [],
            "gst_revenue_trend": [],
            "total_gstr1_revenue": 0,
            "total_gstr3b_revenue": 0,
            "avg_mismatch_pct": 0,
            "circular_trading_risk": "low",
            "flags": [],
        }
        
        total_mismatch = 0
        
        for period_data in gst_data:
            gstr1 = period_data.get("gstr1_revenue", 0)
            gstr3b = period_data.get("gstr3b_revenue", 0)
            gstr2a = period_data.get("gstr2a_purchases", 0)
            itc = period_data.get("itc_claimed", 0)
            period = period_data.get("period", "unknown")
            
            analysis["total_gstr1_revenue"] += gstr1
            analysis["total_gstr3b_revenue"] += gstr3b
            
            # GSTR-1 vs GSTR-3B mismatch
            if gstr1 > 0 and gstr3b > 0:
                mismatch_pct = abs(gstr1 - gstr3b) / gstr1 * 100
                total_mismatch += mismatch_pct
                
                if mismatch_pct > self.anomaly_thresholds["gst_mismatch_pct"]:
                    analysis["mismatches"].append({
                        "period": period,
                        "gstr1_revenue": gstr1,
                        "gstr3b_revenue": gstr3b,
                        "mismatch_pct": round(mismatch_pct, 2),
                        "severity": "high" if mismatch_pct > 20 else "medium",
                    })
                    analysis["flags"].append(
                        f"GSTR-1 vs GSTR-3B mismatch of {mismatch_pct:.1f}% in {period}"
                    )
            
            # ITC vs GSTR-2A check
            if gstr2a > 0 and itc > 0:
                itc_mismatch = (itc - gstr2a) / gstr2a * 100
                if itc_mismatch > 10:
                    analysis["anomalies"].append({
                        "type": "excess_itc_claim",
                        "period": period,
                        "itc_claimed": itc,
                        "gstr2a_eligible": gstr2a,
                        "excess_pct": round(itc_mismatch, 2),
                    })
                    analysis["flags"].append(
                        f"Excess ITC claim of {itc_mismatch:.1f}% over GSTR-2A in {period}"
                    )
            
            # Revenue trend
            analysis["gst_revenue_trend"].append({
                "period": period,
                "revenue": gstr1 if gstr1 > 0 else gstr3b,
            })
        
        # Average mismatch
        if len(gst_data) > 0:
            analysis["avg_mismatch_pct"] = round(total_mismatch / len(gst_data), 2)
        
        # Circular trading detection heuristic
        if len(gst_data) >= 6:
            revenues = [d.get("gstr1_revenue", 0) for d in gst_data]
            purchases = [d.get("gstr2a_purchases", 0) for d in gst_data]
            if revenues and purchases:
                avg_rev = sum(revenues) / len(revenues)
                avg_pur = sum(purchases) / len(purchases)
                if avg_rev > 0 and avg_pur / avg_rev > self.anomaly_thresholds["circular_trading_ratio"]:
                    analysis["circular_trading_risk"] = "high"
                    analysis["flags"].append(
                        "HIGH RISK: Purchase-to-revenue ratio suggests possible circular trading"
                    )
        
        return analysis
    
    def analyze_bank_statements(self, bank_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze bank statements for anomalies and patterns."""
        analysis = {
            "total_months": len(bank_data),
            "avg_monthly_credits": 0,
            "avg_monthly_debits": 0,
            "avg_balance": 0,
            "min_balance": float("inf"),
            "max_balance": 0,
            "total_cheque_bounces": 0,
            "total_inward_returns": 0,
            "emi_regularity": "regular",
            "anomalies": [],
            "flags": [],
            "monthly_trend": [],
        }
        
        total_credits = 0
        total_debits = 0
        total_balance = 0
        total_bounces = 0
        total_returns = 0
        
        for month_data in bank_data:
            credits = month_data.get("total_credits", 0)
            debits = month_data.get("total_debits", 0)
            avg_bal = month_data.get("avg_balance", 0)
            bounces = month_data.get("cheque_bounces", 0)
            returns = month_data.get("inward_returns", 0)
            month = month_data.get("month", "unknown")
            
            total_credits += credits
            total_debits += debits
            total_balance += avg_bal
            total_bounces += bounces
            total_returns += returns
            
            if avg_bal < analysis["min_balance"]:
                analysis["min_balance"] = avg_bal
            if avg_bal > analysis["max_balance"]:
                analysis["max_balance"] = avg_bal
            
            # Check for anomalies
            if bounces > 0:
                analysis["anomalies"].append({
                    "type": "cheque_bounce",
                    "month": month,
                    "count": bounces,
                })
            
            analysis["monthly_trend"].append({
                "month": month,
                "credits": credits,
                "debits": debits,
                "balance": avg_bal,
            })
        
        n = max(len(bank_data), 1)
        analysis["avg_monthly_credits"] = round(total_credits / n, 2)
        analysis["avg_monthly_debits"] = round(total_debits / n, 2)
        analysis["avg_balance"] = round(total_balance / n, 2)
        analysis["total_cheque_bounces"] = total_bounces
        analysis["total_inward_returns"] = total_returns
        
        if analysis["min_balance"] == float("inf"):
            analysis["min_balance"] = 0
        
        # Flag excessive bounces
        if total_bounces > self.anomaly_thresholds["cheque_bounce_max"]:
            analysis["flags"].append(
                f"WARNING: {total_bounces} cheque bounces detected in {n} months"
            )
        
        if total_returns > 2:
            analysis["flags"].append(
                f"WARNING: {total_returns} inward return(s) detected"
            )
        
        return analysis
    
    def cross_verify_revenue(
        self,
        gst_revenue: float,
        bank_credits: float,
        reported_revenue: float
    ) -> Dict[str, Any]:
        """
        Cross-verify revenue across GST returns, bank statements, and financial statements.
        Detects revenue inflation or circular trading.
        """
        verification = {
            "gst_revenue": gst_revenue,
            "bank_credits": bank_credits,
            "reported_revenue": reported_revenue,
            "discrepancies": [],
            "flags": [],
            "revenue_inflation_risk": "low",
        }
        
        # GST vs Reported Revenue
        if reported_revenue > 0 and gst_revenue > 0:
            diff_pct = ((reported_revenue - gst_revenue) / gst_revenue) * 100
            if abs(diff_pct) > 15:
                verification["discrepancies"].append({
                    "type": "gst_vs_reported",
                    "difference_pct": round(diff_pct, 2),
                    "severity": "high" if abs(diff_pct) > 30 else "medium",
                })
                verification["flags"].append(
                    f"Reported revenue differs from GST revenue by {abs(diff_pct):.1f}%"
                )
        
        # Bank Credits vs Reported Revenue
        if reported_revenue > 0 and bank_credits > 0:
            diff_pct = ((reported_revenue - bank_credits) / bank_credits) * 100
            if abs(diff_pct) > self.anomaly_thresholds["revenue_vs_banking_pct"]:
                verification["discrepancies"].append({
                    "type": "bank_vs_reported",
                    "difference_pct": round(diff_pct, 2),
                    "severity": "high" if abs(diff_pct) > 40 else "medium",
                })
                verification["flags"].append(
                    f"Banking credits differ from reported revenue by {abs(diff_pct):.1f}%"
                )
                if diff_pct > 30:
                    verification["revenue_inflation_risk"] = "high"
        
        # GST vs Bank Credits
        if gst_revenue > 0 and bank_credits > 0:
            diff_pct = ((gst_revenue - bank_credits) / bank_credits) * 100
            if abs(diff_pct) > 15:
                verification["discrepancies"].append({
                    "type": "gst_vs_bank",
                    "difference_pct": round(diff_pct, 2),
                    "severity": "medium",
                })
        
        if len(verification["discrepancies"]) >= 2:
            verification["revenue_inflation_risk"] = "high"
            verification["flags"].append(
                "ALERT: Multiple revenue discrepancies detected - possible revenue inflation"
            )
        
        return verification
    
    def compute_trend_analysis(self, multi_year_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze multi-year financial trends."""
        trends = {
            "revenue_trend": [],
            "profitability_trend": [],
            "leverage_trend": [],
            "overall_trajectory": "stable",
            "growth_rate": 0,
            "flags": [],
        }
        
        if len(multi_year_data) < 2:
            return trends
        
        revenues = [(d.get("year", ""), d.get("revenue", 0)) for d in multi_year_data if d.get("revenue")]
        pats = [(d.get("year", ""), d.get("pat", 0)) for d in multi_year_data if d.get("pat")]
        debt_ratios = [(d.get("year", ""), d.get("total_debt", 0) / max(d.get("net_worth", 1), 1)) for d in multi_year_data if d.get("total_debt")]
        
        # Revenue CAGR
        if len(revenues) >= 2:
            first_rev = revenues[0][1]
            last_rev = revenues[-1][1]
            years = len(revenues) - 1
            if first_rev > 0 and years > 0:
                cagr = (pow(last_rev / first_rev, 1 / years) - 1) * 100
                trends["growth_rate"] = round(cagr, 2)
                
                if cagr > 15:
                    trends["overall_trajectory"] = "strong_growth"
                elif cagr > 5:
                    trends["overall_trajectory"] = "moderate_growth"
                elif cagr > -5:
                    trends["overall_trajectory"] = "stable"
                elif cagr > -15:
                    trends["overall_trajectory"] = "declining"
                else:
                    trends["overall_trajectory"] = "sharp_decline"
                    trends["flags"].append("ALERT: Sharp revenue decline detected")
        
        # Check for consistent losses
        loss_years = sum(1 for _, p in pats if p < 0)
        if loss_years > 1:
            trends["flags"].append(f"WARNING: Losses in {loss_years} out of {len(pats)} years")
        
        # Increasing leverage check
        if len(debt_ratios) >= 2 and debt_ratios[-1][1] > debt_ratios[0][1] * 1.5:
            trends["flags"].append("WARNING: Significant increase in leverage over the period")
        
        trends["revenue_trend"] = [{"year": y, "revenue": r} for y, r in revenues]
        trends["profitability_trend"] = [{"year": y, "pat": p} for y, p in pats]
        trends["leverage_trend"] = [{"year": y, "debt_equity": round(d, 2)} for y, d in debt_ratios]
        
        return trends
    
    def generate_full_analysis(
        self,
        financial_data: List[Dict[str, Any]],
        gst_data: List[Dict[str, Any]],
        bank_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generate comprehensive financial analysis."""
        
        # Compute ratios for most recent year
        latest_financials = financial_data[-1] if financial_data else {}
        ratios = self.compute_financial_ratios(latest_financials)
        
        # GST analysis
        gst_analysis = self.analyze_gst_data(gst_data)
        
        # Bank statement analysis
        bank_analysis = self.analyze_bank_statements(bank_data)
        
        # Cross-verification
        gst_revenue = gst_analysis.get("total_gstr1_revenue", 0) or gst_analysis.get("total_gstr3b_revenue", 0)
        bank_credits = bank_analysis.get("avg_monthly_credits", 0) * 12
        reported_revenue = latest_financials.get("revenue", 0)
        
        cross_verification = self.cross_verify_revenue(gst_revenue, bank_credits, reported_revenue)
        
        # Trend analysis
        trend_analysis = self.compute_trend_analysis(financial_data)
        
        # Consolidate all flags
        all_flags = []
        all_flags.extend(gst_analysis.get("flags", []))
        all_flags.extend(bank_analysis.get("flags", []))
        all_flags.extend(cross_verification.get("flags", []))
        all_flags.extend(trend_analysis.get("flags", []))
        
        # Check ratio thresholds
        if ratios.get("current_ratio", 2) < self.anomaly_thresholds["current_ratio_min"]:
            all_flags.append(f"WARNING: Current ratio ({ratios['current_ratio']}) below minimum threshold")
        if ratios.get("debt_equity_ratio", 0) > self.anomaly_thresholds["debt_equity_max"]:
            all_flags.append(f"WARNING: Debt/Equity ({ratios['debt_equity_ratio']}) above maximum threshold")
        if ratios.get("interest_coverage", 5) < self.anomaly_thresholds["interest_coverage_min"]:
            all_flags.append(f"WARNING: Interest Coverage ({ratios['interest_coverage']}x) below minimum")
        if ratios.get("dscr", 2) < self.anomaly_thresholds["dscr_min"]:
            all_flags.append(f"WARNING: DSCR ({ratios['dscr']}x) below minimum threshold")
        
        return {
            "financial_ratios": ratios,
            "gst_analysis": gst_analysis,
            "bank_analysis": bank_analysis,
            "cross_verification": cross_verification,
            "trend_analysis": trend_analysis,
            "all_flags": all_flags,
            "overall_financial_health": self._assess_health(ratios, all_flags),
        }
    
    def _assess_health(self, ratios: Dict[str, Any], flags: List[str]) -> str:
        """Assess overall financial health."""
        score = 100
        
        # Deductions based on ratios
        if ratios.get("current_ratio", 2) < 1.0:
            score -= 20
        elif ratios.get("current_ratio", 2) < 1.33:
            score -= 10
        
        if ratios.get("debt_equity_ratio", 0) > 3:
            score -= 25
        elif ratios.get("debt_equity_ratio", 0) > 2:
            score -= 15
        
        if ratios.get("interest_coverage", 5) < 1.5:
            score -= 20
        
        if ratios.get("pat_margin", 10) < 0:
            score -= 25
        elif ratios.get("pat_margin", 10) < 3:
            score -= 10
        
        # Deductions based on flags
        high_flags = sum(1 for f in flags if "HIGH" in f.upper() or "ALERT" in f.upper())
        warning_flags = sum(1 for f in flags if "WARNING" in f.upper())
        
        score -= high_flags * 15
        score -= warning_flags * 5
        
        score = max(0, min(100, score))
        
        if score >= 75:
            return "strong"
        elif score >= 55:
            return "adequate"
        elif score >= 35:
            return "weak"
        else:
            return "critical"


# Global analyzer instance
financial_analyzer = FinancialAnalyzer()
