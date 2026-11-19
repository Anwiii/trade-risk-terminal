import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_combined_grid

# --- HERO SECTION — plain headline + paragraph, no banner box ---
st.markdown("""
<h1 style="font-size:2.6rem; font-weight:600; letter-spacing:-0.5px; margin-bottom:12px;">
Where global trade starts to break.</h1>
<p style="color:#9ca3af; font-size:1.05rem; max-width:52ch; margin-bottom:44px;">
Real-time anomaly detection and Monte Carlo risk simulation for global commodity flows.</p>
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
    st.markdown("### Global Trade Volume (Billions USD)")
    fig = px.choropleth(
        country_totals, 
        locations="reporterDesc", 
        locationmode="country names",
        color="trade_value_b", 
        hover_name="reporterDesc", 
        color_continuous_scale="Viridis",
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
    st.markdown("### Data Coverage")

    st.markdown(f"""
    <div class="stat-row"><span class="stat-value">{len(full):,}</span><span class="stat-label">Total Records<br>Ingested</span></div>
    <div class="stat-row"><span class="stat-value">{full["reporterDesc"].nunique()}</span><span class="stat-label">Countries<br>Covered</span></div>
    <div class="stat-row"><span class="stat-value">{full["commodity_name"].nunique()}</span><span class="stat-label">Commodities<br>Tracked</span></div>
    """, unsafe_allow_html=True)