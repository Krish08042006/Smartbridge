import { useState, useEffect } from 'react';
import { checkHealth } from '../services/api';

export default function ConnectionStatus() {
    const [status, setStatus] = useState('checking'); // checking | connected | offline

    useEffect(() => {
        let cancelled = false;

        const ping = async () => {
            const result = await checkHealth();
            if (cancelled) return;

            if (result.status === 'healthy') {
                setStatus('connected');
            } else {
                setStatus('offline');
            }
        };

        ping();
        const interval = setInterval(ping, 30000); // re-check every 30s

        return () => {
            cancelled = true;
            clearInterval(interval);
        };
    }, []);

    if (status === 'checking') return null;

    const isConnected = status === 'connected';

    return (
        <div
            className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium transition-all duration-300 ${isConnected
                    ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-400'
                    : 'bg-amber-500/10 border border-amber-500/20 text-amber-400'
                }`}
            title={isConnected ? 'Flask backend is running' : 'Backend offline – using demo mode'}
        >
            <span className={`w-1.5 h-1.5 rounded-full ${isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-amber-400'}`} />
            {isConnected ? 'API Connected' : 'Demo Mode'}
        </div>
    );
}
