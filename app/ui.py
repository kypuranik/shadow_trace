import streamlit as st

def apply_ui():
    st.markdown("""
    <style>

    /* ===== BASE APP ===== */
    .stApp {
        background: linear-gradient(135deg, #1e293b, #334155);
        color: #f1f5f9;
        font-family: 'Inter', sans-serif;
    }

    /* ===== HEADINGS ===== */
    h1, h2, h3 {
        color: #ffffff !important;
        font-weight: 600;
    }

    /* ===== SAFE TEXT ===== */
    .stMarkdown, .stText, label {
        color: #f8fafc !important;
    }

    /* ===== GLASS CARD ===== */
    .glass {
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(12px);
        border-radius: 14px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    /* ===== BUTTON ===== */
    .stButton>button {
        background: linear-gradient(90deg, #38bdf8, #6366f1);
        color: white;
        border-radius: 10px;
        border: none;
        transition: 0.2s ease;
    }

    .stButton>button:hover {
        transform: scale(1.03);
        opacity: 0.9;
    }

    /* ===== METRICS ===== */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 12px;
    }

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: rgba(15,23,42,0.95) !important;
        color: #e2e8f0 !important;
    }

    /* ===================================================== */
    /* ===== SELECTBOX (DROPDOWN) FIX ===== */
    /* ===================================================== */

    div[data-baseweb="select"] > div {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="menu"] {
        background-color: #1e293b !important;
        border-radius: 10px;
        padding: 5px;
    }

    div[data-baseweb="menu"] div {
        color: #f8fafc !important;
        padding: 10px;
        border-radius: 6px;
    }

    div[data-baseweb="menu"] div:hover {
        background-color: #334155 !important;
        cursor: pointer;
    }

    div[data-baseweb="menu"] div[aria-selected="true"] {
        background-color: #38bdf8 !important;
        color: black !important;
    }

    /* ===================================================== */
    /* ===== CHECKBOX FIX ===== */
    /* ===================================================== */

    div[data-testid="stCheckbox"] {
        color: #f8fafc !important;
    }

    div[data-testid="stCheckbox"] label {
        color: #f8fafc !important;
    }

    div[data-testid="stCheckbox"] label span {
        color: #f8fafc !important;
        font-weight: 500 !important;
    }

    div[data-testid="stCheckbox"] * {
        color: #f8fafc !important;
    }

    div[data-testid="stCheckbox"] input[type="checkbox"] {
        accent-color: #38bdf8;
    }

    /* ===================================================== */
/* ===== ALERT BOXES (FINAL STRONG FIX) ===== */
/* ===================================================== */

    /* Base alert container */
    div[data-testid="stAlert"] {
        border-radius: 12px !important;
        padding: 16px !important;
        font-weight: 500;
    }

    /* INFO (st.info) */
    div[data-testid="stAlert"][role="alert"] {
        background: linear-gradient(135deg, #1e40af, #1d4ed8) !important;
        color: #e0f2fe !important;
        border: none !important;
    }

    /* SUCCESS (st.success) */
    div[data-testid="stAlert"][data-testid="stAlert-success"] {
        background: linear-gradient(135deg, #065f46, #047857) !important;
        color: #d1fae5 !important;
    }

    /* WARNING */
    div[data-testid="stAlert"][data-testid="stAlert-warning"] {
        background: linear-gradient(135deg, #78350f, #92400e) !important;
        color: #fef3c7 !important;
    }

    /* ERROR */
    div[data-testid="stAlert"][data-testid="stAlert-error"] {
        background: linear-gradient(135deg, #7f1d1d, #991b1b) !important;
        color: #fee2e2 !important;
    }

    /* Fix inner text */
    div[data-testid="stAlert"] * {
        color: inherit !important;
    }
                
    /* ===== HIDE STREAMLIT TOP BAR ===== */

    /* Hide top header */
    header {
        visibility: hidden;
    }

    /* Hide hamburger menu (top right ⋮) */
    #MainMenu {
        visibility: hidden;
    }

    /* Hide footer */
    footer {
        visibility: hidden;
    }

    /* Remove top padding gap */
    .block-container {
        padding-top: 1rem !important;
    }            

    </style>
    """, unsafe_allow_html=True)