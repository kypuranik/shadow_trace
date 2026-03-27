# 🧱 Database Design

The ShadowTrace database is designed using both **relational (OLTP)** and **analytical (OLAP)** modeling techniques.

---

#  1. Core Transactional Tables (OLTP)

### 🔹 network_flows
Stores detailed network traffic data.

- Primary Key: `flow_id`
- Contains:
  - Packet counts
  - Flow duration
  - Traffic rates
  - Statistical features

---

### 🔹 attack_types
Stores unique attack categories.

- Primary Key: `attack_id`
- Constraint: `UNIQUE attack_name`
- Used for normalization (avoids redundancy)

---

# 🔗 Relationships

- `network_flows.attack_id` → `attack_types.attack_id`
- Enforced using **FOREIGN KEY constraint**

  This ensures:
- Data consistency  
- Referential integrity  

---

# ⚡ 2. Indexing Strategy

To optimize query performance:

### ✔ Single-column index
- `flow_packets_per_sec`

### ✔ Composite index
- `(attack_id, flow_packets_per_sec)`

  This improves performance for queries like:
- Filtering by attack type
- High-traffic analysis

---

# Query Optimization

- Used `EXPLAIN` to analyze query execution plans
- Reduced full table scans using indexes

---

# 3. Views (Virtual Tables)

### 🔹 attack_summary
- Aggregates total flows per attack

### 🔹 attack_details
- Joins flow data with attack names for readability

 Used to simplify complex queries

---

# 4. Stored Procedures

### 🔹 GetTopAttacks()
- Returns most frequent attacks

### 🔹 GetFlowsByTraffic(min_packets)
- Filters flows based on traffic threshold

 Enables reusable and efficient query execution

---

# 5. Data Warehouse (OLAP - Star Schema)

To support analytical queries, a star schema is implemented.

---

## ⭐ Fact Table

### 🔹 fact_flows
- Stores aggregated traffic counts
- Measures:
  - `total_flows`

---

## Dimension Tables

### 🔹 dim_attack
- Attack categories

### 🔹 dim_traffic
- Traffic levels:
  - Low
  - Medium
  - High

### 🔹 dim_time
- Flow duration buckets:
  - Short
  - Medium
  - Long

---

## 🔗 Star Schema Relationships
        dim_attack
             |
dim_time — fact_flows — dim_traffic

  Enables:
- Multi-dimensional analysis  
- Faster aggregation queries  

---

#  Analytical Capabilities

Using the warehouse design, the system supports:

- Attack distribution analysis  
- Traffic intensity analysis  
- Time-based flow analysis  
- Combined multi-dimensional insights  

---

# DBMS Concepts Used
- Relational Schema Design  
- Normalization  
- Primary Keys & Foreign Keys  
- Indexing (Single + Composite)  
- Query Optimization using EXPLAIN  
- Views (Virtual Tables)  
- Stored Procedures  
- OLAP Star Schema  
- Aggregation (GROUP BY)  
- JOIN Operations  

---

# Summary

The database combines:

- **Efficient transactional storage (OLTP)**
- **High-performance analytical querying (OLAP)**

to support both real-time and historical network traffic analysis.

## ER Diagram
The following diagram represents the entity relationships in the system:
![ER Diagram](er_diagram.png)

## Relational Schema
![Relational Schema](relational_schema.png)