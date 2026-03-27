DELIMITER //

CREATE PROCEDURE GetTopAttacks()
BEGIN
    SELECT attack_id, COUNT(*) AS total
    FROM network_flows
    GROUP BY attack_id
    ORDER BY total DESC
    LIMIT 5;
END //

CREATE PROCEDURE GetFlowsByTraffic(IN min_packets INT)
BEGIN
    SELECT *
    FROM network_flows
    WHERE flow_packets_per_sec > min_packets;
END //

DELIMITER ;