#!/usr/bin/env python3
"""
============================================================
Script 14: Streamlit Clinical Diagnostic App
============================================================
Interactive web-based diagnostic tool for spine-pelvis biomechanical
evaluation. Run with: streamlit run 14_streamlit_app.py
"""
import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os

st.set_page_config(page_title="Spine-Pelvis Diagnosis", layout="wide", page_icon="🦴")

st.title("🦴 Spine-Pelvis Biomechanical Diagnosis System")
st.markdown("**ML+XAI-Powered Clinical Decision Support** | v1.0")

# Load models
@st.cache_resource
def load_all_models():
    base = "/mnt/agents/output/spine_ml_xai/output/models"
    m = {}
    if os.path.exists(base):
        for f in os.listdir(base):
            if f.endswith('.pkl'):
                m[f.replace('.pkl','')] = pickle.load(open(os.path.join(base,f), 'rb'))
    return m

models = load_all_models()

tab1, tab2 = st.tabs(["B-2C: Normal vs Abnormal", "B-3C: 3-Class Lesion"])

with tab1:
    st.header("Binary Classification")
    c1, c2 = st.columns(2)
    with c1:
        pi = st.slider("Pelvic Incidence", 26.0, 130.0, 60.5)
        pt = st.slider("Pelvic Tilt", -7.0, 50.0, 17.5)
        ll = st.slider("Lumbar Lordosis", 14.0, 126.0, 52.0)
        ss = st.slider("Sacral Slope", 13.0, 122.0, 43.0)
        pr = st.slider("Pelvic Radius", 70.0, 163.0, 118.0)
        sg = st.slider("SpondyGrade", -11.0, 419.0, 26.0)
    with c2:
        if st.button("Predict B-2C"):
            means = [60.50, 17.54, 51.93, 42.95, 117.92, 26.30]
            stds = [17.24, 10.01, 18.55, 13.42, 13.32, 37.56]
            X = (np.array([[pi, pt, ll, ss, pr, sg]]) - means) / stds
            model = models.get('sl_b2', models.get('lr_b2'))
            if model:
                proba = model.predict_proba(X)[0]
                st.metric("Abnormal Probability", f"{proba[0]:.1%}")
                st.metric("Normal Probability", f"{proba[1]:.1%}")
                st.success(f"Prediction: {'Normal' if proba[1] > proba[0] else 'Abnormal'}")

with tab2:
    st.header("3-Class Classification")
    c1, c2 = st.columns(2)
    with c1:
        pi3 = st.slider("PI", 26.0, 130.0, 60.5, key="pi3")
        pt3 = st.slider("PT", -7.0, 50.0, 17.5, key="pt3")
        ll3 = st.slider("LL", 14.0, 126.0, 52.0, key="ll3")
        ss3 = st.slider("SS", 13.0, 122.0, 43.0, key="ss3")
        pr3 = st.slider("PR", 70.0, 163.0, 118.0, key="pr3")
        sg3 = st.slider("SG", -11.0, 419.0, 26.0, key="sg3")
    with c2:
        if st.button("Predict B-3C"):
            means = [60.50, 17.54, 51.93, 42.95, 117.92, 26.30]
            stds = [17.24, 10.01, 18.55, 13.42, 13.32, 37.56]
            X = (np.array([[pi3, pt3, ll3, ss3, pr3, sg3]]) - means) / stds
            model = models.get('sl_b3', models.get('lr_b3'))
            if model:
                proba = model.predict_proba(X)[0]
                labels = ['Disk Hernia', 'Normal', 'Spondylolisthesis']
                for i, lab in enumerate(labels):
                    st.metric(lab, f"{proba[i]:.1%}")
                st.success(f"Prediction: {labels[np.argmax(proba)]}")

st.markdown("---")
st.info("⚠️ **Disclaimer**: This tool is for research and educational purposes only. It does not replace clinical judgment.")
