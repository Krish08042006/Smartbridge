import numpy as np
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class FraudPredictor:
    def __init__(self, model_path="model/fraud_model.pkl", 
                 scaler_path="model/scaler.pkl",
                 encoder_path="model/label_encoders.pkl"):
        """Load trained model and preprocessing objects"""
        try:
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.label_encoders = joblib.load(encoder_path)
            print("Model and preprocessing objects loaded successfully")
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Could not load model files: {e}")
    
    def preprocess_input(self, data_dict):
        """
        Preprocess input data for prediction
        
        Args:
            data_dict: Dictionary with feature values
            
        Returns:
            Scaled numpy array ready for prediction
        """
        # Inject defaults for columns the model was trained with
        from datetime import datetime
        defaults = {
            'claim_id': 'CLM000001',
            'policy_id': 'POL10002',
            'claim_date': datetime.now().strftime('%Y-%m-%d'),
        }
        full_data = {**defaults, **data_dict}

        # Convert dict to DataFrame
        df = pd.DataFrame([full_data])

        # Ensure only columns the scaler expects are present, in the correct order
        expected_cols = list(self.scaler.feature_names_in_)
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0
        df = df[expected_cols]
        
        # Encode categorical variables (handle unseen labels gracefully)
        for col in df.columns:
            if col in self.label_encoders:
                le = self.label_encoders[col]
                val = str(df[col].iloc[0])
                if val in le.classes_:
                    df[col] = le.transform(df[col].astype(str))
                else:
                    # Use first known class as fallback for unseen values
                    df[col] = 0
        
        # Handle missing values
        df = df.fillna(0)

        # Scale the 12 base features first (matching training pipeline order)
        scaler_cols = list(self.scaler.feature_names_in_)
        df_scaled = pd.DataFrame(
            self.scaler.transform(df[scaler_cols]),
            columns=scaler_cols
        )

        # THEN create interaction features on scaled data (matching create_features from preprocess.py)
        numeric_cols = df_scaled.select_dtypes(include=[np.number]).columns.tolist()
        if len(numeric_cols) > 1:
            for i, col1 in enumerate(numeric_cols[:3]):
                for col2 in numeric_cols[i+1:4]:
                    df_scaled[f'{col1}_x_{col2}'] = df_scaled[col1] * df_scaled[col2]

        # Ensure we have exactly the columns the model expects, in order
        if hasattr(self.model, 'feature_names_in_'):
            model_cols = list(self.model.feature_names_in_)
            for col in model_cols:
                if col not in df_scaled.columns:
                    df_scaled[col] = 0
            df_scaled = df_scaled[model_cols]
        
        return df_scaled.values
    
    def predict(self, data_dict, return_probability=True):
        """
        Predict fraud for single record
        
        Args:
            data_dict: Dictionary with feature values
            return_probability: Whether to return probability score
            
        Returns:
            Prediction (0 or 1) and probability (if return_probability=True)
        """
        try:
            # Preprocess input
            scaled_data = self.preprocess_input(data_dict)
            
            # Make prediction
            prediction = self.model.predict(scaled_data)[0]
            
            if return_probability:
                probability = self.model.predict_proba(scaled_data)[0]
                return {
                    'prediction': int(prediction),
                    'fraud_probability': float(probability[1]),
                    'legitimate_probability': float(probability[0])
                }
            else:
                return {'prediction': int(prediction)}
                
        except Exception as e:
            return {'error': str(e)}
    
    def predict_batch(self, data_list):
        """
        Predict fraud for multiple records
        
        Args:
            data_list: List of dictionaries with feature values
            
        Returns:
            List of predictions with probabilities
        """
        results = []
        for data in data_list:
            result = self.predict(data, return_probability=True)
            results.append(result)
        return results
    
    def get_model_info(self):
        """Get information about loaded model"""
        return {
            'model_type': type(self.model).__name__,
            'model_params': self.model.get_params() if hasattr(self.model, 'get_params') else {}
        }


def load_and_predict(csv_path, model_path="model/fraud_model.pkl"):
    """
    Load data from CSV and make predictions
    
    Args:
        csv_path: Path to CSV file
        model_path: Path to trained model
        
    Returns:
        DataFrame with predictions
    """
    # Load data
    df = pd.read_csv(csv_path)
    
    # Initialize predictor
    predictor = FraudPredictor(model_path=model_path)
    
    # Convert rows to dictionaries and predict
    predictions = []
    for idx, row in df.iterrows():
        data_dict = row.to_dict()
        pred = predictor.predict(data_dict)
        predictions.append(pred)
    
    # Create results dataframe
    results_df = pd.DataFrame(predictions)
    results_df = pd.concat([df, results_df], axis=1)
    
    return results_df


if __name__ == "__main__":
    # Example usage
    predictor = FraudPredictor()
    
    # Example prediction
    sample_data = {
        # Add sample features based on your data structure
        # This is a placeholder - update with actual feature names
    }
    
    # Uncomment to test:
    # result = predictor.predict(sample_data)
    # print(result)
