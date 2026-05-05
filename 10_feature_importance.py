#!/usr/bin/env python3
"""
============================================================
Script 10: Feature Importance Comparison
============================================================
Cross-dataset feature importance visualization.
"""
import os, numpy as np, pandas as pd, matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

BASE = '/mnt/agents/output/spine_ml_xai'
FIG = os.path.join(BASE, 'output', 'figures')
COLORS = sns.color_palette("Set2", 8)
RANDOM_SEED = 2024

def feature_importance():
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Figure 6: Feature Importance Comparison', fontsize=14, fontweight='bold')
    
    datasets = [
        ('DatasetA_cleaned.csv', ['SO','IO','SFP','LL'], 'AR_Type', 'A', 0),
        ('DatasetB_2C_cleaned.csv', ['PI','PT','LL','SS','PelvicRadius','SpondyGrade'], 'Class', 'B-2C', 1),
        ('DatasetB_3C_cleaned.csv', ['PI','PT','LL','SS','PelvicRadius','SpondyGrade'], 'Class', 'B-3C', 2)
    ]
    
    for csv, cols, target, label, idx in datasets:
        df = pd.read_csv(os.path.join(BASE, 'data', csv))
        X, y = df[cols], LabelEncoder().fit_transform(df[target])
        rf = RandomForestClassifier(n_estimators=500, random_state=RANDOM_SEED)
        rf.fit(X, y)
        imp = pd.Series(rf.feature_importances_, index=cols).sort_values(ascending=True)
        axes[idx].barh(imp.index, imp.values, color=COLORS[idx])
        axes[idx].set_title(f'{label}', fontweight='bold')
        axes[idx].set_xlabel('Gini Importance')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, 'Figure6_Feature_Importance.pdf'), dpi=300)
    print("[10] Feature importance complete.")

if __name__ == '__main__':
    feature_importance()
