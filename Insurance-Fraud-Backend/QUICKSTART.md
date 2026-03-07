# Insurance Fraud Detection - Quick Start Guide

## Overview
This is a complete machine learning pipeline for detecting insurance fraud using Python, scikit-learn, and XGBoost. The system includes data preprocessing, model training, and a Flask REST API for predictions.

## Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Prepare Your Data
Place your CSV files in the `data/` folder:
- **insurance_data.csv** (REQUIRED) - Your main dataset
  - Must include a fraud indicator column (e.g., 'fraud', 'is_fraud', 'FraudIndicator')
  - Mix of numeric and categorical features

Example columns:
```
claim_id, claim_amount, claimant_age, days_since_policy, claim_type, 
policy_type, fraud
```

### Step 3: Train the Model
```bash
cd src
python train_model.py
```

This will:
1. Load and clean your data
2. Preprocess features (scaling, encoding, etc.)
3. Train 3 different models (Logistic Regression, Random Forest, XGBoost)
4. Compare performance and select the best
5. Save trained model to `model/` folder

## Using Predictions

### Option A: Use Python Script
```python
from src.predict import FraudPredictor

predictor = FraudPredictor()

# Single prediction
result = predictor.predict({
    'claim_amount': 5000,
    'claimant_age': 35,
    'days_since_policy': 180,
    # ... other features
})

print(f"Fraud: {result['prediction']}")
print(f"Confidence: {result['fraud_probability']:.2%}")
```

### Option B: Use REST API
```bash
# Start server
python app.py

# In another terminal, make requests
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"claim_amount": 5000, "claimant_age": 35, "days_since_policy": 180}'
```

## Model Output

**Prediction values:**
- `0` = Legitimate claim
- `1` = Fraudulent claim

**Confidence scores:**
- `fraud_probability`: 0.0 to 1.0 (higher = more likely fraud)
- `legitimate_probability`: 0.0 to 1.0 (higher = more likely legitimate)

## Understanding the Results

### When model says: Fraud (1)
- Check claims with fraud_probability > 0.7
- Investigate high-risk claims manually
- Build flag system for human review

### When model says: Legitimate (0)
- fraud_probability < 0.3
- Can process automatically
- Good for fast-track approvals

### Gray zone (0.3-0.7 probability)
- Requires manual investigation
- Enhanced verification recommended
- Good for training new investigators

## Data Requirements

Your insurance_data.csv should have:

**Required:**
- At least one fraud indicator column
- Multiple features (10+) for better performance
- Thousands of records (100+ minimum, 10000+ recommended)

**Good features include:**
- Claim amount
- Policy duration
- Claimant age
- Claim type
- Policy type
- Number of claims
- Time since policy start
- Claim frequency
- Geographic location

**Format:**
```csv
claim_id,amount,age,policy_days,claim_type,policy_type,fraud
CLM001,5000,35,180,Auto,Comprehensive,0
CLM002,15000,42,45,Medical,Full,1
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'xgboost'` | Run: `pip install -r requirements.txt` |
| `No fraud column found` | Verify CSV has fraud indicator, update column name in preprocess.py |
| `FileNotFoundError: model/fraud_model.pkl` | Run training first: `python train_model.py` |
| `Connection refused` on API | Ensure Flask server is running: `python app.py` |
| Model accuracy too low | Add more training data or engineer better features |

## Advanced Usage

### Custom Model Parameters
Edit `src/train_model.py`:
```python
# Change XGBoost parameters
model = xgb.XGBClassifier(
    n_estimators=200,      # More trees
    max_depth=8,           # Deeper trees
    learning_rate=0.05,    # Slower learning
    scale_pos_weight=3     # Penalize false negatives
)
```

### Batch Predictions from CSV
```python
from src.predict import load_and_predict

results = load_and_predict('data/test_claims.csv')
results.to_csv('predictions.csv', index=False)
```

### Cross-Validation
Add to train_model.py:
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1')
print(f"CV Scores: {scores}")
print(f"Mean: {scores.mean():.4f} (+/- {scores.std():.4f})")
```

## Performance Optimization

**If predictions are too slow:**
- Use Logistic Regression instead of XGBoost
- Reduce number of features
- Use model.predict() instead of predict_proba()

**If accuracy is poor:**
- Add more training data
- Engineer better features
- Increase XGBoost n_estimators
- Adjust class_weight parameter

**If model overfits:**
- Increase regularization
- Reduce tree depth
- Add more data
- Use cross-validation

## API Documentation

### Health Check
```
GET /health
Response: {"status": "healthy", "model_loaded": true}
```

### Single Prediction
```
POST /predict
Body: {"feature1": value1, "feature2": value2, ...}
Response: {
  "prediction": 1,
  "fraud_probability": 0.85,
  "legitimate_probability": 0.15
}
```

### Batch Prediction
```
POST /predict-batch
Body: {"records": [{"f1": v1, ...}, {"f1": v1, ...}]}
Response: {"predictions": [{...}, {...}]}
```

## Next Steps

1. **Try with your data**: Place CSV in data/ folder
2. **Run training**: `python src/train_model.py`
3. **Check results**: Review model performance metrics
4. **Deploy API**: `python app.py` for real-time predictions
5. **Monitor**: Track prediction accuracy over time

## Support

For issues:
1. Check README.md for full documentation
2. Review console output for error messages
3. Ensure data format matches requirements
4. Verify all dependencies installed

Good luck with your fraud detection system!
