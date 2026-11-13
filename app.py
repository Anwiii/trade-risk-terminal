import streamlit as st

# Force sidebar open to avoid the "keyboard_double_" collapse bug
st.set_page_config(page_title="Trade Risk Terminal", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* APPLY FONTS */
    html, body, [class*="css"], .stApp, h1, h2, h3, h4, h5, h6, p, div, span {
        font-family: 'Inter', sans-serif !important;
    }
    .mono { font-family: 'JetBrains Mono', monospace !important; }
    
    /* Dark Theme */
    .stApp { background-color: #06080e; color: #e5e7eb; }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #1f2937; }
    
    /* Navbar */
    .nav-brand { font-size: 1.2rem; font-weight: 700; color: #f9fafb; padding-top: 10px; letter-spacing: -0.5px; }
    
    /* Page Links */
    [data-testid="stPageLink-NavLink"] {
        background-color: transparent;
        border-radius: 6px;
        padding: 8px 16px;
        margin-right: 10px;
    }
    [data-testid="stPageLink-NavLink"]:hover {
        background-color: #1f2937;
    }
    
    /* Sidebar Active State */
    [data-testid="stSidebar"] [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.1) !important;
        border-left: 3px solid #3b82f6 !important;
        font-weight: 600;
    }
    
    /* Headers */
    h1, h2, h3 { color: #f9fafb !important; font-weight: 600 !important; letter-spacing: -0.5px; }
</style>
""", unsafe_allow_html=True)

# 1. DEFINE PAGES
pages = [
    st.Page("pages/1_Overview.py", title="Overview", icon="🏠", default=True),
    st.Page("pages/2_Detector.py", title="Historical Detector", icon="🔍"),
    st.Page("pages/3_Simulator.py", title="Risk Simulator", icon="🛡️"),
    st.Page("pages/4_Performance.py", title="Model Performance", icon="📈"),
]

# 2. TOP BRAND & SEARCH
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown('<div class="nav-brand">📊 Trade Risk Terminal</div>', unsafe_allow_html=True)
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
pg = st.navigation(pages)
pg.run()