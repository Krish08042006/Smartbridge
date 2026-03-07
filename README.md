Insurance Fraud Detection Using Machine Learning
A comprehensive machine learning solution for detecting insurance fraud using multiple classification algorithms.

Project Structure
Insurance-Fraud-Backend/
├── app.py                 # Flask API application
├── requirements.txt       # Python dependencies
├── data/
│   ├── insurance_data.csv      # Insurance claims data
│   ├── employee_data.csv       # Employee information (optional)
│   └── vendor_data.csv         # Vendor information
├── model/
│   ├── fraud_model.pkl         # Trained model (generated after training)
│   ├── scaler.pkl              # Feature scaler (generated after training)
│   └── label_encoders.pkl      # Label encoders (generated after training)
└── src/
    ├── train_model.py          # Model training pipeline
    ├── predict.py              # Prediction module
    └── preprocess.py           # Data preprocessing utilities
Setup Instructions
1. Create Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
2. Install Dependencies
pip install -r requirements.txt
3. Prepare Data
Ensure your CSV files are in the data/ directory:
insurance_data.csv (required) - must contain a fraud indicator column
vendor_data.csv (optional)
employee_data.csv (optional)
Training the Model
Run the Training Pipeline
cd src
python train_model.py
This will:

Load and preprocess the insurance data
Create feature engineering enhancements
Train three models:
Logistic Regression
Random Forest Classifier
XGBoost Classifier
Select the best performing model
Save the model and preprocessing objects to the model/ directory
Expected Output
==============================================================
Insurance Fraud Detection Model Training Pipeline
==============================================================

Loading and preprocessing data...
Loaded insurance data shape: (10000, 15)
Columns: ['claim_id', 'amount', 'claimant_age', ...]

==================================================
Training Logistic Regression...
==================================================

Logistic Regression Results:
  Accuracy:  0.8543
  Precision: 0.8200
  Recall:    0.7600
  F1-Score:  0.7885
  ROC-AUC:   0.9123

...
[More models trained]
...

==================================================
Best Model: XGBoost (F1-Score: 0.8456)
==================================================
Model Performance
The system evaluates models using:

Accuracy: Overall correctness of predictions
Precision: Accuracy of fraud predictions
Recall: Ability to identify all fraud cases
F1-Score: Balanced measure of precision and recall
ROC-AUC: Area under the ROC curve for model discrimination
Using the API
Start the Flask Server
python app.py
The API will be available at http://localhost:5000

API Endpoints
1. Health Check
GET /health
Response:

{
  "status": "healthy",
  "model_loaded": true
}
2. Get Model Info
GET /model-info
3. Predict Fraud (Single Record)
POST /predict
Content-Type: application/json

{
  "claim_amount": 5000,
  "claimant_age": 35,
  "days_since_policy_start": 180,
  ...
}
Response:

{
  "prediction": 1,
  "fraud_probability": 0.85,
  "legitimate_probability": 0.15
}
4. Predict Fraud (Batch)
POST /predict-batch
Content-Type: application/json

{
  "records": [
    {"feature1": value1, "feature2": value2, ...},
    {"feature1": value1, "feature2": value2, ...}
  ]
}
5. Get Fraud Statistics
GET /fraud-statistics
Data Format Requirements
Your insurance_data.csv should contain:

A fraud indicator column (named something like: fraud, is_fraud, FraudIndicator, etc.)
Numeric features (claim amount, policy duration, age, etc.)
Categorical features (claim type, policy type, etc.)
Example structure:

claim_id,claim_amount,claimant_age,days_since_policy,claim_type,fraud
CLM001,5000,35,180,Auto,0
CLM002,15000,42,45,Medical,1
CLM003,3000,28,365,Home,0
...
Feature Engineering
The preprocessing pipeline includes:

Missing value handling: Fills numeric features with mean values
Categorical encoding: Uses LabelEncoder for categorical variables
Feature scaling: StandardScaler for normalization
Feature interactions: Creates multiplicative features from top numeric columns
Model Details
Logistic Regression
Simple baseline model
Fast training and inference
Good for interpretability
Random Forest
Ensemble method with 100 trees
Handles non-linear relationships
Provides feature importance scores
XGBoost
Gradient boosting framework
Superior performance on most datasets
Handles imbalanced data well
Troubleshooting
Model Not Loading
Error: Could not load model files
Solution: Ensure you've run python train_model.py first to generate the model files.

Data Loading Error
Error: No fraud column found in data
Solution: Verify your CSV has a fraud indicator column and update preprocess.py if using a different column name.

Missing Dependencies
ModuleNotFoundError: No module named 'xgboost'
Solution: Run pip install -r requirements.txt

Performance Optimization
Adjust test_size in split_data() for different train/test ratios
Modify XGBoost hyperparameters in train_xgboost() for fine-tuning
Increase Random Forest n_estimators for potentially better performance
Adjust learning_rate and max_depth in XGBoost for optimization
Next Steps
Collect more training data
Implement cross-validation
Add more sophisticated feature engineering
Deploy using Docker or cloud services
Implement monitoring for model performance drift
License
This project is part of the AI & ML module at Vishwakarma College.
