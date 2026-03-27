# Relational Schema

The relational schema represents the structure of the database in tabular form.

---

## Core Tables (OLTP)

### attack_types
attack_types(
  attack_id PRIMARY KEY,
  attack_name UNIQUE NOT NULL
)

---

### network_flows
network_flows(
  flow_id PRIMARY KEY,
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
  attack_id FOREIGN KEY → attack_types(attack_id),
  attack_label
)

---

## Data Warehouse Schema (OLAP)

### dim_attack
dim_attack(
  attack_key PRIMARY KEY,
  attack_name
)

---

### dim_traffic
dim_traffic(
  traffic_key PRIMARY KEY,
  traffic_category
)

---

### dim_time
dim_time(
  time_key PRIMARY KEY,
  time_bucket
)

---

### fact_flows
fact_flows(
  fact_id PRIMARY KEY,
  attack_key FOREIGN KEY → dim_attack(attack_key),
  traffic_key FOREIGN KEY → dim_traffic(traffic_key),
  time_key FOREIGN KEY → dim_time(time_key),
  total_flows
)

---

## 🔗 Relationships Summary

- attack_types (1) → (N) network_flows
- dim_attack (1) → (N) fact_flows
- dim_traffic (1) → (N) fact_flows
- dim_time (1) → (N) fact_flows

---

## Indexes

- idx_flow_packets(flow_packets_per_sec)
- idx_attack_packet(attack_id, flow_packets_per_sec)

---

## Notes

- OLTP schema is normalized(3NF) to reduce redundancy  
- OLAP schema follows star schema design for fast analytics  
- Foreign keys ensure referential integrity  

![Relational Schema](relational_schema.png)