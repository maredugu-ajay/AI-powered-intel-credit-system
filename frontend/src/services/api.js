const API_BASE = import.meta.env.VITE_API_URL || '';

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
      headers: { 'Content-Type': 'application/json', ...options.headers },
      ...options,
    };
    // Remove Content-Type for FormData
    if (options.body instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    const resp = await fetch(url, config);
    if (!resp.ok) {
      const err = await resp.json().catch(() => ({ detail: resp.statusText }));
      throw new Error(err.detail || err.message || `API Error ${resp.status}`);
    }
    const ct = resp.headers.get('content-type');
    if (ct && ct.includes('text/html')) return { html: await resp.text() };
    return resp.json();
  }

  // Health
  health() { return this.request('/health'); }

  // Documents
  uploadDocument(file, docType, companyId = 'company') {
    const fd = new FormData();
    fd.append('file', file);
    fd.append('document_type', docType);
    fd.append('company_id', companyId);
    return this.request('/api/documents/upload', { method: 'POST', body: fd });
  }

  // Analysis
  runFullAnalysis(data) {
    return this.request('/api/analysis/full', { method: 'POST', body: JSON.stringify(data) });
  }

  // Research
  runResearch(data) {
    return this.request('/api/research/secondary', { method: 'POST', body: JSON.stringify(data) });
  }

  addInsight(data) {
    return this.request('/api/research/insights', { method: 'POST', body: JSON.stringify(data) });
  }

  // CAM
  generateCAM(data) {
    return this.request('/api/cam/generate', { method: 'POST', body: JSON.stringify(data) });
  }

  generateCAMHtml(data) {
    return this.request('/api/cam/generate-html', { method: 'POST', body: JSON.stringify(data) });
  }

  getReport(id) {
    return this.request(`/api/cam/report/${id}`);
  }
}

const api = new ApiService();
export default api;
