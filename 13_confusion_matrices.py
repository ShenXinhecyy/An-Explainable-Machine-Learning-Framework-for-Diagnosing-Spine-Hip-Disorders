#!/usr/bin/env python3
"""
============================================================
Script 13: Confusion Matrices & Diagnostic Accuracy
============================================================
Generate confusion matrices and calculate diagnostic metrics.
"""
import os, numpy as np, pandas as pd, matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

BASE = '/mnt/agents/output/spine_ml_xai'
FIG = os.path.join(BASE, 'output', 'figures')
TAB = os.path.join(BASE, 'output', 'tables')

def diagnostic_metrics(y_true, y_pred, labels):
    """Calculate comprehensive diagnostic metrics"""
    cm = confusion_matrix(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=labels, output_dict=True)
    return cm, pd.DataFrame(report).T

if __name__ == '__main__':
    print("[13] Confusion matrix & diagnostic accuracy script ready.")
