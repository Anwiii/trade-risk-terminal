import streamlit as st
import pandas as pd

st.title("📈 Model Performance")
st.markdown("Validation metrics for the Robust MAD Z-score and CUSUM detectors.")

st.markdown("### Detector F1-Scores (Test Fold: Russia-Ukraine War)")
data = {
    "Method": ["Standard Z-Score", "Robust MAD Z-Score", "Naive % Change", "Isolation Forest", "CUSUM"],
    "Precision": [0.491, 0.482, 0.337, 0.439, 0.409],
    "Recall": [0.542, 0.618, 0.500, 0.494, 0.902],
    "F1-Score": [0.515, 0.542, 0.403, 0.465, 0.562]
}
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("### Early Warning Results (Walk-Forward)")
st.info("11 of 18 eligible series warned early. Mean lead time: **7.8 months**.")
st.markdown("False Alarm Rate in quiet control period: **19.3%** (627/3,248).")