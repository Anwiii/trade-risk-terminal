import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from utils import load_combined_grid
from analyze_v4 import build_fold, period_str

st.title("Historical Detector")

full = load_combined_grid()
if full is None: st.stop()

search_val = st.session_state.get("search_query", "")

with st.sidebar:
    st.markdown("### Settings")
    event_choice = st.selectbox("Event", ["Russia-Ukraine War (Feb 2022)", "COVID-19 Pandemic (Mar 2020)"])
    event_date_str = "2022-02" if "War" in event_choice else "2020-03"
    ey, em = map(int, event_date_str.split("-"))
    event_period = ey * 100 + em

    country_options = ["All"] + sorted(full["reporterDesc"].dropna().unique().tolist())
    default_idx = 0
    if search_val:
        for i, c in enumerate(country_options):
            if search_val.lower() in c.lower():
                default_idx = i
                break
    
    country_val = st.selectbox("Focus Country", country_options, index=default_idx)
    run = st.button("Run Analysis", type="primary", use_container_width=True)

if run:
    if country_val == "All":
        focus_countries = ["Russian Federation", "Belarus", "Ukraine", "Germany", "China", "Saudi Arabia", "United States", "Kazakhstan", "Argentina"]
        filtered = full[full["reporterDesc"].isin(focus_countries)]
    else:
        filtered = full[full["reporterDesc"] == country_val]
    
    with st.spinner("Scanning series..."):
        final = build_fold(filtered, ["reporterISO", "reporterDesc", "cmdCode", "commodity_name", "flowDesc"], event_period)

    if final is not None:
        final["is_anomaly"] = (final["z_robust"].abs() > 2.0) & (~final["is_baseline"])
        eval_only = final[~final["is_baseline"]].copy()
        
        eval_only["actual_usd"] = np.expm1(eval_only["log_value"])
        eval_only["expected_usd"] = np.expm1(eval_only["trend_pred"])
        eval_only["diff_usd"] = eval_only["actual_usd"] - eval_only["expected_usd"]
        eval_only["pct_dev"] = (eval_only["diff_usd"] / eval_only["expected_usd"].replace(0, np.nan)) * 100
        
        drops = eval_only[(eval_only["is_anomaly"] == True) & (eval_only["diff_usd"] < 0)]
        
        if len(drops) > 0:
            worst_drop_row = drops.loc[drops["pct_dev"].idxmin()]
            top_series = final[(final["reporterDesc"] == worst_drop_row["reporterDesc"]) & 
                               (final["commodity_name"] == worst_drop_row["commodity_name"]) & 
                               (final["flowDesc"] == worst_drop_row["flowDesc"])].sort_values("period")
            
            max_actual_date = top_series[top_series["is_observed"]]["period"].max()
            top_series.loc[top_series["period"] > max_actual_date, "trend_pred"] = np.nan

            window_start = event_period
            window_end = (ey + 1) * 100 + em
            if window_end > max_actual_date:
                window_end = max_actual_date 
            
            window_data = top_series[(top_series["period"] >= window_start) & (top_series["period"] <= window_end)]
            window_data = window_data[window_data["is_anomaly"] == True]
            
            deficit = 0
            impact_b = 0
            pct_change = 0
            direction = "changed"
            
            if len(window_data) > 0:
                actual_window = np.expm1(window_data["log_value"]).sum()
                expected_window = np.expm1(window_data["trend_pred"]).sum()
                deficit = expected_window - actual_window
                impact_b = abs(deficit) / 1e9
                direction = "collapsed" if deficit > 0 else "spiked"
                pct_change = (deficit / expected_window) * 100 if expected_window > 0 else 0

            # FIXED GRAMMAR LOGIC
            note_class = "text-red" if deficit > 0 else "text-green"
            trend_word = "below" if deficit > 0 else "above"
            effect_word = "lost" if deficit > 0 else "unexpected"
            
            # Styled Stat Rows using custom CSS classes from app.py
            st.markdown(f"""
            <div class="divider-row">
                <div class="divider-item">
                    <div class="divider-label">Worst Hit Series</div>
                    <div class="divider-value">{worst_drop_row['commodity_name']}</div>
                    <div style="color: #9ca3af; font-size: 0.85rem;">{worst_drop_row['reporterDesc']}</div>
                </div>
                <div class="divider-item">
                    <div class="divider-label">Volume Change</div>
                    <div class="divider-value {note_class}">{abs(pct_change):.1f}%</div>
                    <div style="color: #9ca3af; font-size: 0.85rem;">{direction}</div>
                </div>
                <div class="divider-item">
                    <div class="divider-label">Estimated Impact</div>
                    <div class="divider-value mono {note_class}">${impact_b:,.2f}B</div>
                    <div style="color: #9ca3af; font-size: 0.85rem;">{effect_word} volume</div>
                </div>
                <div class="divider-item">
                    <div class="divider-label">Analysis Window</div>
                    <div class="divider-value" style="font-size: 1.1rem; padding-top: 5px;">{period_str(window_start)} to {period_str(window_end)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # FIXED CALLOUT SENTENCE
            st.markdown(f"""
            <p style="font-size: 1rem; margin-bottom: 25px; line-height: 1.6; color: #d1d5db;">
                <strong>{worst_drop_row['reporterDesc']}</strong> {worst_drop_row['commodity_name']} {worst_drop_row['flowDesc']}s {direction} by 
                <strong class="{note_class}">{abs(pct_change):.1f}%</strong> {trend_word} expected trend, resulting in 
                <strong class="{note_class}">${impact_b:,.2f}B</strong> in {effect_word} trade volume.
            </p>
            """, unsafe_allow_html=True)

            # CHARTS
            series_plot = top_series.copy()
            series_plot["date"] = series_plot["period"].apply(lambda p: datetime(int(p) // 100, int(p) % 100, 1))
            actual_b = np.expm1(series_plot["log_value"]) / 1e9
            expected_b = np.expm1(series_plot["trend_pred"]) / 1e9
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=series_plot["date"], y=actual_b, mode='lines', name='Actual Trade', line=dict(color='#3b82f6', width=2.5)))
            fig.add_trace(go.Scatter(x=series_plot["date"], y=expected_b, mode='lines', name='Expected Trend', line=dict(color='#6b7280', width=1.5, dash='dash')))
            fig.add_trace(go.Scatter(x=series_plot["date"], y=expected_b, fill='tonexty', fillcolor='rgba(239, 68, 68, 0.15)', mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
            fig.add_vline(x=datetime(ey, em, 1), line_dash="dot", line_color="#6b7280", line_width=2)
            
            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Billions USD", hovermode="x unified",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(l=0, r=0, t=30, b=0), height=400, font=dict(color='#9ca3af', size=11)
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown('<div style="color:#7c8699; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.08em; margin:28px 0 12px; font-weight:600;">Monthly Deviation from Trend</div>', unsafe_allow_html=True)
            series_plot["diff_b"] = actual_b - expected_b
            colors = ['#ef4444' if x < 0 else '#10b981' for x in series_plot["diff_b"]]
            
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=series_plot["date"], y=series_plot["diff_b"], marker_color=colors, marker_line_width=0))
            fig2.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Billions USD", margin=dict(l=0, r=0, t=10, b=0), height=200,
                font=dict(color='#9ca3af', size=11), showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)
else:
    st.markdown("""
    <p style="color:#9ca3af; font-size:1.05rem; margin-top:24px;">
    Select an event and country in the sidebar, then click <strong>Run Analysis</strong>.</p>
    """, unsafe_allow_html=True)