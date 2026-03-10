import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AppProvider } from './context/AppContext';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import CompanyProfile from './pages/CompanyProfile';
import DataIngestor from './pages/DataIngestor';
import FinancialAnalysis from './pages/FinancialAnalysis';
import ResearchAgent from './pages/ResearchAgent';
import PrimaryInsights from './pages/PrimaryInsights';
import CreditScoring from './pages/CreditScoring';
import CAMReport from './pages/CAMReport';

export default function App() {
  return (
    <AppProvider>
      <BrowserRouter>
        <Routes>
          <Route element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="company" element={<CompanyProfile />} />
            <Route path="documents" element={<DataIngestor />} />
            <Route path="financials" element={<FinancialAnalysis />} />
            <Route path="research" element={<ResearchAgent />} />
            <Route path="insights" element={<PrimaryInsights />} />
            <Route path="scoring" element={<CreditScoring />} />
            <Route path="cam" element={<CAMReport />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AppProvider>
  );
}
