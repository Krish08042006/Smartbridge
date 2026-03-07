#!/usr/bin/env python
"""
Sample Insurance Data Generator

This script generates sample insurance claims data for testing and development.
You can use this if you don't have your own data yet.

Usage:
    python generate_sample_data.py

This will create data/insurance_data.csv with realistic sample data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_insurance_data(n_records=10000, fraud_rate=0.05):
    """
    Generate realistic insurance claims data
    
    Args:
        n_records: Number of records to generate
        fraud_rate: Percentage of fraud cases (0.05 = 5%)
    
    Returns:
        DataFrame with insurance claims data
    """
    np.random.seed(42)
    
    print(f"Generating {n_records} insurance records with {fraud_rate*100}% fraud rate...")
    
    # Generate base data
    data = {
        'claim_id': [f'CLM{i:06d}' for i in range(1, n_records + 1)],
        'policy_id': [f'POL{np.random.randint(10000, 99999)}' for _ in range(n_records)],
        'claim_date': [datetime.now() - timedelta(days=np.random.randint(0, 365)) 
                       for _ in range(n_records)],
        'claim_amount': np.random.exponential(5000, n_records).astype(int),
        'claimant_age': np.random.normal(45, 15, n_records).astype(int),
        'policy_duration_days': np.random.exponential(500, n_records).astype(int),
        'previous_claims': np.random.poisson(2, n_records),
        'claim_type': np.random.choice(
            ['Auto', 'Medical', 'Property', 'Liability', 'Disability'],
            n_records
        ),
        'policy_type': np.random.choice(
            ['Basic', 'Standard', 'Premium', 'Comprehensive'],
            n_records
        ),
        'state': np.random.choice(
            ['CA', 'TX', 'NY', 'FL', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'],
            n_records
        ),
        'claim_status': np.random.choice(
            ['Approved', 'Denied', 'Under Review', 'Closed'],
            n_records
        ),
        'days_since_policy_start': np.random.exponential(500, n_records).astype(int),
    }
    
    df = pd.DataFrame(data)
    
    # Generate fraud indicator
    # Fraud is more likely with certain patterns
    fraud = np.zeros(n_records)
    fraud_indices = np.random.choice(n_records, int(n_records * fraud_rate), replace=False)
    fraud[fraud_indices] = 1
    
    # Make fraud patterns more realistic (optional tweaks)
    # High amount claims are more likely to be fraud
    high_amount_threshold = df['claim_amount'].quantile(0.90)
    high_amount_indices = df[df['claim_amount'] > high_amount_threshold].index
    for idx in high_amount_indices:
        if np.random.random() < 0.15:  # 15% of high amount claims are fraud
            fraud[idx] = 1
    
    # Multiple claims are more likely to be fraud
    multiple_claims_indices = df[df['previous_claims'] > 5].index
    for idx in multiple_claims_indices:
        if np.random.random() < 0.10:  # 10% of high claim history are fraud
            fraud[idx] = 1
    
    # Ensure fraud rate stays close to target
    current_fraud_rate = fraud.sum() / len(fraud)
    if current_fraud_rate > fraud_rate * 1.5:  # If too many fraud cases
        excess_fraud = int(current_fraud_rate * len(fraud)) - int(fraud_rate * len(fraud))
        fraud_indices = np.where(fraud == 1)[0]
        indices_to_fix = np.random.choice(fraud_indices, excess_fraud, replace=False)
        fraud[indices_to_fix] = 0
    
    df['fraud'] = fraud.astype(int)
    
    # Add some constraints for realism
    df['claimant_age'] = df['claimant_age'].clip(18, 100)
    df['claim_amount'] = df['claim_amount'].clip(100, 500000)
    
    # Convert dates to string
    df['claim_date'] = df['claim_date'].dt.strftime('%Y-%m-%d')
    
    return df

def main():
    """Generate and save sample data"""
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate data
    df = generate_insurance_data(n_records=10000, fraud_rate=0.05)
    
    # Save to CSV
    output_path = os.path.join(data_dir, 'insurance_data.csv')
    df.to_csv(output_path, index=False)
    
    print(f"\n✓ Sample data generated successfully!")
    print(f"  Location: {output_path}")
    print(f"  Records: {len(df):,}")
    print(f"  Columns: {len(df.columns)}")
    print(f"\nData Summary:")
    print(df.head(10))
    print(f"\nClass Distribution:")
    print(f"  Legitimate: {(df['fraud'] == 0).sum():,} ({(df['fraud'] == 0).sum() / len(df) * 100:.1f}%)")
    print(f"  Fraudulent: {(df['fraud'] == 1).sum():,} ({(df['fraud'] == 1).sum() / len(df) * 100:.1f}%)")
    print(f"\nData Info:")
    print(f"  Claim Amount Range: ${df['claim_amount'].min()} - ${df['claim_amount'].max()}")
    print(f"  Age Range: {df['claimant_age'].min()} - {df['claimant_age'].max()}")
    print(f"  Policy Duration: {df['policy_duration_days'].min()} - {df['policy_duration_days'].max()} days")
    
    print(f"\n✓ Ready to train! Run: python src/train_model.py")

if __name__ == "__main__":
    main()
