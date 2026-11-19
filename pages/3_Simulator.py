import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
from utils import load_combined_grid, get_analog_library
from what_if_simulator import run_scenario
from analyze_v4 import PARTNER_ISO_TO_NAME

st.title("Risk Simulator")

full = load_combined_grid()
if full is None: st.stop()

try:
    analog_df, skipped = get_analog_library()
except Exception as e:
    st.error(f"Library error: {e}")
    st.stop()

with st.sidebar:
    st.markdown("### Settings")
    wi_country = st.selectbox("Country", sorted(full["reporterDesc"].dropna().unique().tolist()), index=0)
    wi_commodity = st.selectbox("Commodity", sorted(full["commodity_name"].dropna().unique().tolist()), index=0)
    wi_date = st.date_input("Hypothetical Start", datetime(2025, 1, 1))
    run_sim = st.button("Run Risk Assessment", type="primary", use_container_width=True)

if run_sim:
    try:
        future_start = wi_date.year * 100 + wi_date.month
        
        projection, warns = run_scenario(
            target_reporter=wi_country, target_commodity=wi_commodity, target_flow="Export",
            hypothetical_start=future_start, 
            source="mirror" if wi_country in PARTNER_ISO_TO_NAME.values() else "reporter",
            analog_df=analog_df 
        )
        
        for w in warns: st.warning(w)
        
        baseline_avg = projection["projected_trend_value"].mean() / 1e9
        median_avg = projection["median_estimate_p50"].mean() / 1e9
        p10_avg = projection["low_estimate_p10"].mean() / 1e9
        loss_pct = ((median_avg - baseline_avg) / baseline_avg) * 100
        worst_case_loss = baseline_avg - p10_avg

        median_note = "loss" if loss_pct < 0 else "gain"
        st.markdown(f"""
        <div class="stat-row">
            <span class="stat-value">${baseline_avg:,.2f}B</span>
            <span class="stat-label">Expected Baseline<br>per month, no disruption</span>
        </div>
        <div class="stat-row">
            <span class="stat-value">${median_avg:,.2f}B</span>
            <span class="stat-label">Median Projection<br><span class="stat-note {median_note}" style="text-transform:none; letter-spacing:normal;">{loss_pct:+.1f}% change</span></span>
        </div>
        <div class="stat-row">
            <span class="stat-value">${p10_avg:,.2f}B</span>
            <span class="stat-label">Worst-Case (P10)<br><span class="stat-note loss" style="text-transform:none; letter-spacing:normal;">${worst_case_loss:,.2f}B lost/month</span></span>
        </div>
        <div class="stat-row">
            <span class="stat-value" style="font-size:1.1rem;">{wi_date.strftime('%b %Y')}</span>
            <span class="stat-label">Scenario<br>{wi_country} · {wi_commodity}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="color:#7c8699; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; margin:28px 0 12px; font-weight:600;">
        Risk Projection &middot; {wi_country} &middot; {wi_commodity} &middot; {wi_date.strftime('%b %Y')}</div>
        """, unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=projection["months_since_hypothetical_start"], y=projection["high_estimate_p90"]/1e9, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
        fig.add_trace(go.Scatter(x=projection["months_since_hypothetical_start"], y=projection["low_estimate_p10"]/1e9, mode='lines', line=dict(width=0), fill='tonexty', fillcolor='rgba(59, 130, 246, 0.12)', name="Best / Worst Range"))
        fig.add_trace(go.Scatter(x=projection["months_since_hypothetical_start"], y=projection["median_estimate_p50"]/1e9, mode='lines', name='Most Likely', line=dict(color='#3b82f6', width=2.5)))
        fig.add_trace(go.Scatter(x=projection["months_since_hypothetical_start"], y=projection["projected_trend_value"]/1e9, mode='lines', name='No Disruption', line=dict(color='#6b7280', width=1.5, dash='dash')))
        
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Months Since Disruption", yaxis_title="Billions USD",
            hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=20, b=0), height=420, font=dict(color='#9ca3af', size=11)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    except ValueError as e:
        st.error(f"Simulation not possible: {e}")
    except Exception as e:
        st.error(f"Error: {type(e).__name__}: {e}")
else:
    st.info("Select a country, commodity, and hypothetical start date in the sidebar to run a risk simulation.")