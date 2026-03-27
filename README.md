# ⚡ ShadowTrace: Network Traffic Analysis & Attack Detection

ShadowTrace is an interactive system for analyzing network traffic, detecting attack patterns, and simulating real-time anomalies using a combination of **DBMS concepts, NLP querying, and live simulation**.

---

## 📌 Key Highlights

* 📊 Real-time traffic simulation with anomaly detection
* 🧠 Natural Language → SQL query system
* 🗄️ MySQL database with optimized schema & indexing
* ⚡ OLTP + OLAP (Star Schema) integration
* 📈 Interactive dashboard for traffic insights

---

## 📦 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🏗️ System Architecture

![Architecture](docs/architecture.png)

---

## 🧩 ER Diagram

![ER Diagram](docs/er_diagram.png)

---

## 📐 Relational Schema

![Relational Schema](docs/relational_schema.png)

---

## 📸 Screenshots

### 📊 Dashboard

#### Overview

![Dashboard Overview](screenshots/dashboard_overview.png)

#### Attack Distribution

![Dashboard Chart](screenshots/dashboard_chart.png)

#### Data Summary

![Dashboard Table](screenshots/dashboard_table.png)

---

### ⚡ Simulation

#### Traffic Graph

![Simulation Graph](screenshots/simulation_graph.png)

#### Data Table

![Simulation Table](screenshots/simulation_table.png)

---

### 💬 NLP Query

![Query](screenshots/query.png)

---

### 📖 Learn Module

![Learn](screenshots/learn.png)

---

## 🚀 Features

### 📊 Dashboard

* Visualizes network traffic patterns
* Shows high-intensity flows
* Displays dominant attack types

### ⚡ Live Simulation

* Generates real-time traffic data
* Detects high packet rate anomalies (DDoS simulation)
* Adjustable simulation speed

### 💬 NLP Query System

* Converts natural language into SQL queries
* Example:

  * "Show most common attacks"
  * "Find high traffic flows"

### 📖 Learning Module

* Explains attack types
* Shows risk levels and prevention methods

---

## 🧠 Database Design

### 🔹 OLTP (Transactional)

* `network_flows`
* `attack_types`

### 🔹 OLAP (Star Schema)

* `fact_flows`
* `dim_attack`
* `dim_traffic`
* `dim_time`

---

## ⚡ DBMS Concepts Used

* Relational Schema Design
* Normalization (3NF)
* Primary & Foreign Keys
* Indexing (Single + Composite)
* Query Optimization (EXPLAIN)
* Views
* Stored Procedures
* Star Schema (OLAP)
* Aggregation & Joins

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Database:** MySQL
* **Libraries:** Pandas, NumPy

---

## 📂 Dataset

Due to GitHub size limits, the full dataset is not included in this repository.

🔗 Download Dataset:
https://drive.google.com/drive/folders/1ghUgOM6Sz9Y5HP9vi60ip2JfVF-NolU1?usp=share_link

After downloading, place the files inside:
`dataset/`

Dataset source: CICIDS2017 (real-world network traffic dataset)

---

## 📂 Project Structure

```
shadow_trace/
├── requirements.txt
├── app/
│   ├── app.py
│   ├── db.py
│   ├── load_flows.py
│   ├── query_mapper.py
│   └── pages/
│
├── dataset/
├── database/
├── docs/
├── screenshots/
├── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone repository

```bash
git clone https://github.com/kypuranik/shadow_trace
cd shadow_trace
```

### 2️⃣ Setup database

```sql
CREATE DATABASE shadow_trace;
```

Run SQL files from the `database/` folder.

### 3️⃣ Install dependencies

```bash
pip install streamlit pandas numpy pymysql
```

### 4️⃣ Run application

```bash
cd app
streamlit run app.py
```

---

## 🎯 Use Cases

* Network traffic monitoring
* Cyber attack detection (DDoS, PortScan)
* DBMS concept demonstration
* Educational cybersecurity tool

---

## 🔥 Project Highlights

* Designed a hybrid OLTP + OLAP database system
* Implemented real-time traffic simulation with anomaly detection
* Built NLP-based query interface converting natural language to SQL
* Optimized queries using indexes and execution plan analysis

---

## 📌 Future Improvements

* Real-time packet capture integration
* Machine learning-based attack detection
* Advanced visualization dashboards

---

## 👨‍💻 Author

Kaivalya Puranik

---

## ⭐ If you like this project

Give it a ⭐ on GitHub!
