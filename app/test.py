from sqlalchemy import create_engine
import pandas as pd

engine = create_engine("mysql+pymysql://shadow_user:shadow123@127.0.0.1:3306/shadow_trace")

df = pd.read_sql("SELECT COUNT(*) as cnt FROM network_flows", engine)
print(df)