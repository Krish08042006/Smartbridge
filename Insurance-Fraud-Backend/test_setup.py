#!/usr/bin/env python
"""
Test script to validate Insurance Fraud Detection system setup
"""

import os
import sys
import pandas as pd

def check_dependencies():
    """Check if all required packages are installed"""
    print("=" * 60)
    print("CHECKING DEPENDENCIES")
    print("=" * 60)
    
    dependencies = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'xgboost': 'xgboost',
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'joblib': 'joblib'
    }
    
    missing = []
    for module, package in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    else:
        print("\n✓ All dependencies installed!")
        return True

def check_data_files():
    """Check if required data files exist"""
    print("\n" + "=" * 60)
    print("CHECKING DATA FILES")
    print("=" * 60)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, 'data')
    
    required_files = ['insurance_data.csv', 'vendor_data.csv']
    found_files = []
    
    if not os.path.exists(data_path):
        print(f"✗ Data directory not found: {data_path}")
        return False
    
    for file in required_files:
        file_path = os.path.join(data_path, file)
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                print(f"✓ {file} ({len(df)} rows, {len(df.columns)} columns)")
                found_files.append(file)
            except Exception as e:
                print(f"✗ {file} - Error reading: {e}")
        else:
            print(f"⚠ {file} - NOT FOUND")
    
    if 'insurance_data.csv' not in found_files:
        print("\n❌ Required file missing: insurance_data.csv")
        return False
    
    return True

def check_insurance_data():
    """Check insurance data structure"""
    print("\n" + "=" * 60)
    print("CHECKING INSURANCE DATA STRUCTURE")
    print("=" * 60)
    
    try:
        df = pd.read_csv('data/insurance_data.csv')
        
        print(f"Dataset shape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"\nColumns: {', '.join(df.columns[:10])}")
        if len(df.columns) > 10:
            print(f"... and {len(df.columns) - 10} more")
        
        # Check for fraud column
        fraud_cols = [col for col in df.columns if 'fraud' in col.lower()]
        if fraud_cols:
            fraud_col = fraud_cols[0]
            print(f"\n✓ Fraud indicator found: '{fraud_col}'")
            print(f"  Value distribution:\n{df[fraud_col].value_counts()}")
        else:
            print("\n✗ No fraud indicator column found")
            print("  Expected column names: fraud, is_fraud, FraudIndicator, etc.")
            return False
        
        # Check data types
        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        print(f"\nNumeric features: {len(numeric_cols)}")
        print(f"Categorical features: {len(categorical_cols)}")
        
        # Check missing values
        missing = df.isnull().sum()
        if missing.any():
            print(f"\nMissing values detected:")
            print(missing[missing > 0])
        else:
            print("\n✓ No missing values")
        
        return True
        
    except FileNotFoundError:
        print("✗ insurance_data.csv not found in data/ directory")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def check_directory_structure():
    """Check project directory structure"""
    print("\n" + "=" * 60)
    print("CHECKING DIRECTORY STRUCTURE")
    print("=" * 60)
    
    required_dirs = ['src', 'data', 'model']
    required_files = ['app.py', 'requirements.txt', 'README.md']
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # Check directories
    for dir_name in required_dirs:
        dir_path = os.path.join(base_path, dir_name)
        if os.path.exists(dir_path):
            print(f"✓ {dir_name}/")
        else:
            print(f"⚠ {dir_name}/ - NOT FOUND")
    
    # Check files
    for file_name in required_files:
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            print(f"✓ {file_name}")
        else:
            print(f"⚠ {file_name} - NOT FOUND")
    
    # Check src files
    src_path = os.path.join(base_path, 'src')
    if os.path.exists(src_path):
        src_files = ['train_model.py', 'predict.py', 'preprocess.py']
        for file_name in src_files:
            file_path = os.path.join(src_path, file_name)
            if os.path.exists(file_path):
                print(f"✓ src/{file_name}")
            else:
                print(f"✗ src/{file_name} - MISSING")

def main():
    """Run all checks"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " Insurance Fraud Detection - System Check".center(58) + "║")
    print("╚" + "=" * 58 + "╝\n")
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Data Files", check_data_files),
        ("Insurance Data", check_insurance_data)
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            results[check_name] = check_func()
        except Exception as e:
            print(f"\n✗ Error during {check_name}: {e}")
            results[check_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for check_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    if all(results.values()):
        print("\n✓ System ready for training!")
        print("\nNext steps:")
        print("  1. cd src")
        print("  2. python train_model.py")
        print("\nFor API:")
        print("  python app.py")
    else:
        print("\n✗ Please fix the issues above before training")
        print("\nFor help:")
        print("  - Check README.md for documentation")
        print("  - See QUICKSTART.md for quick setup")
    
    print()

if __name__ == "__main__":
    main()
