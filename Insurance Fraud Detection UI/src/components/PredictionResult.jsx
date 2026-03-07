import { useEffect, useRef } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';
import { FiAlertTriangle, FiCheckCircle, FiInfo, FiShield } from 'react-icons/fi';

ChartJS.register(ArcElement, Tooltip, Legend);

const riskConfig = {
    HIGH: {
        color: 'text-red-400',
        bg: 'bg-red-500/10',
        border: 'border-red-500/30',
        gradient: ['#ef4444', '#991b1b'],
        icon: <FiAlertTriangle className="w-6 h-6" />,
        barColor: 'bg-gradient-to-r from-red-500 to-red-400',
    },
    MEDIUM: {
        color: 'text-amber-400',
        bg: 'bg-amber-500/10',
        border: 'border-amber-500/30',
        gradient: ['#f59e0b', '#92400e'],
        icon: <FiInfo className="w-6 h-6" />,
        barColor: 'bg-gradient-to-r from-amber-500 to-amber-400',
    },
    LOW: {
        color: 'text-emerald-400',
        bg: 'bg-emerald-500/10',
        border: 'border-emerald-500/30',
        gradient: ['#10b981', '#065f46'],
        icon: <FiCheckCircle className="w-6 h-6" />,
        barColor: 'bg-gradient-to-r from-emerald-500 to-emerald-400',
    },
};

export default function PredictionResult({ result, onReset }) {
    const config = riskConfig[result.riskLevel] || riskConfig.LOW;
    const probability = Math.round(result.probability * 100);
    const barRef = useRef(null);

    useEffect(() => {
        if (barRef.current) {
            barRef.current.style.width = '0%';
            setTimeout(() => {
                barRef.current.style.width = `${probability}%`;
            }, 300);
        }
    }, [probability]);

    const gaugeData = {
        datasets: [
            {
                data: [probability, 100 - probability],
                backgroundColor: [config.gradient[0], 'rgba(51,65,85,0.3)'],
                borderWidth: 0,
                cutout: '78%',
                circumference: 270,
                rotation: 225,
            },
        ],
    };

    const gaugeOptions = {
        responsive: true,
        maintainAspectRatio: true,
        plugins: {
            legend: { display: false },
            tooltip: { enabled: false },
        },
    };

    return (
        <div className="animate-slide-up space-y-6">
            {/* Header */}
            <div className={`flex items-center gap-3 px-5 py-4 rounded-xl ${config.bg} border ${config.border}`}>
                <span className={config.color}>{config.icon}</span>
                <div>
                    <div className={`text-lg font-bold ${config.color}`}>
                        {result.riskLevel} RISK
                    </div>
                    <div className="text-sm text-dark-400">Fraud detection analysis complete</div>
                </div>
            </div>

            {/* Gauge + Probability */}
            <div className="grid md:grid-cols-2 gap-6">
                {/* Gauge */}
                <div className="glass-card p-6 flex flex-col items-center justify-center">
                    <div className="relative w-48 h-48">
                        <Doughnut data={gaugeData} options={gaugeOptions} />
                        <div className="absolute inset-0 flex flex-col items-center justify-center pt-6">
                            <span className={`text-4xl font-bold ${config.color}`}>{probability}%</span>
                            <span className="text-sm text-dark-500 mt-1">Fraud Probability</span>
                        </div>
                    </div>
                </div>

                {/* Details */}
                <div className="glass-card p-6 space-y-5">
                    {/* Progress bar */}
                    <div>
                        <div className="flex justify-between text-sm mb-2">
                            <span className="text-dark-400">Fraud Probability</span>
                            <span className={`font-semibold ${config.color}`}>{probability}%</span>
                        </div>
                        <div className="w-full h-3 bg-dark-700 rounded-full overflow-hidden">
                            <div
                                ref={barRef}
                                className={`h-full rounded-full ${config.barColor} transition-all duration-1000 ease-out`}
                                style={{ width: '0%' }}
                            />
                        </div>
                    </div>

                    {/* Risk factors */}
                    {result.factors && (
                        <div>
                            <h4 className="text-sm font-medium text-dark-300 mb-3">Risk Factors</h4>
                            <div className="space-y-2">
                                {result.factors.map((factor) => (
                                    <div key={factor.name} className="flex items-center justify-between text-sm">
                                        <span className="text-dark-400">{factor.name}</span>
                                        <span
                                            className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${factor.impact === 'high'
                                                    ? 'bg-red-500/15 text-red-400'
                                                    : factor.impact === 'medium'
                                                        ? 'bg-amber-500/15 text-amber-400'
                                                        : 'bg-emerald-500/15 text-emerald-400'
                                                }`}
                                        >
                                            {factor.impact}
                                        </span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            </div>

            {/* Recommendation */}
            <div className="glass-card p-6">
                <div className="flex items-start gap-3">
                    <FiShield className="w-5 h-5 text-primary-400 mt-0.5 shrink-0" />
                    <div>
                        <h4 className="text-sm font-semibold text-white mb-1">Recommendation</h4>
                        <p className="text-dark-400 text-sm leading-relaxed">{result.recommendation}</p>
                    </div>
                </div>
            </div>

            {/* Reset */}
            <button onClick={onReset} className="btn-secondary w-full flex items-center justify-center gap-2">
                Analyze Another Claim
            </button>
        </div>
    );
}
