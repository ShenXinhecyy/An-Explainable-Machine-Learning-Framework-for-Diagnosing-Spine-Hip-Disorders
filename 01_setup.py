#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
============================================================
Script 01: Environment Setup & Configuration
============================================================
Installs packages, sets random seeds, configures plotting theme,
and creates directory structure for the entire analysis pipeline.

Usage:
    python 01_setup.py
"""
import os
import sys
import subprocess

# ============================================================
# Package Installation
# ============================================================
REQUIRED_PACKAGES = [
    'numpy>=1.24', 'pandas>=2.0', 'matplotlib>=3.7', 'seaborn>=0.12',
    'scikit-learn>=1.3', 'xgboost>=2.0', 'shap>=0.42', 'lime>=0.2',
    'scipy>=1.11', 'streamlit>=1.25', 'openpyxl>=3.1'
]

def install_packages():
    """Install required packages via pip"""
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg.split('>=')[0])
        except ImportError:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', pkg])
    print("[01] All packages installed.")

# ============================================================
# Directory Structure
# ============================================================
def create_directories(base_dir='/mnt/agents/output/spine_ml_xai'):
    """Create standardized project directory structure"""
    dirs = [
        'data', 'output/tables', 'output/figures', 'output/models',
        'output/reports', 'code', 'app', 'paper'
    ]
    for d in dirs:
        os.makedirs(os.path.join(base_dir, d), exist_ok=True)
    print(f"[01] Directory structure created under {base_dir}")

# ============================================================
# Global Configuration
# ============================================================
import numpy as np
import matplotlib.pyplot as plt

RANDOM_SEED = 2024
np.random.seed(RANDOM_SEED)

# Publication-ready plotting theme
plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'figure.figsize': (10, 8),
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'legend.fontsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': '#333333',
    'text.color': '#333333',
})

if __name__ == '__main__':
    install_packages()
    create_directories()
    print("[01_setup.py] Environment setup complete.")
