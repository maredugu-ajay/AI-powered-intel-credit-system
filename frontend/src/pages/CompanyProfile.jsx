import { useApp } from '../context/AppContext';
import { Building2, Users, Landmark, Save } from 'lucide-react';

export default function CompanyProfile() {
  const { state, dispatch, toast } = useApp();
  const c = state.company;

  const update = (field, value) => {
    dispatch({ type: 'SET_COMPANY', payload: { [field]: value } });
  };

  const save = () => {
    localStorage.setItem('intelcredit_company', JSON.stringify(state.company));
    toast('Company data saved successfully!', 'success');
  };

  return (
    <>
      <p className="section-desc">Enter the borrower company details for credit appraisal.</p>

      {/* Basic Info */}
      <div className="form-section">
        <h3><Building2 size={18} /> Company Information</h3>
        <div className="form-row">
          <div className="form-group">
            <label>Company Name</label>
            <input value={c.company_name} onChange={e => update('company_name', e.target.value)} />
          </div>
          <div className="form-group">
            <label>CIN</label>
            <input value={c.cin} onChange={e => update('cin', e.target.value)} />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>PAN</label>
            <input value={c.pan} onChange={e => update('pan', e.target.value)} />
          </div>
          <div className="form-group">
            <label>GSTIN</label>
            <input value={c.gstin} onChange={e => update('gstin', e.target.value)} />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Incorporation Date</label>
            <input type="date" value={c.incorporation_date} onChange={e => update('incorporation_date', e.target.value)} />
          </div>
          <div className="form-group">
            <label>Registered Address</label>
            <input value={c.registered_address} onChange={e => update('registered_address', e.target.value)} />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Industry</label>
            <select value={c.industry} onChange={e => update('industry', e.target.value)}>
              <option>Manufacturing</option>
              <option>Services</option>
              <option>Trading</option>
              <option>Infrastructure</option>
              <option>IT/ITES</option>
              <option>Pharma</option>
              <option>Real Estate</option>
              <option>Agriculture</option>
            </select>
          </div>
          <div className="form-group">
            <label>Sector</label>
            <input value={c.sector} onChange={e => update('sector', e.target.value)} />
          </div>
        </div>
        <div className="form-group full-width">
          <label>Business Description</label>
          <textarea rows={3} value={c.business_description} onChange={e => update('business_description', e.target.value)} />
        </div>
      </div>

      {/* Promoter Info */}
      <div className="form-section">
        <h3><Users size={18} /> Promoter Details</h3>
        <div className="form-row">
          <div className="form-group">
            <label>Promoter Names</label>
            <input value={c.promoter_names} onChange={e => update('promoter_names', e.target.value)} />
          </div>
          <div className="form-group">
            <label>Promoter Holding (%)</label>
            <input type="number" value={c.promoter_holding} onChange={e => update('promoter_holding', e.target.value)} />
          </div>
        </div>
      </div>

      {/* Financial Overview */}
      <div className="form-section">
        <h3><Landmark size={18} /> Financial Overview & Loan Request</h3>
        <div className="form-row">
          <div className="form-group">
            <label>Annual Revenue (₹ Cr)</label>
            <input type="number" value={c.annual_revenue} onChange={e => update('annual_revenue', e.target.value)} />
          </div>
          <div className="form-group">
            <label>Net Worth (₹ Cr)</label>
            <input type="number" value={c.net_worth} onChange={e => update('net_worth', e.target.value)} />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Existing Debt (₹ Cr)</label>
            <input type="number" value={c.existing_debt} onChange={e => update('existing_debt', e.target.value)} />
          </div>
          <div className="form-group">
            <label>Credit Rating</label>
            <select value={c.credit_rating} onChange={e => update('credit_rating', e.target.value)}>
              {['AAA','AA+','AA','AA-','A+','A','A-','BBB+','BBB','BBB-','BB+','BB','BB-','B+','B','NR'].map(r =>
                <option key={r}>{r}</option>
              )}
            </select>
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Loan Amount Requested (₹)</label>
            <input type="number" value={c.loan_amount} onChange={e => update('loan_amount', e.target.value)} />
          </div>
          <div className="form-group">
            <label>Loan Purpose</label>
            <input value={c.loan_purpose} onChange={e => update('loan_purpose', e.target.value)} />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Loan Tenure (Years)</label>
            <input type="number" value={c.loan_tenure} onChange={e => update('loan_tenure', e.target.value)} />
          </div>
          <div className="form-group">
            <label>Collateral Type</label>
            <input value={c.collateral_type} onChange={e => update('collateral_type', e.target.value)} />
          </div>
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Collateral Value (₹)</label>
            <input type="number" value={c.collateral_value} onChange={e => update('collateral_value', e.target.value)} />
          </div>
        </div>
      </div>

      <button className="btn btn-primary btn-lg" onClick={save}>
        <Save size={18} /> Save Company Data
      </button>
    </>
  );
}
