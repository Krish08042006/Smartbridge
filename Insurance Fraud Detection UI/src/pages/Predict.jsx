import { useState } from 'react';
import ClaimForm from '../components/ClaimForm';
import PredictionResult from '../components/PredictionResult';
import { predictFraud } from '../services/api';
import { FiShield } from 'react-icons/fi';

export default function Predict() {
    const [result, setResult] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = async (formData) => {
        setIsLoading(true);
        try {
            const prediction = await predictFraud(formData);
            setResult(prediction);
        } catch (err) {
            console.error('Prediction failed:', err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleReset = () => setResult(null);

    return (
        <div className="min-h-screen pt-24 pb-16 px-4 sm:px-6">
            {/* Background Orbs */}
            <div className="fixed glow-orb w-[400px] h-[400px] bg-primary-600 top-32 -right-40 opacity-10" />
            <div className="fixed glow-orb w-[300px] h-[300px] bg-accent-600 bottom-20 -left-32 opacity-10" />

            <div className="max-w-2xl mx-auto relative z-10">
                {/* Header */}
                <div className="text-center mb-10">
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 mb-4 bg-primary-500/10 border border-primary-500/20 rounded-full text-primary-300 text-sm font-medium">
                        <FiShield className="w-4 h-4" />
                        Fraud Prediction
                    </div>
                    <h1 className="text-3xl md:text-4xl font-bold text-white mb-3">
                        Insurance Claim <span className="gradient-text">Prediction</span>
                    </h1>
                    <p className="text-dark-400 max-w-md mx-auto">
                        Enter the claim details below for an instant AI-powered fraud risk assessment.
                    </p>
                </div>

                {/* Card */}
                <div className="glass-card p-6 md:p-8">
                    {result ? (
                        <PredictionResult result={result} onReset={handleReset} />
                    ) : (
                        <ClaimForm onSubmit={handleSubmit} isLoading={isLoading} />
                    )}
                </div>
            </div>
        </div>
    );
}
