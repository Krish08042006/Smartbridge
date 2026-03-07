import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
import os
warnings.filterwarnings('ignore')

def get_data_path(filename):
    """Get absolute path to data file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    return os.path.join(parent_dir, 'data', filename)

def load_data():
    """Load and merge insurance, employee, and vendor data"""
    try:
        insurance_path = get_data_path('insurance_data.csv')
        vendor_path = get_data_path('vendor_data.csv')
        employee_path = get_data_path('employee_data.csv')
        
        insurance = pd.read_csv(insurance_path)
        vendor = pd.read_csv(vendor_path) if os.path.exists(vendor_path) else None
        
        # If employee_data exists, load it
        try:
            employee = pd.read_csv(employee_path) if os.path.exists(employee_path) else None
        except FileNotFoundError:
            employee = None
        
        return insurance, employee, vendor
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        return None, None, None

def preprocess_data(insurance_df, employee_df=None, vendor_df=None):
    """
    Preprocess insurance fraud data
    """
    if insurance_df is None:
        raise ValueError("Insurance data is required")
    
    df = insurance_df.copy()
    
    # Handle missing values
    df = df.fillna(df.mean(numeric_only=True))
    
    # Drop rows with critical missing values
    if df.isnull().any().any():
        df = df.dropna()
    
    # Identify fraud column (usually named 'fraud', 'is_fraud', 'FraudIndicator')
    fraud_columns = [col for col in df.columns if 'fraud' in col.lower()]
    if not fraud_columns:
        raise ValueError("No fraud column found in data")
    
    fraud_col = fraud_columns[0]
    
    # Separate features and target
    X = df.drop(columns=[fraud_col])
    y = df[fraud_col]
    
    # Encode categorical variables
    categorical_cols = X.select_dtypes(include=['object']).columns
    label_encoders = {}
    
    for col in categorical_cols:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
    
    # Feature scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)
    
    return X_scaled, y, scaler, label_encoders, fraud_col

def split_data(X, y, test_size=0.2, random_state=42):
    """Split data into training and testing sets"""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test

def create_features(df):
    """Create additional features for fraud detection"""
    df_features = df.copy()
    
    # Example feature engineering (adjust based on actual data)
    numeric_cols = df_features.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 1:
        # Create interaction features
        for i, col1 in enumerate(numeric_cols[:3]):
            for col2 in numeric_cols[i+1:4]:
                df_features[f'{col1}_x_{col2}'] = df_features[col1] * df_features[col2]
    
    return df_features