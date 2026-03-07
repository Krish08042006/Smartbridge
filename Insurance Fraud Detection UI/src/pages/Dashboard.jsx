import { useState, useEffect } from 'react';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
} from 'chart.js';
import { Pie, Bar, Doughnut } from 'react-chartjs-2';
import { FiShield, FiAlertTriangle, FiCheckCircle, FiActivity, FiTrendingUp, FiPieChart, FiRefreshCw } from 'react-icons/fi';
import { getFraudStatistics, getModelInfo } from '../services/api';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const colorMap = {
    primary: { bg: 'bg-primary-500/10', text: 'text-primary-400', border: 'border-primary-500/20' },
    red: { bg: 'bg-red-500/10', text: 'text-red-400', border: 'border-red-500/20' },
    emerald: { bg: 'bg-emerald-500/10', text: 'text-emerald-400', border: 'border-emerald-500/20' },
    accent: { bg: 'bg-accent-500/10', text: 'text-accent-400', border: 'border-accent-500/20' },
};

const chartTextColor = '#94a3b8';
const chartGridColor = 'rgba(51,65,85,0.4)';

// Fallback demo data
const DEMO_STATS = {
    total_predictions: 1247,
    fraud_cases: 186,
    legitimate_cases: 1061,
    fraud_rate: 14.9,
};

export default function Dashboard() {
    const [liveStats, setLiveStats] = useState(null);
    const [modelInfo, setModelInfo] = useState(null);
    const [isLive, setIsLive] = useState(false);
    const [refreshing, setRefreshing] = useState(false);

    const fetchData = async () => {
        setRefreshing(true);
        const [stats, info] = await Promise.all([getFraudStatistics(), getModelInfo()]);
        if (stats && stats.model_loaded) {
            setLiveStats(stats);
            setIsLive(true);
        } else {
            setIsLive(false);
        }
        if (info) setModelInfo(info);
        setRefreshing(false);
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 15000);
        return () => clearInterval(interval);
    }, []);

    const data = isLive ? liveStats : DEMO_STATS;
    const totalClaims = data.total_predictions || 0;
    const fraudCases = data.fraud_cases || 0;
    const genuineCases = data.legitimate_cases || 0;
    const fraudRate = data.fraud_rate || 0;

    const stats = [
        { label: 'Total Claims', value: totalClaims.toLocaleString(), icon: <FiActivity className="w-5 h-5" />, color: 'primary' },
        { label: 'Fraud Detected', value: fraudCases.toLocaleString(), icon: <FiAlertTriangle className="w-5 h-5" />, color: 'red' },
        { label: 'Genuine Claims', value: genuineCases.toLocaleString(), icon: <FiCheckCircle className="w-5 h-5" />, color: 'emerald' },
        { label: 'Fraud Rate', value: `${fraudRate}%`, icon: <FiShield className="w-5 h-5" />, color: 'accent' },
    ];

    // Fraud vs Genuine Pie
    const pieData = {
        labels: ['Fraudulent', 'Genuine'],
        datasets: [
            {
                data: [fraudCases || 186, genuineCases || 1061],
                backgroundColor: ['rgba(239,68,68,0.8)', 'rgba(16,185,129,0.8)'],
                borderColor: ['rgba(239,68,68,1)', 'rgba(16,185,129,1)'],
                borderWidth: 2,
                hoverOffset: 8,
            },
        ],
    };

    // Claim Amount Distribution (static demo)
    const barData = {
        labels: ['$0-10k', '$10k-25k', '$25k-50k', '$50k-75k', '$75k-100k', '$100k+'],
        datasets: [
            {
                label: 'Genuine',
                data: [320, 280, 220, 130, 70, 41],
                backgroundColor: 'rgba(16,185,129,0.7)',
                borderRadius: 6,
                borderSkipped: false,
            },
            {
                label: 'Fraudulent',
                data: [15, 28, 52, 45, 30, 16],
                backgroundColor: 'rgba(239,68,68,0.7)',
                borderRadius: 6,
                borderSkipped: false,
            },
        ],
    };

    // Fraud by Incident Type (static demo)
    const incidentData = {
        labels: ['Auto', 'Medical', 'Property', 'Liability'],
        datasets: [
            {
                label: 'Fraud Cases',
                data: [72, 51, 38, 25],
                backgroundColor: [
                    'rgba(99,102,241,0.7)',
                    'rgba(245,158,11,0.7)',
                    'rgba(239,68,68,0.7)',
                    'rgba(20,184,166,0.7)',
                ],
                borderRadius: 6,
                borderSkipped: false,
            },
        ],
    };

    // Overall Risk Gauge
    const gaugeData = {
        datasets: [
            {
                data: [fraudRate || 14.9, 100 - (fraudRate || 14.9)],
                backgroundColor: ['rgba(245,158,11,0.85)', 'rgba(51,65,85,0.3)'],
                borderWidth: 0,
                cutout: '78%',
                circumference: 270,
                rotation: 225,
            },
        ],
    };

    const commonBarOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { labels: { color: chartTextColor, padding: 16, usePointStyle: true, pointStyleWidth: 10 } },
            title: { display: false },
        },
        scales: {
            x: {
                ticks: { color: chartTextColor, font: { size: 11 } },
                grid: { display: false },
            },
            y: {
                ticks: { color: chartTextColor, font: { size: 11 } },
                grid: { color: chartGridColor },
            },
        },
    };

    return (
        <div className="min-h-screen pt-24 pb-16 px-4 sm:px-6">
            {/* Background */}
            <div className="fixed glow-orb w-[500px] h-[500px] bg-primary-600 -top-40 -left-40 opacity-10" />
            <div className="fixed glow-orb w-[400px] h-[400px] bg-accent-600 bottom-0 -right-32 opacity-10" />

            <div className="max-w-7xl mx-auto relative z-10">
                {/* Header */}
                <div className="mb-10 flex flex-col sm:flex-row sm:items-end sm:justify-between gap-4">
                    <div>
                        <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-4 bg-primary-500/10 border border-primary-500/20 rounded-full text-primary-300 text-sm font-medium">
                            <FiPieChart className="w-4 h-4" />
                            Analytics
                        </div>
                        <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
                            Fraud Analytics <span className="gradient-text">Dashboard</span>
                        </h1>
                        <p className="text-dark-400">
                            {isLive ? 'Live data from backend API.' : 'Showing demo data — start the backend for live stats.'}
                            {modelInfo && <span className="ml-2 text-dark-500">Model: {modelInfo.model_type}</span>}
                        </p>
                    </div>
                    <button
                        onClick={fetchData}
                        disabled={refreshing}
                        className="btn-secondary inline-flex items-center gap-2 text-sm self-start"
                    >
                        <FiRefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
                        Refresh
                    </button>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    {stats.map((stat) => {
                        const c = colorMap[stat.color];
                        return (
                            <div key={stat.label} className="glass-card p-5 group hover:border-dark-600 transition-colors">
                                <div className="flex items-center justify-between mb-3">
                                    <div className={`w-10 h-10 rounded-xl ${c.bg} border ${c.border} flex items-center justify-center ${c.text}`}>
                                        {stat.icon}
                                    </div>
                                    {isLive && (
                                        <span className="flex items-center gap-1 text-xs font-medium text-emerald-400">
                                            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                                            Live
                                        </span>
                                    )}
                                </div>
                                <div className="text-2xl font-bold text-white">{stat.value}</div>
                                <div className="text-sm text-dark-500 mt-0.5">{stat.label}</div>
                            </div>
                        );
                    })}
                </div>

                {/* Charts Grid */}
                <div className="grid lg:grid-cols-2 gap-6 mb-6">
                    {/* Fraud vs Genuine Pie */}
                    <div className="glass-card p-6">
                        <h3 className="text-lg font-semibold text-white mb-1">Fraud vs Genuine Claims</h3>
                        <p className="text-sm text-dark-500 mb-6">Distribution of claim classifications</p>
                        <div className="flex items-center justify-center" style={{ height: 280 }}>
                            <Pie
                                data={pieData}
                                options={{
                                    responsive: true,
                                    maintainAspectRatio: false,
                                    plugins: {
                                        legend: {
                                            position: 'bottom',
                                            labels: { color: chartTextColor, padding: 20, usePointStyle: true, pointStyleWidth: 10 },
                                        },
                                    },
                                }}
                            />
                        </div>
                    </div>

                    {/* Risk Score Gauge */}
                    <div className="glass-card p-6">
                        <h3 className="text-lg font-semibold text-white mb-1">Overall Fraud Risk Score</h3>
                        <p className="text-sm text-dark-500 mb-6">Aggregate fraud risk across all claims</p>
                        <div className="flex items-center justify-center" style={{ height: 280 }}>
                            <div className="relative w-56 h-56">
                                <Doughnut
                                    data={gaugeData}
                                    options={{
                                        responsive: true,
                                        maintainAspectRatio: true,
                                        plugins: { legend: { display: false }, tooltip: { enabled: false } },
                                    }}
                                />
                                <div className="absolute inset-0 flex flex-col items-center justify-center pt-6">
                                    <span className="text-5xl font-bold text-amber-400">{fraudRate}%</span>
                                    <span className="text-sm text-dark-500 mt-2">Fraud Rate</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="grid lg:grid-cols-2 gap-6">
                    {/* Claim Amount Distribution */}
                    <div className="glass-card p-6">
                        <h3 className="text-lg font-semibold text-white mb-1">Claim Amount Distribution</h3>
                        <p className="text-sm text-dark-500 mb-6">Genuine vs fraudulent claims by amount range</p>
                        <div style={{ height: 300 }}>
                            <Bar data={barData} options={commonBarOptions} />
                        </div>
                    </div>

                    {/* Fraud by Claim Type */}
                    <div className="glass-card p-6">
                        <h3 className="text-lg font-semibold text-white mb-1">Fraud by Claim Type</h3>
                        <p className="text-sm text-dark-500 mb-6">Number of fraud cases per claim category</p>
                        <div style={{ height: 300 }}>
                            <Bar
                                data={incidentData}
                                options={{
                                    ...commonBarOptions,
                                    indexAxis: 'y',
                                    plugins: { ...commonBarOptions.plugins, legend: { display: false } },
                                }}
                            />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
