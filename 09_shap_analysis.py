#!/usr/bin/env python3
"""
============================================================
Script 09: SHAP Explainability Analysis
============================================================
Global and local SHAP value analysis for model interpretability.
"""
import os, numpy as np, pandas as pd, matplotlib.pyplot as plt
import shap, pickle, xgboost as xgb
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

BASE = '/mnt/agents/output/spine_ml_xai'
FIG = os.path.join(BASE, 'output', 'figures')
RANDOM_SEED = 2024

def shap_analysis():
    # B-2C
    df = pd.read_csv(os.path.join(BASE, 'data', 'DatasetB_2C_cleaned.csv'))
    X = df[['PI','PT','LL','SS','PelvicRadius','SpondyGrade']]
    y = LabelEncoder().fit_transform(df['Class'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=RANDOM_SEED, stratify=y)
    
    model = xgb.XGBClassifier(n_estimators=300, max_depth=5, eval_metric='logloss', random_state=RANDOM_SEED)
    model.fit(X_train, y_train)
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)
    
    fig, ax = plt.subplots(1, 1, figsize=(8, 6))
    shap.summary_plot(shap_values, X_test, plot_type="bar", show=False, color='#66c2a5')
    plt.title('Dataset B-2C: Mean |SHAP| (XGBoost)', fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, 'Figure5_SHAP_B2C.pdf'), dpi=300)
    
    print("[09] SHAP analysis complete.")

if __name__ == '__main__':
    shap_analysis()
