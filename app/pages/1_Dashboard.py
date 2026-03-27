import streamlit as st
import pandas as pd
import plotly.express as px
from db import fetch_data

st.set_page_config(page_title="ShadowTrace Dashboard", layout="wide")

# =========================
# 🧠 TITLE
# =========================
st.title("📊 ShadowTrace — Intelligent Traffic Analysis")
st.markdown("Analyze network behavior and detect high-intensity attack patterns.")

# =========================
# 🎛️ FILTER
# =========================
threshold = st.slider(
    "🚦 Filter by Traffic Intensity (Packets/sec)",
    min_value=0,
    max_value=200000,   # 🔥 LIMITED for stability
    value=5000,
    step=1000
)

# =========================
# 📊 FETCH MAIN DATA
# =========================
query = f"""
SELECT a.attack_name, COUNT(*) as occurrences,
       AVG(f.flow_packets_per_sec) as avg_traffic
FROM network_flows f
JOIN attack_types a ON f.attack_id = a.attack_id
WHERE f.flow_packets_per_sec >= {threshold}
GROUP BY a.attack_name
ORDER BY occurrences DESC;
"""

use_sim = st.checkbox("⚡ Use Live Simulation Data")

if use_sim and 'sim_data' in st.session_state:
    df = st.session_state.sim_data

    # convert to grouped format
    df = df.groupby("attack_name").agg(
        occurrences=("attack_name", "count"),
        avg_traffic=("flow_packets_per_sec", "mean")
    ).reset_index()
else:
    df = fetch_data(query)

# =========================
# 🧱 KPI CARDS (SAFE)
# =========================
col1, col2, col3 = st.columns(3)

# Total flows
total_df = fetch_data("SELECT COUNT(*) as count FROM network_flows")
if total_df is not None and not total_df.empty:
    total_flows = int(total_df.iloc[0]["count"])
else:
    total_flows = 0

# High traffic flows
high_df = fetch_data(f"""
SELECT COUNT(*) as count FROM network_flows 
WHERE flow_packets_per_sec >= {threshold}
""")

if high_df is not None and not high_df.empty:
    high_flows = int(high_df.iloc[0]["count"])
else:
    high_flows = 0

# Top attack
if df is not None and not df.empty:
    top_attack = df.iloc[0]["attack_name"]
else:
    top_attack = "N/A"

col1.metric("📦 Total Flows", f"{total_flows:,}")
col2.metric("🔥 High Traffic Flows", f"{high_flows:,}")
col3.metric("⚠️ Dominant Attack", top_attack)

st.markdown("---")

# =========================
# 📊 CHART + DATA
# =========================
if df is not None and not df.empty:

    # 🔥 INTERACTIVE CHART
    fig = px.bar(
        df,
        x="attack_name",
        y="occurrences",
        color="avg_traffic",
        color_continuous_scale="reds",
        title="🚨 Attack Distribution (Filtered by Traffic)",
        labels={
            "attack_name": "Attack Type",
            "occurrences": "Number of Occurrences",
            "avg_traffic": "Avg Traffic (Packets/sec)"
        }
    )

    fig.update_layout(
        xaxis_tickangle=-45,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # 🧠 INSIGHT BOX
    # =========================
    top_attack = df.iloc[0]["attack_name"]

    st.success(f"""
🚨 **Key Insight**

**{top_attack}** is the most dominant attack when traffic exceeds **{threshold} packets/sec**.

This indicates high-intensity network activity that may require monitoring.
""")

    # =========================
    # 📋 TABLE
    # =========================
    st.subheader("📋 Raw Data Summary")

    df_display = df.copy()
    df_display.rename(columns={
        "occurrences": "Count",
        "avg_traffic": "Avg Traffic (Packets/sec)"
    }, inplace=True)

    st.dataframe(df_display, use_container_width=True)

    # =========================
    # 🧠 EXPLANATION PANEL
    # =========================
    st.info(f"""
📊 **Understanding This Dashboard**

- Showing traffic where **packets/sec ≥ {threshold}**
- Higher values indicate **more intense traffic**
- Color intensity shows **traffic severity**

👉 Helps detect:
- DDoS attacks  
- Bot traffic  
- Network spikes  
""")

    # =========================
    # ⚠️ WHY IT MATTERS
    # =========================
    st.warning("""
⚠️ **Why This Matters**

High packet rates may indicate:
- Distributed Denial of Service (DDoS)
- Bot traffic
- Network flooding

Monitoring helps prevent:
- Server crashes  
- Performance degradation  
- Security risks  
""")

else:
    st.warning("No data found for selected traffic level. Try lowering the filter.")