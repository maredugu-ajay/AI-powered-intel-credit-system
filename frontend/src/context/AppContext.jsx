import { createContext, useContext, useReducer, useCallback } from 'react';

const AppContext = createContext();

const initialState = {
  company: {
    company_name: '',
    cin: '',
    pan: '',
    gstin: '',
    incorporation_date: '',
    registered_address: '',
    industry: 'Manufacturing',
    sector: '',
    business_description: '',
    promoter_names: '',
    promoter_holding: '',
    annual_revenue: '',
    net_worth: '',
    existing_debt: '',
    credit_rating: 'NR',
    loan_amount: '',
    loan_purpose: '',
    loan_tenure: '',
    collateral_type: '',
    collateral_value: '',
  },
  documents: [],
  financialYears: [],
  analysisResults: null,
  researchResults: null,
  insights: [],
  scoringResults: null,
  camReport: null,
  loading: false,
  loadingMsg: '',
  toasts: [],
};

function reducer(state, action) {
  switch (action.type) {
    case 'SET_COMPANY':
      return { ...state, company: { ...state.company, ...action.payload } };
    case 'ADD_DOCUMENT':
      return { ...state, documents: [...state.documents, action.payload] };
    case 'SET_FINANCIAL_YEARS':
      return { ...state, financialYears: action.payload };
    case 'SET_ANALYSIS':
      return { ...state, analysisResults: action.payload };
    case 'SET_RESEARCH':
      return { ...state, researchResults: action.payload };
    case 'SET_INSIGHTS':
      return { ...state, insights: action.payload };
    case 'ADD_INSIGHT':
      return { ...state, insights: [...state.insights, action.payload] };
    case 'REMOVE_INSIGHT':
      return { ...state, insights: state.insights.filter(i => i.id !== action.payload) };
    case 'SET_SCORING':
      return { ...state, scoringResults: action.payload };
    case 'SET_CAM':
      return { ...state, camReport: action.payload };
    case 'SET_LOADING':
      return { ...state, loading: action.payload.loading, loadingMsg: action.payload.msg || '' };
    case 'ADD_TOAST':
      return { ...state, toasts: [...state.toasts, { id: Date.now(), ...action.payload }] };
    case 'REMOVE_TOAST':
      return { ...state, toasts: state.toasts.filter(t => t.id !== action.payload) };
    default:
      return state;
  }
}

export function AppProvider({ children }) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const showLoading = useCallback((msg) => dispatch({ type: 'SET_LOADING', payload: { loading: true, msg } }), []);
  const hideLoading = useCallback(() => dispatch({ type: 'SET_LOADING', payload: { loading: false } }), []);

  const toast = useCallback((message, type = 'info') => {
    const id = Date.now() + Math.random();
    dispatch({ type: 'ADD_TOAST', payload: { id, message, type } });
    setTimeout(() => dispatch({ type: 'REMOVE_TOAST', payload: id }), 4000);
  }, []);

  return (
    <AppContext.Provider value={{ state, dispatch, showLoading, hideLoading, toast }}>
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error('useApp must be used within AppProvider');
  return ctx;
}
