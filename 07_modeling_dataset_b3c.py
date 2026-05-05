#!/usr/bin/env python3
"""
============================================================
Script 07: Predictive Modeling - Dataset B-3C (3-Class)
============================================================
"""
import os, pickle, numpy as np, pandas as pd
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, cohen_kappa_score, roc_auc_score, log_loss
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import xgboost as xgb

BASE = '/mnt/agents/output/spine_ml_xai'
RANDOM_SEED = 2024

def main():
    df = pd.read_csv(os.path.join(BASE, 'data', 'DatasetB_3C_cleaned.csv'))
    X = df[['PI','PT','LL','SS','PelvicRadius','SpondyGrade']]
    y = LabelEncoder().fit_transform(df['Class'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=RANDOM_SEED, stratify=y)
    scaler = StandardScaler(); X_train_s = scaler.fit_transform(X_train); X_test_s = scaler.transform(X_test)
    
    results = {}
    models = {
        'LR': LogisticRegression(multi_class='multinomial', max_iter=1000),
        'RF': RandomForestClassifier(n_estimators=500, class_weight='balanced', random_state=RANDOM_SEED),
        'XGB': xgb.XGBClassifier(n_estimators=300, max_depth=5, objective='multi:softprob', num_class=3, eval_metric='mlogloss', random_state=RANDOM_SEED),
        'SVM': SVC(kernel='rbf', probability=True, class_weight='balanced', random_state=RANDOM_SEED),
        'NN': MLPClassifier(hidden_layer_sizes=(64,32), max_iter=2000, early_stopping=True, random_state=RANDOM_SEED)
    }
    for name, model in models.items():
        scaled = name in ['LR', 'SVM', 'NN']
        model.fit(X_train_s if scaled else X_train, y_train)
        X_t = X_test_s if scaled else X_test
        y_pred = model.predict(X_t)
        y_proba = model.predict_proba(X_t)
        results[f'B3_{name}'] = {
            'Accuracy': accuracy_score(y_test, y_pred),
            'Kappa': cohen_kappa_score(y_test, y_pred),
            'AUC': roc_auc_score(y_test, y_proba, multi_class='ovr', average='macro'),
            'LogLoss': log_loss(y_test, y_proba)
        }
        pickle.dump(model, open(os.path.join(BASE, 'output', 'models', f'model_b3_{name}.pkl'), 'wb'))
    
    base = [(n, m) for n, m in [('lr', models['LR']), ('rf', models['RF']), ('xgb', models['XGB']), ('svm', models['SVM'])]]
    sl = StackingClassifier(estimators=base, final_estimator=LogisticRegression(multi_class='multinomial', max_iter=1000), cv=5, stack_method='predict_proba', n_jobs=-1)
    sl.fit(X_train_s, y_train)
    y_pred = sl.predict(X_test_s); y_proba = sl.predict_proba(X_test_s)
    results['B3_SuperLearner'] = {
        'Accuracy': accuracy_score(y_test, y_pred),
        'Kappa': cohen_kappa_score(y_test, y_pred),
        'AUC': roc_auc_score(y_test, y_proba, multi_class='ovr', average='macro'),
        'LogLoss': log_loss(y_test, y_proba)
    }
    pickle.dump(sl, open(os.path.join(BASE, 'output', 'models', 'sl_b3.pkl'), 'wb'))
    pickle.dump(scaler, open(os.path.join(BASE, 'output', 'models', 'scaler_b3.pkl'), 'wb'))
    
    pd.DataFrame(results).T.to_csv(os.path.join(BASE, 'output', 'tables', 'Table4B3_Model_Comparison.csv'))
    print("[07] Dataset B-3C modeling complete.")
    print(pd.DataFrame(results).T)

if __name__ == '__main__':
    main()
