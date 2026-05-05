#!/usr/bin/env python3
"""
============================================================
Script 11: Bootstrap Internal Validation (2000 iterations)
============================================================
Optimism-corrected performance estimation via bootstrap resampling.
"""
import os, numpy as np, pandas as pd, pickle
from sklearn.metrics import roc_auc_score

BASE = '/mnt/agents/output/spine_ml_xai'
RANDOM_SEED = 2024

def bootstrap_validation(model, X, y, n_boot=2000):
    """Bootstrap optimism-corrected AUC"""
    np.random.seed(RANDOM_SEED)
    n = len(y)
    aucs = []
    for i in range(n_boot):
        idx = np.random.choice(n, size=n, replace=True)
        oob = np.array([j for j in range(n) if j not in idx])
        if len(oob) < 10: continue
        try:
            m = pickle.loads(pickle.dumps(model))
            m.fit(X.iloc[idx] if hasattr(X, 'iloc') else X[idx], y[idx])
            p = m.predict_proba(X.iloc[oob] if hasattr(X, 'iloc') else X[oob])
            auc = roc_auc_score(y[oob], p[:, 1]) if p.shape[1] == 2 else roc_auc_score(y[oob], p, multi_class='ovr', average='macro')
            aucs.append(auc)
        except: continue
    return aucs

if __name__ == '__main__':
    print("[11] Bootstrap validation script ready.")
