CREATE VIEW attack_summary AS
SELECT attack_id, COUNT(*) AS total_flows
FROM network_flows
GROUP BY attack_id;

CREATE VIEW attack_details AS
SELECT nf.*, at.attack_name
FROM network_flows nf
JOIN attack_types at
ON nf.attack_id = at.attack_id;