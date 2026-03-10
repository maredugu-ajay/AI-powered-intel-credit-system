import { useState, useCallback } from 'react';
import { useApp } from '../context/AppContext';
import { Plus, Database, Play, X } from 'lucide-react';
import api from '../services/api';

const FIELDS = [
  { key: 'revenue', label: 'Revenue (₹ Cr)' },
  { key: 'ebitda', label: 'EBITDA (₹ Cr)' },
  { key: 'pat', label: 'PAT (₹ Cr)' },
  { key: 'total_assets', label: 'Total Assets (₹ Cr)' },
  { key: 'total_liabilities', label: 'Total Liabilities (₹ Cr)' },
  { key: 'net_worth', label: 'Net Worth (₹ Cr)' },
  { key: 'current_assets', label: 'Current Assets (₹ Cr)' },
  { key: 'current_liabilities', label: 'Current Liabilities (₹ Cr)' },
];

const BENCHMARKS = {
  debt_to_equity: { target: 1.5, label: '< 1.5', dir: 'lower' },
  current_ratio: { target: 1.5, label: '> 1.5', dir: 'higher' },
  interest_coverage: { target: 2.5, label: '> 2.5', dir: 'higher' },
  ebitda_margin: { target: 15, label: '> 15%', dir: 'higher' },
  pat_margin: { target: 8, label: '> 8%', dir: 'higher' },
  roe: { target: 15, label: '> 15%', dir: 'higher' },
  roa: { target: 5, label: '> 5%', dir: 'higher' },
  dscr: { target: 1.5, label: '> 1.5', dir: 'higher' },
};

export default function FinancialAnalysis() {
  const { state, dispatch, showLoading, hideLoading, toast } = useApp();
  const [years, setYears] = useState(state.financialYears.length ? state.financialYears : []);
  const [activeTab, setActiveTab] = useState('input');

  const addYear = () => {
    const idx = years.length;
    const start = 2025 - idx;
    setYears(prev => [...prev, { id: Date.now(), year: `FY${start - 1}-${String(start).slice(2)}`, revenue: '', ebitda: '', pat: '', total_assets: '', total_liabilities: '', net_worth: '', current_assets: '', current_liabilities: '' }]);
  };

  const removeYear = (id) => setYears(prev => prev.filter(y => y.id !== id));

  const updateYear = (id, field, value) => {
    setYears(prev => prev.map(y => y.id === id ? { ...y, [field]: value } : y));
  };

  const runAnalysis = useCallback(async () => {
    if (years.length === 0) { toast('Add financial year data first', 'warning'); return; }
    showLoading('Running comprehensive financial analysis...');
    try {
      const payload = {
        company_name: state.company.company_name || 'Company',
        company_id: state.company.cin || 'company_' + Date.now(),
        financial_data: years.map(y => ({
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
      };
      const result = await api.runFullAnalysis(payload);
      // Normalize: backend may nest under 'analysis' or return flat
      const analysis = result.analysis ? { ...result, ...result.analysis, ratios: result.ratios || result.analysis.financial_ratios, flags: result.flags || result.analysis.all_flags } : result;
      dispatch({ type: 'SET_ANALYSIS', payload: analysis });
      dispatch({ type: 'SET_FINANCIAL_YEARS', payload: years });
      setActiveTab('ratios');
      toast('Financial analysis complete!', 'success');
    } catch (e) {
      toast(e.message, 'error');
    } finally {
      hideLoading();
    }
  }, [years, dispatch, showLoading, hideLoading, toast]);

  const analysis = state.analysisResults;
  const formatName = n => n.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

  return (
    <>
      <p className="section-desc">Input financial data, then run comprehensive analysis with ratio computations, GST checks, and cross-verification.</p>

      {/* Tabs */}
      <div className="tabs">
        {['input', 'ratios', 'gst', 'banking', 'flags'].map(t => (
          <button key={t} className={`tab${activeTab === t ? ' active' : ''}`} onClick={() => setActiveTab(t)}>
            {t === 'input' ? 'Input Data' : t === 'gst' ? 'GST Analysis' : formatName(t)}
          </button>
        ))}
      </div>

      {/* Input Tab */}
      {activeTab === 'input' && (
        <>
          <div style={{ display: 'flex', gap: 12, marginBottom: 20 }}>
            <button className="btn btn-primary" onClick={addYear}><Plus size={16} /> Add Financial Year</button>
            <button className="btn btn-success" onClick={runAnalysis} disabled={years.length === 0}><Play size={16} /> Run Analysis</button>
          </div>
          {years.map(yr => (
            <div className="fin-year-card" key={yr.id}>
              <h4>
                {yr.year}
                <button style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer' }} onClick={() => removeYear(yr.id)}>
                  <X size={16} />
                </button>
              </h4>
              <div className="fin-grid">
                {FIELDS.map(f => (
                  <div className="form-group" key={f.key}>
                    <label>{f.label}</label>
                    <input type="number" value={yr[f.key]} onChange={e => updateYear(yr.id, f.key, e.target.value)} placeholder="0" />
                  </div>
                ))}
              </div>
            </div>
          ))}
          {years.length === 0 && <p className="placeholder">No financial years added. Click "Add Financial Year" to begin.</p>}
        </>
      )}

      {/* Ratios Tab */}
      {activeTab === 'ratios' && (
        <div className="card">
          <h3>Financial Ratios</h3>
          {analysis?.ratios ? (
            <table className="metric-table">
              <thead><tr><th>Metric</th><th>Value</th><th>Benchmark</th><th>Status</th></tr></thead>
              <tbody>
                {Object.entries(analysis.ratios).filter(([, v]) => typeof v === 'number').map(([key, val]) => {
                  const bm = BENCHMARKS[key];
                  const ok = bm ? (bm.dir === 'lower' ? val <= bm.target : val >= bm.target) : true;
                  return (
                    <tr key={key}>
                      <td>{formatName(key)}</td>
                      <td><strong>{val.toFixed(2)}</strong></td>
                      <td>{bm ? bm.label : '-'}</td>
                      <td>{ok ? '✅' : '⚠️'}</td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          ) : <p className="placeholder">Run analysis to see financial ratios.</p>}
        </div>
      )}

      {/* GST Tab */}
      {activeTab === 'gst' && (
        <div className="card">
          <h3>GST Analysis</h3>
          {analysis?.gst_analysis
            ? <pre className="json-display">{JSON.stringify(analysis.gst_analysis, null, 2)}</pre>
            : <p className="placeholder">Run analysis with GST data to see results.</p>}
        </div>
      )}

      {/* Banking Tab */}
      {activeTab === 'banking' && (
        <div className="card">
          <h3>Banking Analysis</h3>
          {analysis?.bank_analysis
            ? <pre className="json-display">{JSON.stringify(analysis.bank_analysis, null, 2)}</pre>
            : <p className="placeholder">Run analysis with bank data to see results.</p>}
        </div>
      )}

      {/* Flags Tab */}
      {activeTab === 'flags' && (
        <div className="card">
          <h3>Red Flags & Observations</h3>
          {analysis?.flags && analysis.flags.length > 0 ? (
            analysis.flags.map((flag, i) => (
              <div key={i} className={`insight-card ${flag.severity || 'neutral'}`}>
                <div>
                  <strong>{flag.flag || flag.type || 'Flag'}</strong>
                  <p style={{ fontSize: 13, marginTop: 4 }}>{flag.detail || flag.description || ''}</p>
                </div>
              </div>
            ))
          ) : <p className="placeholder">No flags detected. Run analysis to check.</p>}
        </div>
      )}
    </>
  );
}
