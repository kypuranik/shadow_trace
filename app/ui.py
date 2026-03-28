import streamlit as st

def apply_ui():
    st.markdown("""
    <style>

    /* ===== BASE ===== */
    .stApp {
        background: linear-gradient(135deg, #1e293b, #334155);
        color: #f1f5f9;  /* FIX: readable text */
        font-family: 'Inter', sans-serif;
    }

    /* ===== HEADINGS FIX ===== */
    h1, h2, h3 {
        color: #ffffff !important;   /* FIX: visible headings */
        font-weight: 600;
    }

    /* ===== TEXT ===== */
    p, label, div {
        color: #f8fafc !important;
    }

    /* ===== GLASS CARD ===== */
    .glass {
        background: rgba(15, 23, 42, 0.7);   /* darker glass */
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
    }

    /* ===== METRICS ===== */
    [data-testid="metric-container"] {
        background: rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 12px;
    }

    /* ===== SIDEBAR FIX ===== */
    section[data-testid="stSidebar"] {
        background: rgba(15,23,42,0.95) !important;
        color: white !important;
    }

    </style>
    """, unsafe_allow_html=True)