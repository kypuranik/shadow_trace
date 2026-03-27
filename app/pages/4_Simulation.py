import streamlit as st
import pandas as pd
import numpy as np
import time

st.title("⚡ Live Traffic Simulation")
st.markdown("Monitoring real-time packet flow and detecting anomalies.")

# =========================
# INIT SESSION STATE
# =========================
if 'sim_data' not in st.session_state:
    st.session_state.sim_data = pd.DataFrame(columns=[
        "time", "flow_packets_per_sec", "attack_name"
    ])

if 'running' not in st.session_state:
    st.session_state.running = False

if 'tick' not in st.session_state:
    st.session_state.tick = 0

# Persistent checkbox state
if "show_all_data" not in st.session_state:
    st.session_state.show_all_data = False

# =========================
# CONTROLS
# =========================
col1, col2 = st.columns(2)

if col1.button("🟢 Start Simulation"):
    st.session_state.running = True

if col2.button("🔴 Stop Simulation"):
    st.session_state.running = False

# Speed control
speed = st.slider("⏱️ Simulation Speed (seconds)", 0.1, 2.0, 0.5)

# Persistent toggle (IMPORTANT)
st.session_state.show_all_data = st.checkbox(
    "📊 Show full simulation data",
    value=st.session_state.show_all_data
)

# =========================
# PLACEHOLDERS
# =========================
metric1 = st.empty()
metric2 = st.empty()
chart = st.empty()
table = st.empty()

# =========================
# RUN SIMULATION
# =========================
if st.session_state.running:

    # Generate random traffic
    packets = np.random.randint(100, 5000)

    # Attack logic
    if packets > 4000:
        attack = "DDoS"
        status = "⚠️ DDoS WARNING"
        color = "inverse"
    else:
        attack = "Normal"
        status = "Normal"
        color = "normal"

    # Increment time
    st.session_state.tick += 1

    # =========================
    # METRICS
    # =========================
    metric1.metric(
        "Current Traffic",
        f"{packets} pkts/s",
        delta=status,
        delta_color=color
    )

    metric2.metric(
        "System Status",
        "Under Attack" if attack != "Normal" else "Monitoring Active"
    )

    # =========================
    # STORE DATA
    # =========================
    new_row = pd.DataFrame([{
        "time": st.session_state.tick,
        "flow_packets_per_sec": packets,
        "attack_name": attack
    }])

    st.session_state.sim_data = pd.concat([
        st.session_state.sim_data,
        new_row
    ]).tail(200).reset_index(drop=True)

    # =========================
    # GRAPH
    # =========================
    df = st.session_state.sim_data.set_index("time")
    chart.line_chart(df["flow_packets_per_sec"])

    # =========================
    # TABLE
    # =========================
    st.caption(f"Showing {len(st.session_state.sim_data)} records")

    if st.session_state.show_all_data:
        table.dataframe(
            st.session_state.sim_data,
            use_container_width=True,
            height=400  # enables scrolling
        )
    else:
        table.dataframe(
            st.session_state.sim_data.tail(10),
            use_container_width=True,
            hide_index=True
        )

    # Loop control
    time.sleep(speed)
    st.rerun()

# =========================
# WHEN STOPPED
# =========================
else:
    st.info("Click Start Simulation")

    if not st.session_state.sim_data.empty:
        df = st.session_state.sim_data.set_index("time")
        chart.line_chart(df["flow_packets_per_sec"])

        st.caption(f"Showing {len(st.session_state.sim_data)} records")

        if st.session_state.show_all_data:
            table.dataframe(
                st.session_state.sim_data,
                use_container_width=True,
                height=400
            )
        else:
            table.dataframe(
                st.session_state.sim_data.tail(10),
                use_container_width=True,
                hide_index=True
            )