from sqlalchemy import create_engine
import pandas as pd
import streamlit as st

# =========================
# 🔧 DATABASE CONFIG
# =========================
DB_URI = "mysql+pymysql://shadow_user:shadow123@127.0.0.1:3306/shadow_trace"
# ⚠️ Replace:
# root → your username
# password → your MySQL password
# shadow_trace → your database name


# =========================
# ⚡ CREATE ENGINE (CACHED)
# =========================
@st.cache_resource
def get_engine():
    return create_engine(
        DB_URI,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True  # 🔥 avoids stale connections
    )


# =========================
# 📊 FETCH DATA FUNCTION
# =========================
def fetch_data(query, params=None):
    try:
        engine = get_engine()

        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params=params)

        return df

    except Exception as e:
        # 🔥 Show error in Streamlit UI
        st.error(f"Database Error: {e}")
        return None