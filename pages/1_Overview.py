import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_combined_grid

# Page Config & CSS for this specific page
st.markdown("""
<style>
    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 40px 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    .hero-banner h1 { color: white !important; font-size: 3rem; margin-bottom: 10px; }
    .hero-banner p { color: #e2e8f0; font-size: 1.2rem; }
    
    /* Status Cards */
    .stat-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 24px;
        text-align: center;
    }
    .stat-value { color: #60a5fa; font-size: 2.5rem; font-weight: 700; }
    .stat-label { color: #9ca3af; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; }
</style>
""", unsafe_allow_html=True)

# --- HERO SECTION ---
st.markdown("""
<div class="hero-banner">
    <h1>🌍 Global Trade Risk Terminal</h1>
    <p>Real-time anomaly detection and Monte Carlo risk simulation for global commodity flows.</p>
</div>
""", unsafe_allow_html=True)

full = load_combined_grid()
if full is None:
    st.error("Data cache not found.")
    st.stop()

# --- DATA PROCESSING ---
recent_data = full[full["period"] >= 202001]
country_totals = recent_data.groupby("reporterDesc")["trade_value"].sum().reset_index()
country_totals["trade_value_b"] = country_totals["trade_value"] / 1e9

# --- CHARTS ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🗺️ Global Trade Volume (Billions USD)")
    fig = px.choropleth(
        country_totals, 
        locations="reporterDesc", 
        locationmode="country names",
        color="trade_value_b", 
        hover_name="reporterDesc", 
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        geo=dict(showframe=False, showcoastlines=True, projection_type='equirectangular')
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📊 Data Coverage")
    
    st.markdown(f"""
    <div class="stat-card" style="margin-bottom: 15px;">
        <div class="stat-value">{len(full):,}</div>
        <div class="stat-label">Total Records Ingested</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-card" style="margin-bottom: 15px;">
        <div class="stat-value">{full["reporterDesc"].nunique()}</div>
        <div class="stat-label">Countries Covered</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-value">{full["commodity_name"].nunique()}</div>
        <div class="stat-label">Commodities Tracked</div>
    </div>
    """, unsafe_allow_html=True)