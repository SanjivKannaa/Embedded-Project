-- SELECT timestamp, value FROM ( SELECT timestamp, value as {} FROM {} UNION SELECT timestamp, value as {} FROM {} UNION SELECT timestamp, value as {} FROM {} ) AS all ORDER BY timestamp DESC LIMIT 6

INSERT INTO mq2 values("1", "1");
INSERT INTO mq2 values("2", "1");
INSERT INTO mq2 values("3", "0");
INSERT INTO mq2 values("4", "1");
INSERT INTO mq2 values("5", "1");


INSERT INTO mq3 values("1", "1");
INSERT INTO mq3 values("2", "1");
INSERT INTO mq3 values("3", "0");
INSERT INTO mq3 values("4", "1");


INSERT INTO mq4 values("1", "1");
INSERT INTO mq4 values("2", "1");
INSERT INTO mq4 values("4", "0");
INSERT INTO mq4 values("5", "1");




SELECT
mq2.timestamp,
mq2.value AS mq2value,
mq3.value AS mq3value,
mq4.value AS mq4value
FROM mq2
LEFT JOIN mq3 ON mq2.timestamp = mq3.timestamp
LEFT JOIN mq4 ON mq3.timestamp = mq4.timestamp
ORDER BY timestamp;

+-----------+----------+----------+----------+
| timestamp | mq2value | mq3value | mq4value |
+-----------+----------+----------+----------+
| 1         | 1        | 1        | 1        |
| 2         | 1        | 1        | 1        |
| 3         | 0        | 0        |          |
| 4         | 1        | 1        | 0        |
| 5         | 1        |          | 1        |
+-----------+----------+----------+----------+