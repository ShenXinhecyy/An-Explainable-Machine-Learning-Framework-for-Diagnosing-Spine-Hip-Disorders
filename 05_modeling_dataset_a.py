#!/usr/bin/env python3
"""
============================================================
Script 05: Predictive Modeling - Dataset A (4-Class AR)
============================================================
Logistic Regression, LASSO/EN/Ridge, RF, XGBoost, SVM, NN, KNN,
and Super Learner for acetabular retroversion prediction.
"""
import os, pickle, numpy as np, pandas as pd, matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, cohen_kappa_score, roc_auc_score, log_loss
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import xgboost as xgb

BASE = '/mnt/agents/output/spine_ml_xai'
RANDOM_SEED = 2024

def evaluate_multiclass(model, X_test, y_test, use_scaled=False):
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    kappa = cohen_kappa_score(y_test, y_pred)
    try:
        y_proba = model.predict_proba(X_test)
        auc = roc_auc_score(y_test, y_proba, multi_class='ovr', average='macro')
        ll = log_loss(y_test, y_proba)
    except:
        auc, ll = np.nan, np.nan
    return {'Accuracy': acc, 'Kappa': kappa, 'AUC': auc, 'LogLoss': ll}

def main():
    df = pd.read_csv(os.path.join(BASE, 'data', 'DatasetA_cleaned.csv'))
    X = df[['SO', 'IO', 'SFP', 'LL']].copy()
    y = LabelEncoder().fit_transform(df['AR_Type'])
    X_imp = pd.DataFrame(IterativeImputer(random_state=RANDOM_SEED).fit_transform(X), columns=X.columns)
    X_train, X_test, y_train, y_test = train_test_split(X_imp, y, test_size=0.3, random_state=RANDOM_SEED, stratify=y)
    scaler = StandardScaler(); X_train_s = scaler.fit_transform(X_train); X_test_s = scaler.transform(X_test)
    
    results = {}
    models = {
        'LR': LogisticRegression(multi_class='multinomial', max_iter=1000),
        'LASSO': LogisticRegression(multi_class='multinomial', solver='saga', penalty='l1', C=1.0, max_iter=5000),
        'Ridge': LogisticRegression(multi_class='multinomial', penalty='l2', C=1.0, max_iter=5000),
        'RF': RandomForestClassifier(n_estimators=500, class_weight='balanced', random_state=RANDOM_SEED),
        'XGB': xgb.XGBClassifier(n_estimators=300, max_depth=5, objective='multi:softprob', num_class=4, eval_metric='mlogloss', random_state=RANDOM_SEED),
        'SVM': SVC(kernel='rbf', probability=True, class_weight='balanced', random_state=RANDOM_SEED),
        'NN': MLPClassifier(hidden_layer_sizes=(64,32), max_iter=2000, early_stopping=True, random_state=RANDOM_SEED)
    }
    
    for name, model in models.items():
        scaled = name in ['LR', 'LASSO', 'Ridge', 'SVM', 'NN']
        model.fit(X_train_s if scaled else X_train, y_train)
        results[f'A_{name}'] = evaluate_multiclass(model, X_test_s if scaled else X_test, y_test)
        pickle.dump(model, open(os.path.join(BASE, 'output', 'models', f'model_a_{name}.pkl'), 'wb'))
    
    # Super Learner
    base = [(n, m) for n, m in [('lr', models['LR']), ('rf', models['RF']), ('xgb', models['XGB']), ('svm', models['SVM'])]]
    sl = StackingClassifier(estimators=base, final_estimator=LogisticRegression(multi_class='multinomial', max_iter=1000), cv=5, stack_method='predict_proba', n_jobs=-1)
    sl.fit(X_train_s, y_train)
    results['A_SuperLearner'] = evaluate_multiclass(sl, X_test_s, y_test)
    
    pd.DataFrame(results).T.to_csv(os.path.join(BASE, 'output', 'tables', 'Table4A_Model_Comparison.csv'))
    print("[05] Dataset A modeling complete.")
    print(pd.DataFrame(results).T)

if __name__ == '__main__':
    main()
