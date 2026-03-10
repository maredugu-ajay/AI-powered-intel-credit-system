import { useState, useRef } from 'react';
import { useApp } from '../context/AppContext';
import { Upload, FileText, CheckCircle } from 'lucide-react';
import api from '../services/api';

const DOC_TYPES = [
  'annual_report', 'financial_statement', 'gst_return', 'bank_statement',
  'itr', 'legal_notice', 'sanction_letter', 'rating_report',
];

export default function DataIngestor() {
  const { state, dispatch, showLoading, hideLoading, toast } = useApp();
  const [docType, setDocType] = useState('annual_report');
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef();

  const handleUpload = async (file) => {
    showLoading(`Uploading & parsing: ${file.name}...`);
    try {
      const result = await api.uploadDocument(file, docType);
      dispatch({ type: 'ADD_DOCUMENT', payload: { type: docType, name: file.name, data: result } });
      toast('Document parsed successfully!', 'success');
    } catch (e) {
      toast(e.message, 'error');
    } finally {
      hideLoading();
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    if (e.dataTransfer.files.length) handleUpload(e.dataTransfer.files[0]);
  };

  return (
    <>
      <p className="section-desc">Upload financial documents for data extraction and analysis.</p>

      {/* Upload Area */}
      <div
        className={`upload-area${dragOver ? ' dragover' : ''}`}
        onClick={() => fileRef.current?.click()}
        onDragOver={e => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
      >
        <Upload size={48} color="var(--primary)" />
        <h3>Drop files here or click to upload</h3>
        <p>Supports PDF, Excel, CSV, JSON, DOCX (Max 50MB)</p>
        <div style={{ marginTop: 20, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8 }}>
          <label style={{ fontSize: 13, color: 'var(--text-secondary)' }}>Document Type:</label>
          <select value={docType} onChange={e => setDocType(e.target.value)}
            style={{ padding: '8px 12px', border: '1px solid var(--border)', borderRadius: 8, fontSize: 13 }}
            onClick={e => e.stopPropagation()}
          >
            {DOC_TYPES.map(t => <option key={t} value={t}>{t.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</option>)}
          </select>
        </div>
        <input ref={fileRef} type="file" hidden accept=".pdf,.xlsx,.xls,.csv,.json,.docx"
          onChange={e => { if (e.target.files[0]) handleUpload(e.target.files[0]); }} />
      </div>

      {/* Parsed Results */}
      {state.documents.length > 0 && (
        <div className="card">
          <h3><CheckCircle size={18} color="var(--success)" /> Parsed Documents ({state.documents.length})</h3>
          <pre className="json-display">{JSON.stringify(state.documents, null, 2)}</pre>
        </div>
      )}
    </>
  );
}
