import streamlit as st
import time

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui import apply_ui
apply_ui()

from db import fetch_data
from query_mapper import map_natural_language_to_sql  

st.title("⚡ Query Engine (Adaptive DB Mode)")

# =========================
# 🧠 QUERY TYPE DETECTION
# =========================
def detect_query_type(user_query):
    q = user_query.lower()

    if any(x in q for x in ["trend", "over time", "distribution", "analytics", "compare"]):
        return "OLAP"

    if any(x in q for x in ["list", "show", "raw", "flows", "records"]):
        return "OLTP"

    return "OLTP"


# =========================
# 📥 INPUT
# =========================
user_query = st.text_input("💬 Ask your question")

if st.button("🔍 Search"):

    if not user_query:
        st.warning("Enter a query")
        st.stop()

    # =========================
    # 🔍 DETECT MODE
    # =========================
    query_type = detect_query_type(user_query)

    # =========================
    # ⚡ ROUTE QUERY
    # =========================
    if query_type == "OLAP":

        st.info("⚡ Using Data Warehouse (OLAP Mode)")

        sql = """
        SELECT 
            a.attack_name,
            t.traffic_category,
            SUM(f.total_flows) AS total
        FROM fact_flows f
        JOIN dim_attack a ON f.attack_key = a.attack_key
        JOIN dim_traffic t ON f.traffic_key = t.traffic_key
        GROUP BY a.attack_name, t.traffic_category
        ORDER BY total DESC
        """

    else:

        st.info("⚡ Using Transactional DB (OLTP Mode)")

        sql = map_natural_language_to_sql(user_query)

        if sql is None:
            st.error("❌ Could not understand query")
            st.stop()

    # =========================
    # ⏱ EXECUTION TIME
    # =========================
    start = time.time()
    df = fetch_data(sql)
    exec_time = time.time() - start

    # =========================
    # 📊 OUTPUT
    # =========================
    st.success(f"✅ Query Mode: {query_type}")
    st.caption(f"⏱ Execution Time: {exec_time:.4f} sec")

    st.dataframe(df)

    # =========================
    # 🧠 EXPLAINABLE PANEL (FRONTEND)
    # =========================
    st.markdown("### 🧠 Query Intelligence")

    if query_type == "OLAP":
        explanation = """
        🔹 This query is routed to the **Data Warehouse (OLAP)**  
        🔹 Uses **star schema (fact + dimensions)**  
        🔹 Optimized for **aggregations & trends**  
        🔹 Faster for large-scale analytical queries  
        """
    else:
        explanation = """
        🔹 This query is routed to the **Transactional Database (OLTP)**  
        🔹 Uses **normalized tables (network_flows)**  
        🔹 Best for **row-level / detailed data**  
        🔹 Suitable for real-time querying  
        """

    st.markdown(f"""
    <div class="glass">
    {explanation}
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # ⚙️ EXPLAIN QUERY PLAN
    # =========================
    if st.checkbox("⚙️ Show Query Execution Plan"):
        try:
            explain_df = fetch_data(f"EXPLAIN {sql}")
            st.dataframe(explain_df)
        except:
            st.warning("Explain plan not available for this query")