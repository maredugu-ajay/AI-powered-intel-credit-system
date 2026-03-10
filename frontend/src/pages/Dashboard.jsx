import { useNavigate } from 'react-router-dom';
import { FileUp, BarChart3, Search, Shield, FileText, ChevronRight } from 'lucide-react';

const pipelineSteps = [
  { num: 1, title: 'Data Ingestor', desc: 'Upload & parse financial documents, GST returns, bank statements' },
  { num: 2, title: 'Financial Analysis', desc: 'Ratio computation, trend analysis, cross-verification' },
  { num: 3, title: 'Research Agent', desc: 'News, litigation, regulatory, sector & management checks' },
  { num: 4, title: 'Primary Insights', desc: 'Qualitative observations from branch visits & meetings' },
  { num: 5, title: 'ML Scoring', desc: 'Explainable Five Cs credit scoring with risk assessment' },
  { num: 6, title: 'CAM Report', desc: 'Auto-generate comprehensive Credit Appraisal Memo' },
];

const fiveCs = [
  { label: 'Character', angle: 0 },
  { label: 'Capacity', angle: 72 },
  { label: 'Capital', angle: 144 },
  { label: 'Collateral', angle: 216 },
  { label: 'Conditions', angle: 288 },
];

export default function Dashboard() {
  const navigate = useNavigate();

  return (
    <>
      {/* Welcome Banner */}
      <div className="welcome-banner">
        <div className="welcome-text">
          <h1>AI-Powered Credit Decisioning</h1>
          <p>
            Automate the end-to-end preparation of Credit Appraisal Memos with
            explainable ML scoring, multi-source data integration, and India-context intelligence.
          </p>
          <div className="welcome-actions">
            <button className="btn btn-accent btn-lg" onClick={() => navigate('/company')}>
              <FileUp size={18} /> Start New Appraisal
            </button>
          </div>
        </div>
        {/* Five Cs Wheel */}
        <div style={{ width: 200, height: 200, position: 'relative', flexShrink: 0 }}>
          <svg viewBox="0 0 200 200" style={{ width: '100%', height: '100%' }}>
            <circle cx="100" cy="100" r="80" fill="none" stroke="rgba(255,255,255,0.15)" strokeWidth="1" />
            <circle cx="100" cy="100" r="28" fill="var(--accent)" />
            <text x="100" y="105" textAnchor="middle" fill="white" fontSize="12" fontWeight="700">5 Cs</text>
            {fiveCs.map((c, i) => {
              const rad = (c.angle - 90) * (Math.PI / 180);
              const x = 100 + 75 * Math.cos(rad);
              const y = 100 + 75 * Math.sin(rad);
              return (
                <g key={i}>
                  <rect x={x - 35} y={y - 12} width="70" height="24" rx="12"
                    fill="rgba(255,255,255,0.2)" />
                  <text x={x} y={y + 4} textAnchor="middle" fill="white" fontSize="9" fontWeight="600">
                    {c.label}
                  </text>
                  <line x1={100 + 30 * Math.cos(rad)} y1={100 + 30 * Math.sin(rad)}
                    x2={x - 35 * Math.cos(rad)} y2={y - 13 * Math.sin(rad)}
                    stroke="rgba(255,255,255,0.2)" strokeWidth="1" />
                </g>
              );
            })}
          </svg>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        {[
          { icon: <FileUp size={22} />, value: '12+', label: 'Document Types', bg: 'linear-gradient(135deg, #1a237e, #3949ab)' },
          { icon: <BarChart3 size={22} />, value: '25+', label: 'Financial Ratios', bg: 'linear-gradient(135deg, #ff6f00, #ff9800)' },
          { icon: <Search size={22} />, value: '6', label: 'Research Sources', bg: 'linear-gradient(135deg, #28a745, #20c997)' },
          { icon: <Shield size={22} />, value: '5', label: 'Scoring Pillars', bg: 'linear-gradient(135deg, #dc3545, #e57373)' },
        ].map((s, i) => (
          <div className="stat-card" key={i}>
            <div className="stat-icon" style={{ background: s.bg }}>{s.icon}</div>
            <div className="stat-info">
              <h3>{s.value}</h3>
              <p>{s.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Pipeline */}
      <div className="pipeline-overview">
        <h3>Credit Appraisal Pipeline</h3>
        <div className="pipeline-steps">
          {pipelineSteps.map((step, i) => (
            <div key={i} style={{ display: 'flex', alignItems: 'center', gap: 8, flex: 1, minWidth: 0 }}>
              <div className="pipeline-step" style={{ flex: 1, minWidth: 140 }}>
                <div className="step-number">{step.num}</div>
                <div className="step-content">
                  <h4>{step.title}</h4>
                  <p>{step.desc}</p>
                </div>
              </div>
              {i < pipelineSteps.length - 1 && <ChevronRight className="pipeline-arrow" size={20} />}
            </div>
          ))}
        </div>
      </div>
    </>
  );
}
