CREATE INDEX idx_flow_packets
ON network_flows(flow_packets_per_sec);

-- Composite index to optimize attack + traffic queries
CREATE INDEX idx_attack_packet
ON network_flows(attack_id, flow_packets_per_sec);