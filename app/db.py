from sqlalchemy import create_engine, text
import pandas as pd
import streamlit as st

# =========================
# 🔧 DATABASE CONFIG
# =========================
DB_URI = "mysql+mysqlconnector://shadow_user:shadow123@localhost:3306/shadow_trace"

# =========================
# ⚡ ENGINE
# =========================
@st.cache_resource
def get_engine():
    return create_engine(
        DB_URI,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True
    )

# =========================
# 🔍 TABLE DETECTION
# =========================
@st.cache_data(ttl=0)
def get_main_table():
    try:
        engine = get_engine()
        df = pd.read_sql("SHOW TABLES", engine)

        if df.empty:
            return None

        col = df.columns[0]
        tables = df[col].tolist()

        if "network_flows" in tables:
            return "network_flows"

        return tables[0]

    except Exception as e:
        st.error(f"Error detecting table: {e}")
        return None

# =========================
# 📊 GENERIC QUERY
# =========================
def fetch_data(query, params=None):
    try:
        engine = get_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text(query), conn, params=params)
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()

# =========================
# 🚀 LOAD DATA (SAFE LIMIT)
# =========================
@st.cache_data(ttl=0)
def load_full_data(limit=200000):
    try:
        engine = get_engine()
        table = get_main_table()

        if table is None:
            return pd.DataFrame()

        query = f"SELECT * FROM {table} LIMIT {limit}"
        df = pd.read_sql(query, engine)

        return df

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# =========================
# 📊 TOTAL COUNT
# =========================
@st.cache_data(ttl=0)
def get_basic_stats():
    try:
        engine = get_engine()
        table = get_main_table()

        if table is None:
            return {}

        query = f"SELECT COUNT(*) as total_rows FROM {table}"
        df = pd.read_sql(query, engine)

        return df.iloc[0].to_dict()

    except Exception as e:
        st.error(f"Stats error: {e}")
        return {}