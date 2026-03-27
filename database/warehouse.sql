CREATE TABLE dim_attack (
    attack_key INT AUTO_INCREMENT PRIMARY KEY,
    attack_name VARCHAR(50)
);

CREATE TABLE dim_traffic (
    traffic_key INT AUTO_INCREMENT PRIMARY KEY,
    traffic_category VARCHAR(50)
);

CREATE TABLE dim_time (
    time_key INT AUTO_INCREMENT PRIMARY KEY,
    time_bucket VARCHAR(50)
);

CREATE TABLE fact_flows (
    fact_id INT AUTO_INCREMENT PRIMARY KEY,
    attack_key INT,
    traffic_key INT,
    time_key INT,
    total_flows INT,
    FOREIGN KEY (attack_key) REFERENCES dim_attack(attack_key),
    FOREIGN KEY (traffic_key) REFERENCES dim_traffic(traffic_key),
    FOREIGN KEY (time_key) REFERENCES dim_time(time_key)
);