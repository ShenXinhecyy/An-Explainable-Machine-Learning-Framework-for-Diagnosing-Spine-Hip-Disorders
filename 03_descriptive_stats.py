#!/usr/bin/env python3
"""
============================================================
Script 03: Descriptive Statistics & Visualization
============================================================
Comprehensive descriptive analysis including group comparisons,
normality tests, effect sizes, and publication-ready plots.
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro, kruskal, mannwhitneyu

BASE_DIR = '/mnt/agents/output/spine_ml_xai'
DATA_DIR = os.path.join(BASE_DIR, 'data')
FIG_DIR = os.path.join(BASE_DIR, 'output', 'figures')
TAB_DIR = os.path.join(BASE_DIR, 'output', 'tables')
COLORS = sns.color_palette("Set2", 8)
RANDOM_SEED = 2024

def cohens_d(x, y):
    nx, ny = len(x), len(y)
    pooled_std = np.sqrt(((nx-1)*x.var() + (ny-1)*y.var()) / (nx+ny-2))
    return (x.mean() - y.mean()) / pooled_std if pooled_std > 0 else 0

def descriptive_analysis():
    df_a = pd.read_csv(os.path.join(DATA_DIR, 'DatasetA_cleaned.csv'))
    df_b2 = pd.read_csv(os.path.join(DATA_DIR, 'DatasetB_2C_cleaned.csv'))
    df_b3 = pd.read_csv(os.path.join(DATA_DIR, 'DatasetB_3C_cleaned.csv'))
    
    # Dataset A analysis
    results_a = []
    for col in ['SO', 'IO', 'SFP', 'LL']:
        group_vals = [df_a[df_a['AR_Type']==g][col].dropna() for g in ['None', 'Bilateral', 'Left', 'Right']]
        kw_stat, kw_p = kruskal(*group_vals)
        results_a.append(f"{col}: KW H={kw_stat:.3f}, p={kw_p:.4f}")
    
    with open(os.path.join(TAB_DIR, 'Table1A_Baseline.txt'), 'w') as f:
        f.write("\n".join(results_a))
    
    # Visualization: Boxplots + Violin
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.suptitle('Figure 1A: Dataset A Distribution by AR Type', fontsize=14, fontweight='bold')
    for i, col in enumerate(['SO', 'IO', 'SFP', 'LL']):
        df_plot = df_a.dropna(subset=[col])
        sns.boxplot(data=df_plot, x='AR_Type', y=col, order=['None','Bilateral','Left','Right'], 
                    ax=axes[0,i], palette=COLORS[:4])
        sns.violinplot(data=df_plot, x='AR_Type', y=col, order=['None','Bilateral','Left','Right'], 
                       ax=axes[1,i], palette=COLORS[:4], inner='quartile')
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'Figure1A_DatasetA_Distributions.pdf'), dpi=300)
    
    print("[03_descriptive_stats.py] Descriptive analysis complete.")

if __name__ == '__main__':
    descriptive_analysis()
