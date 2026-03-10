import { useState } from 'react';
import { useApp } from '../context/AppContext';
import { Shield, Play } from 'lucide-react';
import api from '../services/api';

const FIVE_CS = [
  { name: 'Character', key: 'character', color: '#1a237e', weight: '20%' },
  { name: 'Capacity', key: 'capacity', color: '#3949ab', weight: '25%' },
  { name: 'Capital', key: 'capital', color: '#5c6bc0', weight: '20%' },
  { name: 'Collateral', key: 'collateral', color: '#7986cb', weight: '15%' },
  { name: 'Conditions', key: 'conditions', color: '#9fa8da', weight: '20%' },
];

export default function CreditScoring() {
  const { state, dispatch, showLoading, hideLoading, toast } = useApp();


  const buildPayload = () => {
    const c = state.company;
    return {
      company: {
        company_name: c.company_name || 'Company',
        cin: c.cin || '',
        pan: c.pan || '',
        gstin: c.gstin || '',
        industry: c.industry || 'Manufacturing',
        sub_sector: c.sector || '',
        incorporation_date: c.incorporation_date || '',
        registered_address: c.registered_address || '',
        promoters: c.promoter_names ? c.promoter_names.split(',').map(s => s.trim()) : [],
      },
      loan_request: {
        requested_amount: (parseFloat(c.loan_amount) || 0) / 100000,
        loan_purpose: c.loan_purpose || 'Working Capital',
        tenure_months: (parseInt(c.loan_tenure) || 5) * 12,
        collateral_description: c.collateral_type || '',
        collateral_value: (parseFloat(c.collateral_value) || 0) / 100000,
      },
      financial_data: state.financialYears.map(y => ({
        year: y.year,
        revenue: parseFloat(y.revenue) || 0,
        ebitda: parseFloat(y.ebitda) || 0,
        pat: parseFloat(y.pat) || 0,
        total_assets: parseFloat(y.total_assets) || 0,
        total_liabilities: parseFloat(y.total_liabilities) || 0,
        net_worth: parseFloat(y.net_worth) || 0,
        current_assets: parseFloat(y.current_assets) || 0,
        current_liabilities: parseFloat(y.current_liabilities) || 0,
      })),
      gst_data: [],
      bank_data: [],
      primary_insights: state.insights.map(i => ({
        category: i.category === 'operations' ? 'site_visit' : i.category === 'management' ? 'management_interview' : i.category,
        observation: i.observation,
        severity: i.impact === 'positive' ? 'positive' : i.impact === 'negative' ? 'warning' : 'info',
        impact_area: i.category,
      })),
    };
  };

  const runScoring = async () => {
    const hasData = state.financialYears.length > 0;
    if (!hasData) {
      toast('Add financial data first on the Financial Analysis page', 'warning');
      return;
    }
    showLoading('Running credit scoring with your data...');
    try {
      const payload = buildPayload();
      const result = await api.generateCAM(payload);
      dispatch({ type: 'SET_SCORING', payload: result });
      dispatch({ type: 'SET_CAM', payload: result });
      toast('Credit scoring complete with your data!', 'success');
    } catch (e) {
      toast(e.message, 'error');
    } finally {
      hideLoading();
    }
  };

  const data = state.scoringResults;
  const report = data?.report || data || {};
  const scoreBd = report.score_breakdown || {};
  const scoring = report.credit_scoring || report.scoring || (scoreBd.weighted_score != null ? scoreBd : {});
  const decision = data?.decision || report.decision || scoring.decision || {};
  const fiveCsFromBackend = {
    character: { score: scoreBd.character_score },
    capacity: { score: scoreBd.capacity_score },
    capital: { score: scoreBd.capital_score },
    collateral: { score: scoreBd.collateral_score },
    conditions: { score: scoreBd.conditions_score },
  };
  const breakdown = scoring.breakdown || scoring.five_cs || (scoreBd.character_score != null ? fiveCsFromBackend : {});
  const overallScore = scoring.overall_score || scoring.score || scoring.weighted_score || 0;
  const risk = scoring.risk_category || scoring.risk_level || 'moderate';
  const verdict = decision.verdict || decision.recommendation || decision.decision || '';
  const circumference = 2 * Math.PI * 85; // ~534

  const scoreColor = overallScore >= 75 ? '#28a745' : overallScore >= 55 ? '#ff9800' : '#dc3545';
  const offset = circumference - (overallScore / 100) * circumference;

  const decisionClass = verdict.toLowerCase().includes('approve') ? 'approved'
    : verdict.toLowerCase().includes('reject') ? 'rejected' : 'conditional';

  return (
    <>
      <p className="section-desc">Explainable ML scoring engine based on the Five Cs of Credit (Character, Capacity, Capital, Collateral, Conditions).</p>

      {/* Run Button */}
      <div className="card" style={{ textAlign: 'center' }}>
        <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
          <button className="btn btn-primary btn-lg" onClick={runScoring}>
            <Play size={18} /> Run Credit Scoring
          </button>
        </div>
        <p className="hint">
          {state.financialYears.length > 0
            ? `Using your ${state.financialYears.length} year(s) of financial data + ${state.insights.length} insight(s)`
            : 'Add financial data on the Financial Analysis page first'}
        </p>
      </div>

      {data && (
        <>
          {/* Score Circle + Badges */}
          <div className="score-overview">
            <div className="main-score">
              <svg viewBox="0 0 200 200">
                <circle cx="100" cy="100" r="85" fill="none" stroke="#e9ecef" strokeWidth="12" />
                <circle cx="100" cy="100" r="85" fill="none"
                  stroke={scoreColor} strokeWidth="12" strokeLinecap="round"
                  strokeDasharray={circumference}
                  strokeDashoffset={offset}
                  style={{ transition: 'stroke-dashoffset 1.5s ease' }}
                />
              </svg>
              <div className="score-text">
                <span className="score-value">{overallScore.toFixed(1)}</span>
                <span className="score-label">/ 100</span>
              </div>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12, alignItems: 'center' }}>
              <div className={`risk-badge ${risk.toLowerCase().replace(' ', '_')}`}>{risk.toUpperCase()}</div>
              {verdict && <div className={`decision-badge ${decisionClass}`}>{verdict.toUpperCase()}</div>}
            </div>
          </div>

          {/* Five Cs Bars */}
          <div className="card">
            <h3><Shield size={18} /> Five Cs Breakdown</h3>
            {FIVE_CS.map(c => {
              const val = breakdown[c.key]?.score ?? breakdown[c.key] ?? 0;
              const color = val >= 75 ? '#28a745' : val >= 55 ? '#ff9800' : '#dc3545';
              return (
                <div className="c-score-row" key={c.key}>
                  <div className="c-score-name">{c.name} <span style={{ fontWeight: 400, fontSize: 11, color: '#999' }}>({c.weight})</span></div>
                  <div className="c-score-value" style={{ color }}>{typeof val === 'number' ? val.toFixed(1) : val}</div>
                  <div className="c-score-bar">
                    <div className="c-score-fill" style={{ width: `${val}%`, background: c.color }}>{val >= 30 ? val.toFixed(0) : ''}</div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Decision Details */}
          <div className="card">
            <h3>Decision Details</h3>
            {(decision.recommended_amount || decision.loan_amount || decision.approved_amount) && (
              <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(3, 1fr)', marginBottom: 24 }}>
                <div className="stat-card">
                  <div className="stat-info">
                    <h3>₹{((decision.recommended_amount || decision.loan_amount || decision.approved_amount || 0) / 1e7).toFixed(1)} Cr</h3>
                    <p>Recommended Amount</p>
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-info">
                    <h3>{decision.interest_rate || 'N/A'}%</h3>
                    <p>Interest Rate</p>
                  </div>
                </div>
                <div className="stat-card">
                  <div className="stat-info">
                    <h3>{decision.tenure || decision.tenure_months ? `${decision.tenure || Math.round((decision.tenure_months || 0) / 12)}` : 'N/A'} yrs</h3>
                    <p>Tenure</p>
                  </div>
                </div>
              </div>
            )}

            {(decision.explanation || decision.steps || decision.explanation_steps) && (
              <>
                <h4 style={{ marginBottom: 12, fontSize: 14, color: 'var(--text-secondary)' }}>Scoring Explanation</h4>
                {(Array.isArray(decision.explanation || decision.explanation_steps) ? (decision.explanation || decision.explanation_steps) : [decision.explanation || decision.explanation_steps]).filter(Boolean).map((s, i) => (
                  <div className="explanation-step" key={i}>{s}</div>
                ))}
              </>
            )}

            {decision.conditions && (
              <>
                <h4 style={{ margin: '20px 0 12px', fontSize: 14, color: 'var(--text-secondary)' }}>Conditions</h4>
                {(Array.isArray(decision.conditions) ? decision.conditions : [decision.conditions]).map((c, i) => (
                  <div className="explanation-step" style={{ borderLeftColor: 'var(--warning)' }} key={i}>{c}</div>
                ))}
              </>
            )}
          </div>
        </>
      )}
    </>
  );
}
