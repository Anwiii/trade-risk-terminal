import streamlit as st

# 1. PAGE CONFIG (Must be first)
st.set_page_config(page_title="Trade Risk Terminal", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# 2. CUSTOM CSS (The "Website" Look)
st.markdown("""
<style>
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

    /* Hide Streamlit Developer UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Base Theme */
    html, body, [class*="css"], .stApp, h1, h2, h3, h4, h5, h6, p, div, span {
        font-family: 'Inter', sans-serif !important;
    }
    .stApp { background-color: #06080e; color: #e5e7eb; }
    [data-testid="stSidebar"] { background-color: #0d1117; border-right: 1px solid #1f2937; }
    
    /* Typography */
    h1, h2, h3 { color: #f9fafb !important; font-weight: 600 !important; letter-spacing: -0.5px; }
    .mono { font-family: 'JetBrains Mono', monospace !important; }
    
    /* Navigation Bar Styling */
    .nav-brand { font-size: 1.3rem; font-weight: 700; color: #f9fafb; padding-top: 10px; letter-spacing: -0.5px; }
    [data-testid="stPageLink-NavLink"] {
        background-color: transparent;
        border-radius: 6px;
        padding: 8px 16px;
        margin-right: 10px;
        color: #9ca3af !important;
    }
    [data-testid="stPageLink-NavLink"]:hover {
        background-color: #1f2937;
        color: #f9fafb !important;
    }
    [data-testid="stSidebar"] [aria-selected="true"] {
        background-color: rgba(59, 130, 246, 0.1) !important;
        border-left: 3px solid #3b82f6 !important;
        font-weight: 600;
    }

    /* Divider Stat Rows (Editorial Style) */
    .divider-row { display: flex; gap: 30px; margin-bottom: 25px; margin-top: 10px; }
    .divider-item { border-top: 1px solid #1f2937; padding-top: 12px; flex: 1; }
    .divider-label { color: #9ca3af; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; }
    .divider-value { color: #f9fafb; font-size: 1.6rem; font-weight: 600; line-height: 1.2; }
    .divider-value.mono { font-size: 1.5rem; }

    /* Semantic Colors */
    .text-red { color: #ef4444; }
    .text-green { color: #10b981; }
    .text-blue { color: #3b82f6; }
</style>
""", unsafe_allow_html=True)

# 3. DEFINE PAGES
pages = [
    st.Page("pages/0_Home.py", title="Home", default=True),
    st.Page("pages/1_Overview.py", title="Overview"),
    st.Page("pages/2_Detector.py", title="Historical Detector"),
    st.Page("pages/3_Simulator.py", title="Risk Simulator"),
    st.Page("pages/4_Performance.py", title="Performance"),
]

# 4. TOP NAVIGATION BAR
# Only show the top nav bar if the user is NOT on the Home page
if st.session_state.get("current_page") != "Home":
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown('<div class="nav-brand">Trade Risk Terminal</div>', unsafe_allow_html=True)
    with col2:
        search_query = st.text_input("Search", placeholder="Search Country or Commodity (e.g., Russia, Crude_oil)", label_visibility="collapsed")
        if search_query:
            st.session_state["search_query"] = search_query

    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_spacer = st.columns([1.2, 2, 1.5, 1.5, 1.2, 3])
    with nav_col1: st.page_link(pages[0], label="Home")
    with nav_col2: st.page_link(pages[1], label="Overview")
    with nav_col3: st.page_link(pages[2], label="Detector")
    with nav_col4: st.page_link(pages[3], label="Simulator")
    with nav_col5: st.page_link(pages[4], label="Performance")

    st.markdown("<hr style='border-color: #1f2937; margin-top: 10px; margin-bottom: 20px;'>", unsafe_allow_html=True)

# 5. RUN ROUTER
pg = st.navigation(pages)
pg.run()