import streamlit as st
from db import fetch_data

st.title("🧠 Cyber Attack Education")
st.markdown("Understand network threats in a simple, structured way.")

# ==============================
# 🔧 NORMALIZATION FUNCTION
# ==============================
def normalize_attack_name(name):
    name = name.lower()
    
    if "ddos" in name:
        return "DDoS Attack"
    elif "dos" in name:
        return "DoS Attack"
    elif "web attack" in name:
        return "Web Attack"
    elif "benign" in name:
        return "Normal Traffic"
    elif "bot" in name:
        return "Bot Attack"
    elif "ftp" in name or "ssh" in name:
        return "Brute Force Attack"
    elif "port" in name:
        return "Port Scan"
    elif "infiltration" in name:
        return "Infiltration Attack"
    elif "heartbleed" in name:
        return "Heartbleed Attack"
    else:
        return name.title()

# ==============================
# 🧠 KNOWLEDGE BASE
# ==============================
attack_knowledge = {

    "DDoS Attack": {
        "desc": "Distributed Denial of Service attack where multiple systems flood a target, making it unavailable.",
        "risk": "High 🔴",
        "prevention": "Use load balancing, rate limiting, and DDoS protection services.",
        "link": "https://www.geeksforgeeks.org/computer-networks/denial-of-service-ddos-attack/"
    },

    "DoS Attack": {
        "desc": "Single-source attack that overwhelms a system with excessive requests.",
        "risk": "High 🔴",
        "prevention": "Use firewalls, request filtering, and traffic monitoring.",
        "link": "https://www.geeksforgeeks.org/computer-networks/types-of-dos-attacks/"
    },

    "Web Attack": {
        "desc": "Includes attacks like SQL Injection and XSS targeting web applications.",
        "risk": "Critical 🔴",
        "prevention": "Use input validation, prepared statements, and secure coding practices.",
        "link": "https://www.geeksforgeeks.org/sql/sql-injection/"
    },

    "Brute Force Attack": {
        "desc": "Repeated login attempts to guess credentials.",
        "risk": "High 🔴",
        "prevention": "Use strong passwords, account lockouts, and multi-factor authentication.",
        "link": "https://www.geeksforgeeks.org/computer-networks/brute-force-attack/"
    },

    "Bot Attack": {
        "desc": "Automated scripts performing malicious actions like scraping or traffic flooding.",
        "risk": "Medium 🟡",
        "prevention": "Use CAPTCHA, bot detection systems, and rate limiting.",
        "link": "https://www.geeksforgeeks.org/computer-networks/what-are-bots-botnets-and-zombies/"
    },

    "Port Scan": {
        "desc": "Scanning ports to identify vulnerabilities in a system.",
        "risk": "Medium 🟡",
        "prevention": "Close unused ports and use intrusion detection systems.",
        "link": "https://www.geeksforgeeks.org/ethical-hacking/port-scanning-attack/"
    },

    "Infiltration Attack": {
        "desc": "Unauthorized access into a network to steal data or plant malware.",
        "risk": "Critical 🔴",
        "prevention": "Use network segmentation and strict access control.",
        "link": "https://www.oreilly.com/library/view/cybersecurity-attack/9781788475297/f3ea0ec3-066c-4425-aed1-3973bd37dcbe.xhtml"
    },

    "Heartbleed Attack": {
        "desc": "Exploits OpenSSL vulnerability to steal sensitive data.",
        "risk": "Critical 🔴",
        "prevention": "Patch systems and update SSL libraries.",
        "link": "https://www.geeksforgeeks.org/ethical-hacking/what-is-heartbleed-bug-in-ethical-hacking/"
    },

    "Normal Traffic": {
        "desc": "Legitimate user activity with no malicious intent.",
        "risk": "None 🟢",
        "prevention": "No action needed.",
        "link": None
    }
}

# ==============================
# ⚙️ DEFAULT TEMPLATE
# ==============================
DEFAULT_ATTACK_INFO = {
    "desc": "No detailed description available for this attack yet.",
    "risk": "Unknown ⚪",
    "prevention": "Refer external resources.",
    "link": None
}

# ==============================
# 📡 FETCH FROM DATABASE
# ==============================
try:
    query = "SELECT DISTINCT attack_name FROM attack_types"
    df = fetch_data(query)

    if df is not None and not df.empty:
        raw_attacks = df['attack_name'].tolist()
        attack_list = sorted(list(set([normalize_attack_name(a) for a in raw_attacks])))
    else:
        attack_list = list(attack_knowledge.keys())

except:
    attack_list = list(attack_knowledge.keys())

# ==============================
# 🎛️ UI DROPDOWN
# ==============================
selected_attack = st.selectbox("Select an attack type to learn more:", attack_list)

# ==============================
# 🧠 GET DATA
# ==============================
if selected_attack in attack_knowledge:
    data = attack_knowledge[selected_attack]
else:
    data = DEFAULT_ATTACK_INFO

# ==============================
# 📊 DISPLAY
# ==============================
st.subheader(f"📌 {selected_attack}")

st.write(f"📖 **Description:** {data['desc']}")
st.write(f"⚠️ **Risk Level:** {data['risk']}")
st.write(f"🛡️ **Prevention:** {data['prevention']}")

if data["link"]:
    st.write(f"🔗 **External Resource:** [Learn More]({data['link']})")
else:
    st.write("🔗 **External Resource:** Search online for more details.")

# ==============================
# 🧾 FOOTER
# ==============================
st.markdown("---")
st.caption("ShadowTrace © 2026 | Intelligent Traffic Analysis System")