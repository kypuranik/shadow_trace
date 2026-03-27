import re

# =========================
# 🧠 COLUMN DESCRIPTIONS
# =========================
column_descriptions = {
    "flow_id": "Unique identifier for each network flow",
    "flow_duration": "Duration of the connection",
    "total_fwd_packets": "Total packets sent forward",
    "total_bwd_packets": "Total packets sent backward",
    "flow_packets_per_sec": "Number of packets transmitted per second",
    "flow_bytes_per_sec": "Data transfer rate in bytes per second",
    "packet_length_mean": "Average packet size",
    "packet_length_std": "Variation in packet size",
    "syn_flag_count": "Number of SYN flags (connection requests)",
    "ack_flag_count": "Number of ACK flags (acknowledgments)",
    "attack_id": "ID representing type of attack",
    "attack_label": "Human-readable attack name"
}


def map_natural_language_to_sql(user_input):
    text = user_input.lower()

    # =========================
    # 📂 DATABASE META QUERIES
    # =========================
    if "how many tables" in text:
        return """
        SELECT COUNT(*) as total_tables
        FROM information_schema.tables 
        WHERE table_schema = 'shadow_trace';
        """

    if "tables" in text and ("what" in text or "list" in text):
        return """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'shadow_trace';
        """

    if "columns" in text:
        return """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = 'network_flows';
        """

    if "how many rows" in text or "number of rows" in text:
        return """
        SELECT COUNT(*) as total_rows 
        FROM network_flows;
        """

    # =========================
    # 🧠 COLUMN EXPLANATION
    # =========================
    for col in column_descriptions:
        if col in text:
            return f"EXPLAIN_COLUMN::{col}"

    # =========================
    # 🔍 ENTITY DETECTION
    # =========================
    attacks = {
        "dos": "%DoS%",
        "ddos": "%DDoS%",
        "web": "%Web%",
        "bot": "%Bot%",
        "port": "%Port%",
        "infiltration": "%Infiltration%",
        "heartbleed": "%Heartbleed%",
        "brute": "%Patator%",
    }

    detected_attacks = []
    for key in attacks:
        if key in text:
            detected_attacks.append(attacks[key])

    # =========================
    # 🔢 TOP N DETECTION
    # =========================
    match = re.search(r"top (\d+)", text)
    top_n = int(match.group(1)) if match else None

    # =========================
    # 🎯 INTENT DETECTION
    # =========================

    # LIST
    if "list" in text or "what are" in text:
        return "SELECT DISTINCT attack_name FROM attack_types;"

    # COUNT
    if "how many" in text or "count" in text:
        if detected_attacks:
            return f"""
            SELECT COUNT(*) as count
            FROM network_flows f
            JOIN attack_types a ON f.attack_id = a.attack_id
            WHERE a.attack_name LIKE '{detected_attacks[0]}';
            """
        else:
            return "SELECT COUNT(*) as total_flows FROM network_flows;"

    # TOP N
    if top_n:
        return f"""
        SELECT a.attack_name, COUNT(*) as count
        FROM network_flows f
        JOIN attack_types a ON f.attack_id = a.attack_id
        GROUP BY a.attack_name
        ORDER BY count DESC
        LIMIT {top_n};
        """

    # MOST / DANGEROUS
    if "most" in text or "highest" in text or "danger" in text:
        return """
        SELECT a.attack_name, COUNT(*) as count
        FROM network_flows f
        JOIN attack_types a ON f.attack_id = a.attack_id
        GROUP BY a.attack_name
        ORDER BY count DESC
        LIMIT 1;
        """

    # TRAFFIC
    if "traffic" in text or "packets" in text:
        if "high" in text:
            return """
            SELECT flow_id, flow_packets_per_sec
            FROM network_flows
            ORDER BY flow_packets_per_sec DESC
            LIMIT 10;
            """
        elif "low" in text:
            return """
            SELECT flow_id, flow_packets_per_sec
            FROM network_flows
            ORDER BY flow_packets_per_sec ASC
            LIMIT 10;
            """
        elif detected_attacks:
            return f"""
            SELECT a.attack_name, AVG(f.flow_packets_per_sec) as avg_traffic
            FROM network_flows f
            JOIN attack_types a ON f.attack_id = a.attack_id
            WHERE a.attack_name LIKE '{detected_attacks[0]}'
            GROUP BY a.attack_name;
            """

    # COMPARE
    if "compare" in text and len(detected_attacks) >= 2:
        return f"""
        SELECT a.attack_name, AVG(f.flow_packets_per_sec) as avg_traffic
        FROM network_flows f
        JOIN attack_types a ON f.attack_id = a.attack_id
        WHERE a.attack_name LIKE '{detected_attacks[0]}'
           OR a.attack_name LIKE '{detected_attacks[1]}'
        GROUP BY a.attack_name;
        """

    # FILTER
    if detected_attacks:
        return f"""
        SELECT f.flow_id, a.attack_name, f.flow_packets_per_sec
        FROM network_flows f
        JOIN attack_types a ON f.attack_id = a.attack_id
        WHERE a.attack_name LIKE '{detected_attacks[0]}';
        """

    # DEFAULT
    return None