import { useApp } from '../context/AppContext';

export default function LoadingOverlay() {
  const { state } = useApp();

  if (!state.loading) return null;

  return (
    <div className="loading-overlay">
      <div className="loading-content">
        <div className="spinner" />
        <p>{state.loadingMsg || 'Processing...'}</p>
      </div>
    </div>
  );
}
