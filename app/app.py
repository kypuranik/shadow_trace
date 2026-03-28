import streamlit as st
from ui import apply_ui


# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="ShadowTrace",
    layout="wide"
)

# APPLY GLOBAL UI
apply_ui()

# =========================
# FIX SIDEBAR (IMPORTANT)
# =========================
st.markdown("""
<style>
section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95) !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# MAIN PAGE
# =========================
st.markdown("<h1 style='color:white;'>ShadowTrace</h1>", unsafe_allow_html=True)
st.caption("Network Traffic Intelligence Platform")

st.markdown("""
<div class="glass">
<h3>Overview</h3>
<p>
ShadowTrace provides a unified interface to analyze network traffic,
detect anomalies, and simulate attack scenarios.
</p>
</div>
""", unsafe_allow_html=True)

# =========================
# STATUS
# =========================
st.markdown("### System Status")

col1, col2, col3 = st.columns(3)
col1.metric("System", "Operational")
col2.metric("Detection", "Active")
col3.metric("Security", "Stable")

st.info("Use the sidebar to navigate modules.")