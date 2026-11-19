import streamlit as st

# Force sidebar open to avoid the "keyboard_double_" collapse bug
st.set_page_config(page_title="Trade Risk Terminal", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* Hide Streamlit Developer UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* APPLY FONTS */
    html, body, [class*="css"], .stApp, h1, h2, h3, h4, h5, h6, p, div, span {
        font-family: 'Inter', sans-serif !important;
    }
    .mono { font-family: 'JetBrains Mono', monospace !important; }
    
    /* Dark Theme */
    .stApp { background-color: #06080e; color: #e5e7eb; }

    /* Navbar */
    .nav-brand { font-size: 1.2rem; font-weight: 700; color: #f9fafb; padding-top: 10px; letter-spacing: -0.5px; }

    /* Page links — plain text, no pill background */
    [data-testid="stPageLink-NavLink"] p {
        color: #9ca3af; font-size: 14px; font-weight: 500;
        transition: color .15s;
    }
    [data-testid="stPageLink-NavLink"]:hover p { color: #f9fafb; }

    /* Headers */
    h1, h2, h3 { color: #f9fafb !important; font-weight: 600 !important; letter-spacing: -0.5px; }

    /* Shared stat row — used on every page instead of boxed metric cards */
    .stat-row {
        display: flex; align-items: baseline; justify-content: space-between;
        padding: 20px 0; border-top: 1px solid #1f2937;
    }
    .stat-row:last-child { border-bottom: 1px solid #1f2937; }
    .stat-value { color: #e5e7eb; font-size: 1.9rem; font-weight: 600; font-variant-numeric: tabular-nums; }
    .stat-label { color: #7c8699; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; text-align: right; line-height: 1.4; }
    .stat-note { font-size: 0.82rem; margin-top: 4px; font-weight: 500; }
    .stat-note.loss, .stat-note.down { color: #ef4444; }
    .stat-note.gain, .stat-note.up { color: #10b981; }
    .stat-note.neutral { color: #9ca3af; }

    /* Quieter dataframe header — no fill, just a bottom rule */
    [data-testid="stDataFrame"] thead tr th {
        background-color: transparent !important;
        color: #7c8699 !important;
        text-transform: uppercase; letter-spacing: 0.06em; font-size: 0.72rem;
        border-bottom: 1px solid #1f2937 !important;
    }

    /* Shared callout text — replaces the filled/left-border alert boxes */
    .callout { color: #d1d5db; font-size: 0.95rem; line-height: 1.6; margin: 20px 0; }
    .callout strong.loss { color: #ef4444; }
    .callout strong.gain { color: #10b981; }
</style>
""", unsafe_allow_html=True)

# 1. DEFINE PAGES
pages = [
    st.Page("pages/1_Overview.py", title="Overview", default=True),
    st.Page("pages/2_Detector.py", title="Historical Detector"),
    st.Page("pages/3_Simulator.py", title="Risk Simulator"),
    st.Page("pages/4_Performance.py", title="Model Performance"),
]

# 2. TOP BRAND & SEARCH
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown('<div class="nav-brand">Trade Risk Terminal</div>', unsafe_allow_html=True)
with col2:
    search_query = st.text_input("Search", placeholder="Search Country or Commodity (e.g., Russia, Crude_oil)", label_visibility="collapsed")
    if search_query:
        st.session_state["search_query"] = search_query

# 3. TOP NAVIGATION LINKS
nav_col1, nav_col2, nav_col3, nav_col4, nav_spacer = st.columns([1.5, 2, 1.5, 1.5, 5])
with nav_col1: st.page_link(pages[0], label="Overview")
with nav_col2: st.page_link(pages[1], label="Historical Detector")
with nav_col3: st.page_link(pages[2], label="Risk Simulator")
with nav_col4: st.page_link(pages[3], label="Performance")

st.markdown("<hr style='border-color: #1f2937; margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# 4. RUN ROUTER
pg = st.navigation(pages, position="hidden")
pg.run()