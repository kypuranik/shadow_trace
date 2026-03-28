import streamlit as st

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ui import apply_ui
apply_ui()

from db import fetch_data   
from query_mapper import map_natural_language_to_sql  
st.title("Query Engine")

use_sim = st.checkbox("Use uploaded / simulation data")

user_query = st.text_input("Ask your question")

if st.button("Search"):

    if use_sim and 'sim_data' in st.session_state:
        df = st.session_state.sim_data

        st.info("Using uploaded/simulation data")

        # BASIC NLP FILTER
        if "ddos" in user_query.lower():
            df = df[df["attack_name"].str.contains("ddos", case=False)]

        if "high traffic" in user_query.lower():
            df = df[df["flow_packets_per_sec"] > 4000]

        st.dataframe(df)

    else:
        sql = map_natural_language_to_sql(user_query)
        df = fetch_data(sql)

        st.dataframe(df)