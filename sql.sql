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

select mq2.timestamp, mq2.value as v1, mq3.value as v2 from mq2 FULL OUTER JOIN mq3 ON mq2.timestamp=mq3.timestamp
select mq2.timestamp, mq2.value as mq2a, mq3.value as mq3a, mq4.value as mq4a from mq2 FULL OUTER JOIN mq3 ON mq2.timestamp=mq3.timestamp FULL OUTER JOIN mq4 ON mq3.timestamp=mq4.timestamp AS ALL ORDER BY mq2.timestamp DESC LIMIT 6;