import streamlit as st
import pandas as pd

st.title("Model Performance")
st.markdown('<p style="color:#9ca3af; font-size:1.05rem; margin-bottom:36px;">Validation metrics for the Robust MAD Z-score and CUSUM detectors.</p>', unsafe_allow_html=True)

st.markdown('<div style="color:#7c8699; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:12px; font-weight:600;">Detector F1-Scores (Test Fold: Russia-Ukraine War)</div>', unsafe_allow_html=True)
data = {
    "Method": ["Standard Z-Score", "Robust MAD Z-Score", "Naive % Change", "Isolation Forest", "CUSUM"],
    "Precision": [0.491, 0.482, 0.337, 0.439, 0.409],
    "Recall": [0.542, 0.618, 0.500, 0.494, 0.902],
    "F1-Score": [0.515, 0.542, 0.403, 0.465, 0.562]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown('<div style="color:#7c8699; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; margin:36px 0 12px; font-weight:600;">Early Warning Results (Walk-Forward)</div>', unsafe_allow_html=True)
st.markdown("""
<p class="callout"><strong>11 of 18</strong> eligible series warned early. Mean lead time: <strong>7.8 months</strong>.<br>
False alarm rate in the quiet control period: <strong class="loss">19.3%</strong> (627/3,248).</p>
""", unsafe_allow_html=True)