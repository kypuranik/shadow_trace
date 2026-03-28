import streamlit as st
import pandas as pd
import numpy as np
import time

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui import apply_ui
apply_ui()

st.title("Traffic Simulation & Analysis")

# =========================
# 📂 UPLOAD DATASET
# =========================
st.subheader("Upload Dataset")

uploaded_file = st.file_uploader("Drag and drop CSV file", type=["csv"])

if uploaded_file is not None:
    df_upload = pd.read_csv(uploaded_file)

    st.success("File uploaded successfully")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", len(df_upload))
    col2.metric("Columns", len(df_upload.columns))
    col3.metric("Missing", df_upload.isna().sum().sum())

    # Safe charts
    if "flow_packets_per_sec" in df_upload.columns:
        st.line_chart(df_upload["flow_packets_per_sec"])

    if "attack_name" in df_upload.columns:
        st.bar_chart(df_upload["attack_name"].value_counts())

    # Save uploaded data
    st.session_state.uploaded_data = df_upload


# =========================
# 🧠 SESSION STATE INIT
# =========================
if "running" not in st.session_state:
    st.session_state.running = False

if "tick" not in st.session_state:
    st.session_state.tick = 0

if "sim_data" not in st.session_state:
    st.session_state.sim_data = pd.DataFrame(columns=[
        "time", "flow_packets_per_sec", "attack_name"
    ])

if "show_all_data" not in st.session_state:
    st.session_state.show_all_data = False


# =========================
# 🎮 CONTROLS
# =========================
st.markdown("---")
st.subheader("Live Simulation")

col1, col2 = st.columns(2)

if col1.button("Start Simulation"):
    st.session_state.running = True

if col2.button("Stop Simulation"):
    st.session_state.running = False

speed = st.slider("Speed", 0.1, 2.0, 0.5)


# =========================
# 📊 PLACEHOLDERS
# =========================
metric1 = st.empty()
metric2 = st.empty()
chart = st.empty()
table = st.empty()


# =========================
# ▶️ RUNNING MODE
# =========================
if st.session_state.running:

    packets = np.random.randint(100, 5000)

    if packets > 4000:
        attack = "DDoS"
        status = "High Traffic"
    else:
        attack = "Normal"
        status = "Stable"

    st.session_state.tick += 1

    metric1.metric("Traffic", f"{packets} pkts/s", status)
    metric2.metric("Status", attack)

    new_row = pd.DataFrame([{
        "time": st.session_state.tick,
        "flow_packets_per_sec": packets,
        "attack_name": attack
    }])

    st.session_state.sim_data = pd.concat([
        st.session_state.sim_data,
        new_row
    ]).tail(200).reset_index(drop=True)

    df_data = st.session_state.sim_data.copy()

    # SAFE INDEX HANDLING
    if "time" in df_data.columns:
        df = df_data.set_index("time")
    else:
        df = df_data.reset_index(drop=True)

    # SAFE CHART
    if "flow_packets_per_sec" in df.columns:
        chart.line_chart(df["flow_packets_per_sec"])
    else:
        st.warning("No traffic column found")

    # TABLE
    st.session_state.show_all_data = st.checkbox(
        "Show full data",
        value=st.session_state.show_all_data
    )

    st.caption(f"Total records: {len(st.session_state.sim_data)}")

    if st.session_state.show_all_data:
        table.dataframe(st.session_state.sim_data, height=400)
    else:
        table.dataframe(st.session_state.sim_data.tail(10))

    time.sleep(speed)
    st.rerun()


# =========================
# ⏹️ STOPPED MODE
# =========================
else:
    st.info("Simulation stopped")

    if not st.session_state.sim_data.empty:

        df_data = st.session_state.sim_data.copy()

        if "time" in df_data.columns:
            df = df_data.set_index("time")
        else:
            df = df_data.reset_index(drop=True)

        if "flow_packets_per_sec" in df.columns:
            chart.line_chart(df["flow_packets_per_sec"])
        else:
            st.warning("No traffic column found")

        # TABLE
        st.session_state.show_all_data = st.checkbox(
            "Show full data",
            value=st.session_state.show_all_data
        )

        st.caption(f"Total records: {len(st.session_state.sim_data)}")

        if st.session_state.show_all_data:
            table.dataframe(st.session_state.sim_data, height=400)
        else:
            table.dataframe(st.session_state.sim_data.tail(10))