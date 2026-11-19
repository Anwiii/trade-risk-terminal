import streamlit as st

# We use pure HTML/CSS here for a beautiful hero section
st.markdown("""
<style>
    .hero-section {
        text-align: center;
        padding: 80px 20px;
        background: radial-gradient(circle at 50% 0%, #1e3a8a 0%, #06080e 60%);
        border-radius: 12px;
        margin-bottom: 40px;
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #f9fafb;
        margin-bottom: 15px;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #9ca3af;
        max-width: 800px;
        margin: 0 auto 30px auto;
        line-height: 1.6;
    }
    .feature-card {
        background: #0d1117;
        border: 1px solid #1f2937;
        border-top: 3px solid #3b82f6;
        border-radius: 8px;
        padding: 30px;
        height: 100%;
    }
    .feature-title {
        color: #f9fafb;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .feature-text {
        color: #9ca3af;
        font-size: 0.95rem;
        line-height: 1.6;
    }
</style>

<div class="hero-section">
    <div class="hero-title">Trade Risk Terminal</div>
    <div class="hero-subtitle">
        A Big Data pipeline for detecting, quantifying, and predicting international trade disruptions.
        Powered by Hadoop HDFS, Apache Spark, and Monte Carlo simulation.
    </div>
    <a href="/Overview" target="_self" style="background-color: #3b82f6; color: white; padding: 14px 40px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 1.1rem; display: inline-block;">
        Launch Terminal
    </a>
</div>
""", unsafe_allow_html=True)

# Feature Cards Row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">1. Detect</div>
        <div class="feature-text">
            Identify structural breaks in 5.1 million UN Comtrade records using Robust MAD Z-Scores and CUSUM. 
            Automatically routes missing reporters to mirror statistics.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card" style="border-top-color: #10b981;">
        <div class="feature-title">2. Quantify</div>
        <div class="feature-text">
            Translate raw Z-scores into actionable financial insights. 
            See exactly how much a country's trade volume dropped in Billions of USD compared to expected trends.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card" style="border-top-color: #ef4444;">
        <div class="feature-title">3. Predict</div>
        <div class="feature-text">
            Run 1,000 Monte Carlo simulations with Block Bootstrap sampling. 
            Project forward-looking risk bands (P10-P90) for any hypothetical future disruption.
        </div>
    </div>
    """, unsafe_allow_html=True)