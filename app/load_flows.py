import pandas as pd
import mysql.connector
import numpy as np
import os

conn = mysql.connector.connect(
    host="localhost",
    user="shadow_user",
    password="shadow123",
    database="shadow_trace"
)

cursor = conn.cursor()

dataset_folder = "../dataset"

for file in os.listdir(dataset_folder):

    if file.endswith(".csv"):

        print("Processing:", file)

        df = pd.read_csv(os.path.join(dataset_folder, file))
        df.columns = df.columns.str.strip()

        df = df[[
            "Flow Duration",
            "Total Fwd Packets",
            "Total Backward Packets",
            "Flow Bytes/s",
            "Flow Packets/s",
            "Packet Length Mean",
            "Packet Length Std",
            "SYN Flag Count",
            "ACK Flag Count",
            "Down/Up Ratio",
            "Active Mean",
            "Label"
        ]]

        df.columns = [
            "flow_duration",
            "total_fwd_packets",
            "total_bwd_packets",
            "flow_bytes_per_sec",
            "flow_packets_per_sec",
            "packet_length_mean",
            "packet_length_std",
            "syn_flag_count",
            "ack_flag_count",
            "down_up_ratio",
            "active_mean",
            "label"
        ]

        df.replace([np.inf, -np.inf], 0, inplace=True)
        df.fillna(0, inplace=True)

        for _, row in df.iterrows():

            attack_id = 1 if row["label"] == "BENIGN" else 2

            cursor.execute("""
            INSERT INTO network_flows (
                flow_duration,
                total_fwd_packets,
                total_bwd_packets,
                flow_bytes_per_sec,
                flow_packets_per_sec,
                packet_length_mean,
                packet_length_std,
                syn_flag_count,
                ack_flag_count,
                down_up_ratio,
                active_mean,
                attack_id,
                attack_label
)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                row["flow_duration"],
                row["total_fwd_packets"],
                row["total_bwd_packets"],
                row["flow_bytes_per_sec"],
                row["flow_packets_per_sec"],
                row["packet_length_mean"],
                row["packet_length_std"],
                row["syn_flag_count"],
                row["ack_flag_count"],
                row["down_up_ratio"],
                row["active_mean"],
                attack_id,
                row["label"]
            ))

        conn.commit()

print("All files processed")

cursor.close()
conn.close()