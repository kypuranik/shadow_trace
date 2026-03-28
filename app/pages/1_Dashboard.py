import streamlit as st
import pandas as pd
import plotly.express as px
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui import apply_ui
from db import load_full_data, get_main_table

apply_ui()

st.title("📊 ShadowTrace — Intelligent Traffic Analysis")

# =========================
# 🔄 REFRESH
# =========================
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.rerun()

# =========================
# ⚡ DATA SOURCE SWITCH (FINAL LOGIC)
# =========================
has_sim = "sim_data" in st.session_state and not st.session_state.sim_data.empty
has_upload = "uploaded_data" in st.session_state and not st.session_state.uploaded_data.empty

use_simulation = False

if has_sim or has_upload:
    use_simulation = st.checkbox(
        "⚡ Use Simulation / Uploaded Data",
        help="Switch between database and simulation/uploaded data"
    )

# =========================
# 📂 LOAD DATA
# =========================
table_name = get_main_table()

if table_name is None:
    st.error("❌ No table found in database")
    st.stop()

if use_simulation:

    if has_upload:
        df = st.session_state.uploaded_data.copy()
        st.success("🟢 Using Uploaded Dataset")

    elif has_sim:
        df = st.session_state.sim_data.copy()
        st.success("🟢 Using Live Simulation Data")

    else:
        df = load_full_data()
        st.info("🔵 Fallback to Database")

else:
    df = load_full_data()
    st.info(f"🔵 Using Database Table: {table_name}")

# =========================
# ❌ EMPTY CHECK
# =========================
if df is None or df.empty:
    st.error("❌ No data available")
    st.stop()

# =========================
# 🔍 COLUMN DETECTION
# =========================
traffic_col = None
attack_col = None

for col in df.columns:
    c = col.lower()

    if "packet" in c or "traffic" in c:
        traffic_col = col

    if "label" in c or "attack" in c:
        attack_col = col

if traffic_col is None:
    st.error("❌ No traffic column found")
    st.write(df.columns.tolist())
    st.stop()

# =========================
# 🎚️ FILTER
# =========================
threshold = st.slider(
    "🚦 Traffic Threshold",
    0,
    int(df[traffic_col].max()),
    int(df[traffic_col].mean())
)

df_filtered = df[df[traffic_col] > threshold]

# =========================
# 📊 METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("📦 Total Flows", f"{len(df):,}")
col2.metric("🔥 High Traffic Flows", len(df_filtered))

top_attack = (
    df_filtered[attack_col].mode()[0]
    if attack_col and not df_filtered.empty
    else "N/A"
)

col3.metric("⚠️ Dominant Attack", top_attack)

# =========================
# 📊 ATTACK DISTRIBUTION (LOG SCALE)
# =========================
st.subheader("🚨 Attack Distribution (Log Scale - Balanced View)")

if attack_col and not df_filtered.empty:

    attack_counts = df_filtered[attack_col].value_counts().reset_index()
    attack_counts.columns = ["Attack Type", "Count"]

    # BAR CHART
    fig = px.bar(
        attack_counts,
        x="Attack Type",
        y="Count",
        color="Count"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),

        title=dict(
            text="Attack Distribution (Log Scale)",
            font=dict(size=20, color="#ffffff"),
            x=0.02
        ),

        xaxis=dict(
            title="Attack Type",
            title_font=dict(color="#e2e8f0"),
            tickfont=dict(color="#cbd5f5"),
            gridcolor="rgba(255,255,255,0.1)"
        ),

        yaxis=dict(
            title="Count (Log Scale)",
            title_font=dict(color="#e2e8f0"),
            tickfont=dict(color="#cbd5f5"),
            gridcolor="rgba(255,255,255,0.1)",
            type="log"
        ),

        legend=dict(font=dict(color="#f8fafc")),
        margin=dict(t=60, l=20, r=20, b=20)
    )

    st.plotly_chart(fig, use_container_width=True)

    # PIE CHART
    top_attacks = attack_counts.head(6)

    fig2 = px.pie(
        top_attacks,
        names="Attack Type",
        values="Count"
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f8fafc"),

        title=dict(
            text="Top Attack Share",
            font=dict(size=20, color="#ffffff"),
            x=0.02
        ),

        legend=dict(font=dict(color="#f8fafc"))
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info("⚖️ Dataset is highly imbalanced — log scale used to reveal smaller attack patterns")

else:
    st.info("No attack data available")

# =========================
# 📋 SUMMARY
# =========================
st.subheader("📋 Raw Data Summary")

if attack_col:
    summary = df.groupby(attack_col).agg({
        attack_col: "count",
        traffic_col: "mean"
    }).rename(columns={
        attack_col: "Count",
        traffic_col: "Avg Traffic (Packets/sec)"
    })

    st.dataframe(summary)

# =========================
# 🧠 INSIGHT
# =========================
st.markdown("### 🧠 Key Insight")

st.success(
    f"{top_attack} is the most dominant attack above threshold {int(threshold)} packets/sec."
)