import pandas as pd
import numpy as np
import joblib
import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score,
    precision_score, recall_score, f1_score, roc_auc_score, roc_curve
)
import xgboost as xgb
from preprocess import load_data, preprocess_data, split_data, create_features
import warnings
warnings.filterwarnings('ignore')

def get_model_path(filename):
    """Get absolute path to model file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    model_dir = os.path.join(parent_dir, 'model')
    os.makedirs(model_dir, exist_ok=True)
    return os.path.join(model_dir, filename)

class FraudDetectionModel:
    def __init__(self):
        self.models = {}
        self.results = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = None
        self.label_encoders = None
        
    def train_logistic_regression(self, X_train, y_train, X_test, y_test):
        """Train Logistic Regression model"""
        print("\n" + "="*50)
        print("Training Logistic Regression...")
        print("="*50)
        
        model = LogisticRegression(max_iter=1000, random_state=42)
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        self.models['LogisticRegression'] = model
        self.results['LogisticRegression'] = {
            'model': model,
            'predictions': y_pred,
            'probabilities': y_pred_proba,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba)
        }
        
        self._print_metrics('LogisticRegression', self.results['LogisticRegression'])
        return model
    
    def train_random_forest(self, X_train, y_train, X_test, y_test):
        """Train Random Forest model"""
        print("\n" + "="*50)
        print("Training Random Forest...")
        print("="*50)
        
        model = RandomForestClassifier(
            n_estimators=100, random_state=42, n_jobs=-1,
            class_weight='balanced'
        )
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        self.models['RandomForest'] = model
        self.results['RandomForest'] = {
            'model': model,
            'predictions': y_pred,
            'probabilities': y_pred_proba,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'feature_importance': model.feature_importances_
        }
        
        self._print_metrics('RandomForest', self.results['RandomForest'])
        return model
    
    def train_xgboost(self, X_train, y_train, X_test, y_test):
        """Train XGBoost model"""
        print("\n" + "="*50)
        print("Training XGBoost...")
        print("="*50)
        
        model = xgb.XGBClassifier(
            n_estimators=100, max_depth=6, learning_rate=0.1,
            random_state=42, scale_pos_weight=1, eval_metric='logloss'
        )
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        self.models['XGBoost'] = model
        self.results['XGBoost'] = {
            'model': model,
            'predictions': y_pred,
            'probabilities': y_pred_proba,
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_pred_proba),
            'feature_importance': model.feature_importances_
        }
        
        self._print_metrics('XGBoost', self.results['XGBoost'])
        return model
    
    def _print_metrics(self, model_name, metrics):
        """Print model evaluation metrics"""
        print(f"\n{model_name} Results:")
        print(f"  Accuracy:  {metrics['accuracy']:.4f}")
        print(f"  Precision: {metrics['precision']:.4f}")
        print(f"  Recall:    {metrics['recall']:.4f}")
        print(f"  F1-Score:  {metrics['f1']:.4f}")
        print(f"  ROC-AUC:   {metrics['roc_auc']:.4f}")
    
    def get_best_model(self):
        """Select best model based on F1-score"""
        if not self.results:
            raise ValueError("No models trained yet")
        
        best_f1 = -1
        for model_name, metrics in self.results.items():
            if metrics['f1'] > best_f1:
                best_f1 = metrics['f1']
                self.best_model_name = model_name
                self.best_model = self.models[model_name]
        
        print(f"\n{'='*50}")
        print(f"Best Model: {self.best_model_name} (F1-Score: {best_f1:.4f})")
        print(f"{'='*50}")
        
        return self.best_model, self.best_model_name
    
    def save_model(self, model_path=None):
        """Save trained model"""
        if model_path is None:
            model_path = get_model_path("fraud_model.pkl")
        
        if self.best_model is None:
            raise ValueError("No best model selected. Train models first.")
        
        joblib.dump(self.best_model, model_path)
        print(f"\nModel saved to {model_path}")
    
    def save_preprocessing_objects(self, scaler, label_encoders):
        """Save scaler and label encoders"""
        self.scaler = scaler
        self.label_encoders = label_encoders
        scaler_path = get_model_path("scaler.pkl")
        encoder_path = get_model_path("label_encoders.pkl")
        joblib.dump(scaler, scaler_path)
        joblib.dump(label_encoders, encoder_path)
        print("Preprocessing objects saved")


def main():
    """Main training pipeline"""
    print("\n" + "="*60)
    print("Insurance Fraud Detection Model Training Pipeline")
    print("="*60)
    
    # Load and preprocess data
    print("\nLoading and preprocessing data...")
    insurance_df, employee_df, vendor_df = load_data()
    
    if insurance_df is None:
        print("Error: Could not load data")
        return
    
    print(f"Loaded insurance data shape: {insurance_df.shape}")
    print(f"Columns: {list(insurance_df.columns[:10])}...")  # Print first 10 columns
    
    # Preprocess data
    X, y, scaler, label_encoders, fraud_col = preprocess_data(insurance_df)
    print(f"\nPreprocessed data shape: {X.shape}")
    print(f"Target column: {fraud_col}")
    print(f"Class distribution:\n{y.value_counts()}")
    
    # Create additional features
    X = create_features(X)
    print(f"Features after engineering: {X.shape[1]}")
    
    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y)
    print(f"\nTrain set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}")
    
    # Initialize fraud detection model
    fraud_model = FraudDetectionModel()
    fraud_model.save_preprocessing_objects(scaler, label_encoders)
    
    # Train multiple models
    fraud_model.train_logistic_regression(X_train, y_train, X_test, y_test)
    fraud_model.train_random_forest(X_train, y_train, X_test, y_test)
    fraud_model.train_xgboost(X_train, y_train, X_test, y_test)
    
    # Get and save best model
    best_model, best_name = fraud_model.get_best_model()
    fraud_model.save_model()
    
    # Print comparison summary
    print("\n" + "="*60)
    print("Model Comparison Summary")
    print("="*60)
    for model_name, metrics in fraud_model.results.items():
        print(f"\n{model_name}:")
        print(f"  F1-Score: {metrics['f1']:.4f}")
        print(f"  ROC-AUC:  {metrics['roc_auc']:.4f}")
        print(f"  Accuracy: {metrics['accuracy']:.4f}")
    
    print("\n" + "="*60)
    print("Training Complete!")
    print("="*60)
    
    return fraud_model, X_test, y_test

if __name__ == "__main__":
    main()
