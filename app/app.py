# app.py
import streamlit as st

st.set_page_config(
    page_title="ShadowTrace | Traffic Analysis",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ ShadowTrace")
st.subheader("Intelligent Network Traffic Analysis System")

st.markdown("""
Welcome to **ShadowTrace** — a next-generation database management and traffic analysis tool.

### 🧠 System Capabilities:
👈 **Use the sidebar to navigate through the modules:**

*   📊 **Dashboard:** Technical analysis, JOIN queries, and traffic filtering.
*   📖 **Learn:** Layman-friendly explanations of cyber attacks and prevention.
*   💬 **Query (NLP):** Ask questions in plain English and get database results.
*   ⚡ **Simulation:** Watch real-time mock traffic flow and attack detection.

---
*Built for robustness. Designed for clarity.*
""")

st.info("👈 Select a page from the sidebar to begin.")