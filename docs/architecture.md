# System Architecture

ShadowTrace is a network traffic analysis system that combines database analytics, NLP querying, and real-time simulation.

## Data Flow

Dataset (CICIDS CSV files)
        ↓
Python ETL Pipeline (load_flows.py)
        ↓
MySQL Database (shadow_trace)
        ↓
Streamlit Application
        ↓
User Interaction

---

## Components

### 1. Data Ingestion Layer
- Loads raw CSV data into MySQL
- Cleans and preprocesses network flow data

### 2. Database Layer
- Stores structured network traffic
- Maintains relationships using foreign keys
- Optimized with indexes

### 3. Application Layer
- Built using Streamlit
- Provides:
  - Dashboard analytics
  - NLP query interface
  - Learning module
  - Real-time simulation

### 4. Simulation Layer
- Generates live traffic data
- Stores data in session memory
- Enables real-time analytics

---

## ⚡ Modes of Operation

- **Historical Mode** → Uses MySQL database
- **Simulation Mode** → Uses live generated data

---

## Key Idea

The system integrates:
- Static database analysis
- Real-time data simulation
- Natural language querying

to provide a comprehensive traffic analysis platform.