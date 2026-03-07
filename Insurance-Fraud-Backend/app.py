from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from predict import FraudPredictor
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app, origins=['http://localhost:5173', 'http://localhost:3000', 'http://127.0.0.1:5173'])

# Load predictor once at startup
try:
    predictor = FraudPredictor()
    MODEL_LOADED = True
except Exception as e:
    print(f"Warning: Could not load model - {e}")
    MODEL_LOADED = False
    predictor = None

# In-memory prediction tracker
prediction_stats = {
    'total_predictions': 0,
    'fraud_cases': 0,
    'legitimate_cases': 0,
}

# Expected feature names for the model (excluding target and IDs)
MODEL_FEATURES = [
    {'name': 'claim_amount', 'type': 'number', 'label': 'Claim Amount ($)', 'placeholder': 'e.g. 25000'},
    {'name': 'claimant_age', 'type': 'number', 'label': 'Claimant Age', 'placeholder': 'e.g. 35'},
    {'name': 'policy_duration_days', 'type': 'number', 'label': 'Policy Duration (days)', 'placeholder': 'e.g. 365'},
    {'name': 'previous_claims', 'type': 'number', 'label': 'Previous Claims', 'placeholder': 'e.g. 2'},
    {'name': 'claim_type', 'type': 'select', 'label': 'Claim Type',
     'options': ['Auto', 'Medical', 'Property', 'Liability', 'Disability']},
    {'name': 'policy_type', 'type': 'select', 'label': 'Policy Type',
     'options': ['Basic', 'Standard', 'Premium', 'Comprehensive']},
    {'name': 'state', 'type': 'select', 'label': 'State',
     'options': ['CA', 'TX', 'NY', 'FL', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI']},
    {'name': 'claim_status', 'type': 'select', 'label': 'Claim Status',
     'options': ['Approved', 'Denied', 'Under Review', 'Closed']},
    {'name': 'days_since_policy_start', 'type': 'number', 'label': 'Days Since Policy Start', 'placeholder': 'e.g. 180'},
]


def enrich_prediction(result, input_data):
    """Add riskLevel, recommendation, and factors to raw prediction result."""
    if 'error' in result:
        return result

    prob = result.get('fraud_probability', 0)
    prediction = result.get('prediction', 0)

    # Determine risk level
    if prob >= 0.7:
        risk_level = 'HIGH'
        recommendation = 'This claim should be reviewed by the fraud investigation team immediately.'
    elif prob >= 0.4:
        risk_level = 'MEDIUM'
        recommendation = 'This claim has some risk indicators. Additional verification is recommended.'
    else:
        risk_level = 'LOW'
        recommendation = 'This claim appears to be genuine. Standard processing recommended.'

    # Compute contributing risk factors
    factors = []
    claim_amount = float(input_data.get('claim_amount', 0) or 0)
    previous_claims = int(input_data.get('previous_claims', 0) or 0)
    claimant_age = int(input_data.get('claimant_age', 30) or 30)
    policy_duration = int(input_data.get('policy_duration_days', 365) or 365)

    factors.append({
        'name': 'Claim Amount',
        'impact': 'high' if claim_amount > 30000 else ('medium' if claim_amount > 10000 else 'low')
    })
    factors.append({
        'name': 'Previous Claims',
        'impact': 'high' if previous_claims > 5 else ('medium' if previous_claims > 2 else 'low')
    })
    factors.append({
        'name': 'Claimant Age',
        'impact': 'medium' if claimant_age < 25 or claimant_age > 70 else 'low'
    })
    factors.append({
        'name': 'Policy Duration',
        'impact': 'medium' if policy_duration < 90 else 'low'
    })

    result['riskLevel'] = risk_level
    result['probability'] = prob
    result['recommendation'] = recommendation
    result['factors'] = factors
    return result


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': MODEL_LOADED
    }), 200


@app.route('/model-info', methods=['GET'])
def model_info():
    """Get model information"""
    if not MODEL_LOADED:
        return jsonify({'error': 'Model not loaded'}), 400

    info = predictor.get_model_info()
    info['feature_count'] = len(MODEL_FEATURES)
    return jsonify(info), 200


@app.route('/features', methods=['GET'])
def features():
    """Return the list of expected features for the model"""
    return jsonify({'features': MODEL_FEATURES}), 200


@app.route('/predict', methods=['POST'])
def predict():
    """
    Make fraud prediction for a single record.
    Returns enriched result with riskLevel, recommendation, and factors.
    """
    if not MODEL_LOADED:
        return jsonify({'error': 'Model not loaded'}), 400

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Make prediction
        result = predictor.predict(data, return_probability=True)

        if 'error' in result:
            return jsonify(result), 400

        # Enrich with risk level, recommendation, factors
        result = enrich_prediction(result, data)

        # Track stats
        prediction_stats['total_predictions'] += 1
        if result.get('prediction') == 1:
            prediction_stats['fraud_cases'] += 1
        else:
            prediction_stats['legitimate_cases'] += 1

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    """Make fraud predictions for multiple records"""
    if not MODEL_LOADED:
        return jsonify({'error': 'Model not loaded'}), 400

    try:
        data = request.get_json()
        if not data or 'records' not in data:
            return jsonify({'error': 'No records provided'}), 400

        records = data['records']
        if not isinstance(records, list):
            return jsonify({'error': 'Records must be a list'}), 400

        results = []
        for record in records:
            raw = predictor.predict(record, return_probability=True)
            enriched = enrich_prediction(raw, record)
            results.append(enriched)

            # Track stats
            prediction_stats['total_predictions'] += 1
            if enriched.get('prediction') == 1:
                prediction_stats['fraud_cases'] += 1
            else:
                prediction_stats['legitimate_cases'] += 1

        return jsonify({'predictions': results}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/fraud-statistics', methods=['GET'])
def fraud_statistics():
    """Get fraud detection statistics"""
    total = prediction_stats['total_predictions']
    fraud = prediction_stats['fraud_cases']
    legit = prediction_stats['legitimate_cases']
    rate = round((fraud / total) * 100, 1) if total > 0 else 0.0

    return jsonify({
        'total_predictions': total,
        'fraud_cases': fraud,
        'legitimate_cases': legit,
        'fraud_rate': rate,
        'model_loaded': MODEL_LOADED,
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Insurance Fraud Detection API...")
    print("=" * 60)
    if MODEL_LOADED:
        print("✓ Model loaded successfully")
    else:
        print("✗ Warning: Model not loaded. Train model first.")
    print(f"✓ Endpoints: /health, /predict, /predict-batch, /features, /fraud-statistics, /model-info")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)
