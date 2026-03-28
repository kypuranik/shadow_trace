import streamlit as st
import pandas as pd
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui import apply_ui
from db import load_full_data, get_main_table, get_basic_stats

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
# ⚡ DATA SOURCE SWITCH
# =========================
use_simulation = False

if "sim_data" in st.session_state and not st.session_state.sim_data.empty:
    use_simulation = st.checkbox("⚡ Use Simulation / Uploaded Data")

# =========================
# 📂 LOAD DATA
# =========================
table_name = get_main_table()

if table_name is None:
    st.error("❌ No table found in database")
    st.stop()

if use_simulation:
    df = st.session_state.sim_data.copy()
    st.success("🟢 Using Simulation Data")
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
# 📊 TOTAL ROWS
# =========================
if use_simulation:
    total_rows = len(df)
else:
    stats = get_basic_stats()
    total_rows = stats.get("total_rows", len(df))

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
# 🎚️ SCALED SLIDER
# =========================
actual_max = int(df[traffic_col].max())
UI_MAX = 200000

scale = UI_MAX / actual_max if actual_max > 0 else 1

threshold_ui = st.slider(
    "🚦 Filter by Traffic Intensity (Packets/sec)",
    0,
    UI_MAX,
    int(UI_MAX * 0.3)
)

threshold = threshold_ui / scale

st.caption(f"Actual threshold: {int(threshold)} packets/sec")

# =========================
# 🔎 FILTER
# =========================
df_filtered = df[df[traffic_col] > threshold]

# =========================
# 📊 METRICS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("📦 Total Flows", f"{total_rows:,}")
col2.metric("🔥 High Traffic Flows", len(df_filtered))

if attack_col and not df_filtered.empty:
    top_attack = df_filtered[attack_col].mode()[0]
else:
    top_attack = "N/A"

col3.metric("⚠️ Dominant Attack", top_attack)


# =========================
# 📊 ATTACK DISTRIBUTION (TOP 5)
# =========================
st.subheader("🚨 Attack Distribution (Filtered by Traffic)")

if attack_col and not df_filtered.empty:

    attack_counts = df_filtered[attack_col].value_counts()

    # take top 5 attacks
    top_n = attack_counts.head(5)

    # fallback if only 1 category
    if len(top_n) <= 1:
        st.warning("⚠️ Filter too strict — showing overall distribution")
        attack_counts = df[attack_col].value_counts().head(5)
        top_n = attack_counts

    st.bar_chart(top_n)

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
# 🧠 INSIGHT BOX
# =========================
st.markdown("### 🧠 Key Insight")

st.success(
    f"{top_attack} is the most dominant attack when traffic exceeds {int(threshold)} packets/sec."
)