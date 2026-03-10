import { useApp } from '../context/AppContext';
import { CheckCircle, AlertCircle, AlertTriangle, Info } from 'lucide-react';

const icons = {
  success: CheckCircle,
  error: AlertCircle,
  warning: AlertTriangle,
  info: Info,
};

export default function Toast() {
  const { state } = useApp();

  if (state.toasts.length === 0) return null;

  return (
    <div className="toast-container">
      {state.toasts.map(t => {
        const Icon = icons[t.type] || icons.info;
        return (
          <div key={t.id} className={`toast ${t.type}`}>
            <Icon size={18} />
            {t.message}
          </div>
        );
      })}
    </div>
  );
}
