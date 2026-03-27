# pages/3_Query.py
import streamlit as st
import pandas as pd
from db import fetch_data
from query_mapper import map_natural_language_to_sql

st.title("💬 Ask ShadowTrace")
st.markdown("Use natural language to query the database. (NLP → SQL)")

st.info("💡 **Try asking:** 'Show most common attacks', 'Find high traffic flows', or 'Show dos attacks'.")

user_query = st.text_input("What would you like to know about the network?")

if st.button("Search"):
    if user_query:

        sql = map_natural_language_to_sql(user_query)

        # 🔥 HANDLE COLUMN EXPLANATION FIRST
        if isinstance(sql, str) and sql.startswith("EXPLAIN_COLUMN::"):
            col = sql.split("::")[1]

            from query_mapper import column_descriptions

            st.success(f"🧠 {col}: {column_descriptions.get(col, 'No description available')}")
            st.stop()   # VERY IMPORTANT

        # ✅ NORMAL SQL FLOW
        if sql:
            try:
                use_sim = st.checkbox("⚡ Query Simulation Data")
                if use_sim and 'sim_data' in st.session_state:
                    df = st.session_state.sim_data
                else:
                    df = fetch_data(sql)

                if df is not None and not df.empty:

                    st.code(f"Generated SQL:\n{sql}", language="sql")
                    st.dataframe(df, use_container_width=True)

                    # 🧠 Smart explanation
                    if "count" in df.columns:
                        st.success("🧠 Insight: This shows attack frequency distribution.")

                    elif "total_attacks" in df.columns:
                        st.success(f"🧠 Total attacks detected: {df.iloc[0,0]}")

                    else:
                        st.success("🧠 Showing relevant network data.")

                else:
                    st.warning("No results found.")

            except Exception as e:
                st.error(f"Database error: {e}")

        else:
            st.warning("Sorry, I don't understand that query yet.")