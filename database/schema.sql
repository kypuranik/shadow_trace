CREATE DATABASE shadow_trace;
USE shadow_trace;

CREATE TABLE attack_types (
    attack_id INT AUTO_INCREMENT PRIMARY KEY,
    attack_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE network_flows (
    flow_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    flow_duration INT,
    total_fwd_packets INT,
    total_bwd_packets INT,
    flow_bytes_per_sec FLOAT,
    flow_packets_per_sec FLOAT,
    packet_length_mean FLOAT,
    packet_length_std FLOAT,
    syn_flag_count INT,
    ack_flag_count INT,
    down_up_ratio FLOAT,
    active_mean FLOAT,
    attack_id INT NOT NULL,
    attack_label VARCHAR(100),
    FOREIGN KEY (attack_id) REFERENCES attack_types(attack_id)
);