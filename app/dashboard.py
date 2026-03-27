import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt

print("🚀 Starting dashboard...")

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="shadow_user",
    password="shadow123",
    database="shadow_trace"
)

print(" Connected to database")

# Query using VIEW
query = "SELECT * FROM attack_summary;"
df = pd.read_sql(query, conn)

print(" Data from attack_summary:")
print(df.head())

# Check if data exists
if df.empty:
    print("No data found in attack_summary")
else:
    print("📈 Plotting graph...")

    plt.figure()
    plt.bar(df['attack_id'], df['total_flows'])
    plt.xlabel("Attack ID")
    plt.ylabel("Total Flows")
    plt.title("Attack Distribution")

    plt.show()

print(" Done")