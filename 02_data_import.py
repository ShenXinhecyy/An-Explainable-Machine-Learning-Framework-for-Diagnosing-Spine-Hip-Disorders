#!/usr/bin/env python3
"""
============================================================
Script 02: Data Import & Quality Control
============================================================
Reads Dataset A (local Excel) and Dataset B (two CSV files),
performs data cleaning, missing value handling, and generates
comprehensive data quality reports.
"""
import os, sys
import numpy as np
import pandas as pd
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

BASE_DIR = '/mnt/agents/output/spine_ml_xai'
DATA_DIR = os.path.join(BASE_DIR, 'data')
REP_DIR = os.path.join(BASE_DIR, 'output', 'reports')
RANDOM_SEED = 2024

def load_dataset_a(path='/mnt/agents/upload/补充测量.xlsx'):
    """Load and clean local acetabular retroversion dataset"""
    df = pd.read_excel(path)
    df.columns = ['PatientID', 'SO', 'IO', 'SFP', 'LL', 'IO_dup', 'CBD', 'AR_Type', 'CrossSign', 'PostWallSign', 'IschialSign']
    df = df.drop(columns=['IO_dup'])
    ar_map = {'无': 'None', '左': 'Left', '右': 'Right', '双': 'Bilateral'}
    df['AR_Type'] = df['AR_Type'].map(ar_map)
    df['LL'] = pd.to_numeric(df['LL'], errors='coerce')
    df = df.dropna(subset=['SO', 'IO', 'SFP', 'AR_Type'])
    return df[['SO', 'IO', 'SFP', 'LL', 'AR_Type']]

def load_dataset_b(path_2c='/mnt/agents/upload/column_2C_weka.csv',
                   path_3c='/mnt/agents/upload/column_3C_weka.csv'):
    """Load public vertebral column datasets"""
    df2 = pd.read_csv(path_2c)
    df2.columns = ['PI', 'PT', 'LL', 'SS', 'PelvicRadius', 'SpondyGrade', 'Class']
    df3 = pd.read_csv(path_3c)
    df3.columns = ['PI', 'PT', 'LL', 'SS', 'PelvicRadius', 'SpondyGrade', 'Class']
    return df2, df3

def generate_quality_report(df_a, df_b2, df_b3):
    """Generate comprehensive data quality report"""
    lines = []
    lines.append("="*60)
    lines.append("DATA QUALITY REPORT")
    lines.append("="*60)
    
    for name, df in [("A (AR)", df_a), ("B-2C", df_b2), ("B-3C", df_b3)]:
        lines.append(f"\n--- Dataset {name} ---")
        lines.append(f"Samples: {len(df)}, Features: {df.shape[1]-1}")
        lines.append(f"Missing: {df.isnull().sum().sum()}")
        if 'AR_Type' in df.columns:
            lines.append(f"Classes: {df['AR_Type'].value_counts().to_dict()}")
        elif 'Class' in df.columns:
            lines.append(f"Classes: {df['Class'].value_counts().to_dict()}")
    
    report = "\n".join(lines)
    with open(os.path.join(REP_DIR, '00_Data_Quality_Report.txt'), 'w') as f:
        f.write(report)
    return report

if __name__ == '__main__':
    df_a = load_dataset_a()
    df_b2, df_b3 = load_dataset_b()
    
    # Save cleaned data
    df_a.to_csv(os.path.join(DATA_DIR, 'DatasetA_cleaned.csv'), index=False)
    df_b2.to_csv(os.path.join(DATA_DIR, 'DatasetB_2C_cleaned.csv'), index=False)
    df_b3.to_csv(os.path.join(DATA_DIR, 'DatasetB_3C_cleaned.csv'), index=False)
    
    report = generate_quality_report(df_a, df_b2, df_b3)
    print(report)
    print("\n[02_data_import.py] Data import complete.")
