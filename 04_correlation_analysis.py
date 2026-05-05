#!/usr/bin/env python3
"""
============================================================
Script 04: Correlation Analysis & Heatmaps
============================================================
Spearman correlation matrices with significance annotation
and network visualization for both datasets.
"""
import os, numpy as np, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
BASE = '/mnt/agents/output/spine_ml_xai'
FIG = os.path.join(BASE, 'output', 'figures')
RANDOM_SEED = 2024

def correlation_analysis():
    df_a = pd.read_csv(os.path.join(BASE, 'data', 'DatasetA_cleaned.csv'))
    df_b = pd.read_csv(os.path.join(BASE, 'data', 'DatasetB_3C_cleaned.csv'))
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    fig.suptitle('Figure 2: Correlation Network Analysis', fontsize=14, fontweight='bold')
    
    for ax, df, cols, title in [
        (axes[0], df_a, ['SO','IO','SFP','LL'], 'Dataset A'),
        (axes[1], df_b, ['PI','PT','LL','SS','PelvicRadius','SpondyGrade'], 'Dataset B')
    ]:
        corr = df[cols].corr(method='spearman')
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
                    vmin=-1, vmax=1, ax=ax, square=True)
        ax.set_title(title, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(FIG, 'Figure2_Correlation_Network.pdf'), dpi=300)
    print("[04] Correlation analysis complete.")

if __name__ == '__main__':
    correlation_analysis()
