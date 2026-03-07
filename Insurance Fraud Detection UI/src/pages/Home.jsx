import { Link } from 'react-router-dom';
import { FiShield, FiCpu, FiBarChart2, FiZap, FiArrowRight } from 'react-icons/fi';

const features = [
    {
        icon: <FiCpu className="w-6 h-6" />,
        title: 'ML-Powered Detection',
        description: 'Advanced Random Forest & XGBoost models trained on real insurance data for high-accuracy fraud detection.',
    },
    {
        icon: <FiZap className="w-6 h-6" />,
        title: 'Real-Time Prediction',
        description: 'Submit claims and get instant fraud risk assessments through our Flask REST API integration.',
    },
    {
        icon: <FiBarChart2 className="w-6 h-6" />,
        title: 'Analytics Dashboard',
        description: 'Comprehensive fraud analytics with interactive charts, risk distribution, and trend visualization.',
    },
];

export default function Home() {
    return (
        <div className="min-h-screen">
            {/* Hero Section */}
            <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
                {/* Background Orbs */}
                <div className="glow-orb w-[500px] h-[500px] bg-primary-600 top-20 -left-40 animate-float" />
                <div className="glow-orb w-[400px] h-[400px] bg-accent-600 bottom-20 -right-32 animate-float-slow" />
                <div className="glow-orb w-[300px] h-[300px] bg-primary-500 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-10" />

                {/* Grid Pattern Overlay */}
                <div className="absolute inset-0 bg-[linear-gradient(rgba(99,102,241,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(99,102,241,0.03)_1px,transparent_1px)] bg-[size:60px_60px]" />

                <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 text-center">
                    {/* Badge */}
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-8 bg-primary-500/10 border border-primary-500/20 rounded-full text-primary-300 text-sm font-medium animate-fade-in">
                        <FiShield className="w-4 h-4" />
                        <span>AI-Powered Fraud Detection</span>
                    </div>

                    {/* Title */}
                    <h1 className="text-4xl sm:text-5xl md:text-7xl font-extrabold leading-tight mb-6 animate-slide-up">
                        <span className="text-white">Insurance</span>
                        <br />
                        <span className="gradient-text bg-300% animate-gradient">Fraud Detection</span>
                        <br />
                        <span className="text-white">System</span>
                    </h1>

                    {/* Subtitle */}
                    <p className="text-lg md:text-xl text-dark-400 max-w-2xl mx-auto mb-10 animate-slide-up animate-delay-200">
                        Detect fraudulent insurance claims using Machine Learning. Our system analyzes claim
                        details and predicts whether a claim is fraudulent or genuine with high accuracy.
                    </p>

                    {/* CTA Buttons */}
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up animate-delay-300">
                        <Link to="/predict" className="btn-primary inline-flex items-center gap-2 text-lg">
                            Check Claim
                            <FiArrowRight className="w-5 h-5" />
                        </Link>
                        <Link to="/dashboard" className="btn-secondary inline-flex items-center gap-2 text-lg">
                            View Dashboard
                        </Link>
                    </div>

                    {/* Stats */}
                    <div className="grid grid-cols-3 gap-6 max-w-lg mx-auto mt-20 animate-fade-in animate-delay-500">
                        {[
                            { value: '95%+', label: 'Accuracy' },
                            { value: '<1s', label: 'Response' },
                            { value: '7+', label: 'Features' },
                        ].map((stat) => (
                            <div key={stat.label} className="text-center">
                                <div className="text-2xl md:text-3xl font-bold gradient-text">{stat.value}</div>
                                <div className="text-sm text-dark-500 mt-1">{stat.label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="relative py-24 px-4 sm:px-6">
                <div className="max-w-6xl mx-auto">
                    <div className="text-center mb-16">
                        <h2 className="section-title mb-4">How It Works</h2>
                        <p className="text-dark-400 text-lg max-w-xl mx-auto">
                            Our system uses advanced machine learning algorithms to detect insurance fraud patterns.
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-6">
                        {features.map((feature, index) => (
                            <div
                                key={feature.title}
                                className="glass-card-hover p-8 group"
                                style={{ animationDelay: `${index * 150}ms` }}
                            >
                                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500/20 to-accent-500/20 border border-primary-500/20 flex items-center justify-center text-primary-400 mb-5 group-hover:border-primary-500/40 transition-colors">
                                    {feature.icon}
                                </div>
                                <h3 className="text-xl font-semibold text-white mb-3">{feature.title}</h3>
                                <p className="text-dark-400 leading-relaxed">{feature.description}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="relative py-24 px-4 sm:px-6">
                <div className="max-w-4xl mx-auto">
                    <div className="glass-card p-12 md:p-16 text-center relative overflow-hidden">
                        <div className="glow-orb w-60 h-60 bg-primary-500 -top-20 -right-20 opacity-15" />
                        <div className="glow-orb w-40 h-40 bg-accent-500 -bottom-10 -left-10 opacity-15" />
                        <div className="relative z-10">
                            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
                                Ready to Detect Fraud?
                            </h2>
                            <p className="text-dark-400 text-lg mb-8 max-w-lg mx-auto">
                                Submit a claim for instant AI-powered fraud risk assessment. It only takes a minute.
                            </p>
                            <Link to="/predict" className="btn-primary inline-flex items-center gap-2 text-lg">
                                Start Prediction
                                <FiArrowRight className="w-5 h-5" />
                            </Link>
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
}
