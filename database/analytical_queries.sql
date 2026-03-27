--some analytical queries for the dashboard 
-- Top attacks
SELECT at.attack_name, COUNT(*) AS total
FROM network_flows nf
JOIN attack_types at
ON nf.attack_id = at.attack_id
GROUP BY at.attack_name
ORDER BY total DESC;

-- Traffic distribution
SELECT t.traffic_category, SUM(total_flows)
FROM fact_flows f
JOIN dim_traffic t ON f.traffic_key = t.traffic_key
GROUP BY t.traffic_category;

-- Multi-dimensional analysis
SELECT
a.attack_name,
t.traffic_category,
d.time_bucket,
SUM(total_flows) AS attack_count
FROM fact_flows f
JOIN dim_attack a ON f.attack_key = a.attack_key
JOIN dim_traffic t ON f.traffic_key = t.traffic_key
JOIN dim_time d ON f.time_key = d.time_key
GROUP BY a.attack_name, t.traffic_category, d.time_bucket;