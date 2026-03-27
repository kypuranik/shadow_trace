import pandas as pd
import mysql.connector

# connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="shadow_user",
    password="shadow123",
    database="shadow_trace"
)

cursor = conn.cursor()

# load dataset
df = pd.read_csv("../dataset/Friday-WorkingHours-Afternoon-PortScan.pcap_ISCX.csv")
df.columns = df.columns.str.strip()

print(df.columns.tolist())