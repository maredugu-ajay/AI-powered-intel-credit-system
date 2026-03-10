import { useState } from 'react';
import { useApp } from '../context/AppContext';
import { MessageSquarePlus, Trash2 } from 'lucide-react';

const CATEGORIES = ['operations', 'management', 'market', 'compliance', 'financial', 'general'];
const IMPACTS = ['positive', 'neutral', 'negative'];

export default function PrimaryInsights() {
  const { state, dispatch, toast } = useApp();
  const [form, setForm] = useState({ category: 'operations', observation: '', impact: 'neutral', source: '' });

  const addInsight = () => {
    if (!form.observation.trim()) { toast('Enter an observation', 'warning'); return; }
    dispatch({
      type: 'ADD_INSIGHT',
      payload: { id: Date.now(), ...form, timestamp: new Date().toISOString() },
    });
    setForm(f => ({ ...f, observation: '', source: '' }));
    toast('Insight added!', 'success');
  };

  return (
    <>
      <p className="section-desc">Add qualitative observations from branch visits, management meetings, and field inspections to enhance the credit assessment.</p>

      {/* Form */}
      <div className="form-section">
        <h3><MessageSquarePlus size={18} /> Add Primary Insight</h3>
        <div className="form-row">
          <div className="form-group">
            <label>Category</label>
            <select value={form.category} onChange={e => setForm(f => ({ ...f, category: e.target.value }))}>
              {CATEGORIES.map(c => <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>)}
            </select>
          </div>
          <div className="form-group">
            <label>Impact Assessment</label>
            <select value={form.impact} onChange={e => setForm(f => ({ ...f, impact: e.target.value }))}>
              {IMPACTS.map(i => <option key={i} value={i}>{i.charAt(0).toUpperCase() + i.slice(1)}</option>)}
            </select>
          </div>
        </div>
        <div className="form-group full-width" style={{ marginBottom: 16 }}>
          <label>Observation</label>
          <textarea rows={3} value={form.observation} onChange={e => setForm(f => ({ ...f, observation: e.target.value }))}
            placeholder="Describe your observation from the field visit, meeting, or inspection..." />
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Source</label>
            <input value={form.source} onChange={e => setForm(f => ({ ...f, source: e.target.value }))}
              placeholder="e.g., Plant Visit, Management Meeting" />
          </div>
        </div>
        <div style={{ display: 'flex', gap: 12, marginTop: 16 }}>
          <button className="btn btn-primary" onClick={addInsight}><MessageSquarePlus size={16} /> Add Insight</button>
        </div>
      </div>

      {/* List */}
      <h3 style={{ marginBottom: 16, fontSize: 16 }}>Recorded Insights ({state.insights.length})</h3>
      {state.insights.length === 0
        ? <p className="placeholder">No insights added yet. Use the form above to add observations.</p>
        : state.insights.map(ins => (
          <div key={ins.id} className={`insight-card ${ins.impact}`}>
            <div style={{ flex: 1 }}>
              <strong>{ins.category.charAt(0).toUpperCase() + ins.category.slice(1)}</strong>
              <p style={{ marginTop: 4, fontSize: 13, lineHeight: 1.5 }}>{ins.observation}</p>
              <div className="insight-meta">
                <span className={`tag ${ins.impact === 'positive' ? 'tag-positive' : ins.impact === 'negative' ? 'tag-critical' : 'tag-warning'}`}>{ins.impact}</span>
                {ins.source && <span className="tag tag-info">{ins.source}</span>}
              </div>
            </div>
            <button style={{ background: 'none', border: 'none', color: 'var(--danger)', cursor: 'pointer', opacity: 0.5 }}
              onClick={() => dispatch({ type: 'REMOVE_INSIGHT', payload: ins.id })}>
              <Trash2 size={16} />
            </button>
          </div>
        ))
      }
    </>
  );
}
