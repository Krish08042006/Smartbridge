import axios from 'axios';

const api = axios.create({
    baseURL: '/api',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

/**
 * Map frontend form data → backend model feature names.
 */
const mapFormToBackend = (formData) => ({
    claim_amount: parseFloat(formData.claim_amount) || 0,
    claimant_age: parseInt(formData.claimant_age, 10) || 30,
    policy_duration_days: parseInt(formData.policy_duration_days, 10) || 365,
    previous_claims: parseInt(formData.previous_claims, 10) || 0,
    claim_type: formData.claim_type || 'Auto',
    policy_type: formData.policy_type || 'Standard',
    state: formData.state || 'CA',
    claim_status: formData.claim_status || 'Under Review',
    days_since_policy_start: parseInt(formData.days_since_policy_start, 10) || 180,
});

/**
 * Mock prediction for demo / offline mode.
 */
const mockPrediction = (data) => {
    const amount = parseFloat(data.claim_amount) || 0;
    const prevClaims = parseInt(data.previous_claims, 10) || 0;
    const age = parseInt(data.claimant_age, 10) || 30;

    let score = 0;
    if (amount > 50000) score += 25;
    else if (amount > 30000) score += 15;
    else if (amount > 10000) score += 8;

    if (prevClaims > 5) score += 25;
    else if (prevClaims > 2) score += 12;

    if (age < 25) score += 10;
    else if (age > 70) score += 5;

    const probability = Math.min(Math.max(score, 5), 95) / 100;
    let riskLevel = 'LOW';
    let recommendation = 'This claim appears to be genuine. Standard processing recommended.';

    if (probability >= 0.7) {
        riskLevel = 'HIGH';
        recommendation = 'This claim should be reviewed by the fraud investigation team immediately.';
    } else if (probability >= 0.4) {
        riskLevel = 'MEDIUM';
        recommendation = 'This claim has some risk indicators. Additional verification is recommended.';
    }

    return {
        prediction: riskLevel === 'LOW' ? 0 : 1,
        fraud_probability: probability,
        probability,
        riskLevel,
        recommendation,
        factors: [
            { name: 'Claim Amount', impact: amount > 30000 ? 'high' : amount > 10000 ? 'medium' : 'low' },
            { name: 'Previous Claims', impact: prevClaims > 5 ? 'high' : prevClaims > 2 ? 'medium' : 'low' },
            { name: 'Claimant Age', impact: age < 25 || age > 70 ? 'medium' : 'low' },
        ],
        _mock: true,
    };
};

/**
 * Submit a claim for fraud prediction.
 */
export const predictFraud = async (formData) => {
    const payload = mapFormToBackend(formData);
    try {
        const response = await api.post('/predict', payload);
        return response.data;
    } catch (error) {
        console.warn('Backend unavailable, using mock prediction:', error.message);
        await new Promise((resolve) => setTimeout(resolve, 800));
        return mockPrediction(payload);
    }
};

/**
 * Check backend health status.
 */
export const checkHealth = async () => {
    try {
        const response = await api.get('/health');
        return response.data;
    } catch {
        return { status: 'unreachable', model_loaded: false };
    }
};

/**
 * Get model information.
 */
export const getModelInfo = async () => {
    try {
        const response = await api.get('/model-info');
        return response.data;
    } catch {
        return null;
    }
};

/**
 * Get fraud statistics.
 */
export const getFraudStatistics = async () => {
    try {
        const response = await api.get('/fraud-statistics');
        return response.data;
    } catch {
        return null;
    }
};

/**
 * Get expected model features.
 */
export const getFeatures = async () => {
    try {
        const response = await api.get('/features');
        return response.data.features;
    } catch {
        return null;
    }
};

export default api;
