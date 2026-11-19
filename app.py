import streamlit as st

# 1. PAGE CONFIG (Must be first)
st.set_page_config(page_title="Trade Risk Terminal", page_icon="📊", layout="wide")

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
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { 
        background-color: #0d1117; 
        border-right: 1px solid #1f2937; 
    }
    
    /* Typography */
    h1, h2, h3 { color: #f9fafb !important; font-weight: 600 !important; letter-spacing: -0.5px; }
    .mono { font-family: 'JetBrains Mono', monospace !important; }

    /* Style Native Sidebar Nav */
    [data-testid="stSidebarNav"] { padding-top: 20px; }
    [data-testid="stSidebarNav"]::before {
        content: "Trade Risk Terminal";
        display: block;
        color: #f9fafb;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 20px;
        padding-left: 20px;
        letter-spacing: -0.5px;
    }
    [data-testid="stSidebarNav"] a { 
        border-radius: 6px; 
        margin: 0 10px 5px 10px; 
        color: #9ca3af !important; 
    }
    [data-testid="stSidebarNav"] a:hover { 
        background-color: #1f2937; 
        color: #f9fafb !important; 
    }
    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background-color: rgba(59, 130, 246, 0.1) !important;
        border-left: 3px solid #3b82f6 !important;
        color: #f9fafb !important;
        font-weight: 600;
    }

    /* Editorial Stat Rows */
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

# 3. DEFINE PAGES (Streamlit Native Router)
pages = [
    st.Page("pages/0_Home.py", title="Home", default=True),
    st.Page("pages/1_Overview.py", title="Overview"),
    st.Page("pages/2_Detector.py", title="Historical Detector"),
    st.Page("pages/3_Simulator.py", title="Risk Simulator"),
    st.Page("pages/4_Performance.py", title="Performance"),
]

# 4. RUN ROUTER
pg = st.navigation(pages)
pg.run()