import { useApp } from '../context/AppContext';
import { Search, Newspaper, Gavel, ShieldCheck, Factory, Users } from 'lucide-react';
import api from '../services/api';

export default function ResearchAgent() {
  const { state, dispatch, showLoading, hideLoading, toast } = useApp();

  const runResearch = async () => {
    showLoading('Conducting secondary research across multiple sources...');
    try {
      const result = await api.runResearch({
        company_id: state.company.cin || 'company_' + Date.now(),
        company_name: state.company.company_name || 'Company',
        cin: state.company.cin || '',
        gstin: state.company.gstin || '',
      });
      dispatch({ type: 'SET_RESEARCH', payload: result });
      toast('Research complete!', 'success');
    } catch (e) {
      toast(e.message, 'error');
    } finally {
      hideLoading();
    }
  };

  const data = state.researchResults;

  return (
    <>
      <p className="section-desc">Automated secondary research: news analysis, litigation checks, regulatory compliance, sector outlook, and management background.</p>

      <div className="card" style={{ textAlign: 'center' }}>
        <button className="btn btn-primary btn-lg" onClick={runResearch}>
          <Search size={18} /> Run Secondary Research
        </button>
        <p className="hint">Searches news, e-Courts, NCLT, MCA, sector databases & management records</p>
      </div>

      {data && (
        <div className="research-grid">
          {/* News */}
          {data.news_analysis && (
            <div className="card research-card">
              <h3><Newspaper size={18} /> News Analysis</h3>
              {(Array.isArray(data.news_analysis) ? data.news_analysis : [data.news_analysis]).map((n, i) => {
                const s = n.sentiment || 'neutral';
                return (
                  <div key={i} className={`insight-card ${s === 'positive' ? 'positive' : s === 'negative' ? 'negative' : 'neutral'}`}>
                    <div>
                      <strong>{n.title || n.headline || 'News'}</strong>
                      <p style={{ fontSize: 13, marginTop: 4 }}>{n.summary || n.text || ''}</p>
                      <div className="insight-meta">
                        <span className={`tag ${s === 'positive' ? 'tag-positive' : s === 'negative' ? 'tag-critical' : 'tag-info'}`}>{s}</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          {/* Litigation */}
          {data.litigation && (
            <div className="card research-card">
              <h3><Gavel size={18} /> Litigation Check</h3>
              <pre className="json-display">{JSON.stringify(data.litigation, null, 2)}</pre>
            </div>
          )}

          {/* Regulatory */}
          {data.regulatory && (
            <div className="card research-card">
              <h3><ShieldCheck size={18} /> Regulatory Status</h3>
              <pre className="json-display">{JSON.stringify(data.regulatory, null, 2)}</pre>
            </div>
          )}

          {/* Sector */}
          {data.sector_analysis && (
            <div className="card research-card">
              <h3><Factory size={18} /> Sector Analysis</h3>
              <pre className="json-display">{JSON.stringify(data.sector_analysis, null, 2)}</pre>
            </div>
          )}

          {/* Management */}
          {data.management && (
            <div className="card research-card full-width">
              <h3><Users size={18} /> Management Background</h3>
              <pre className="json-display">{JSON.stringify(data.management, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </>
  );
}
