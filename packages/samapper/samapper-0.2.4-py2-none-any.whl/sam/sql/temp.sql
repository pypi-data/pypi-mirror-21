CREATE VIEW s1_nodes_view AS SELECT DISTINCT ipstart, ipend, subnet, alias, env, x, y, radius
FROM s1_Nodes AS `n`
  JOIN (SELECT src AS 'ip' from s1_ds1_Links
        UNION
        SELECT dst AS 'ip' from s1_ds1_Links) AS `lnks`
  ON `lnks`.ip BETWEEN `n`.ipstart AND `n`.ipend
WHERE (`n`.ipstart=`n`.ipend OR alias IS NOT NULL)
ORDER BY ipstart ASC, ipend ASC;



SELECT ipstart, ipend, subnet, alias, env, x, y, radius
FROM s1_nodes_view AS `n`;




SELECT `us`.ipstart, `us`.ipend, `us`.subnet, `us`.alias, n.env, n.x, n.y, n.radius
FROM (SELECT u8.ipstart * 16777216 AS 'ipstart', u8.ipstart * 16777216 + 16777215 AS 'ipend', 8 AS 'subnet', u8.alias AS 'alias'
  FROM (SELECT ipstart / 16777216 AS 'ipstart', MAX(alias) AS 'alias', COUNT(1) AS 'hosts', COUNT(DISTINCT alias) AS 'aliases'
    FROM s1_nodes_view
    GROUP BY ipstart / 16777216
    HAVING aliases = 1 AND hosts > 1
  ) AS `u8`
  UNION
  SELECT u16.ipstart * 65536 AS 'ipstart', u16.ipstart * 65536 + 65535 AS 'ipend', 16 AS 'subnet', u16.alias AS 'alias'
  FROM (SELECT ipstart / 65536 AS 'ipstart', MAX(alias) AS 'alias', COUNT(1) AS 'hosts', COUNT(DISTINCT alias) AS 'aliases'
    FROM s1_nodes_view
    GROUP BY ipstart / 65536
    HAVING aliases = 1 AND hosts > 1
  ) AS `u16`
  UNION
  SELECT u24.ipstart * 256 AS 'ipstart', u24.ipstart * 256 + 255 AS 'ipend', 24 AS 'subnet', u24.alias AS 'alias'
  FROM (SELECT ipstart / 256 AS 'ipstart', MAX(alias) AS 'alias', COUNT(1) AS 'hosts', COUNT(DISTINCT alias) AS 'aliases'
    FROM s1_nodes_view
    GROUP BY ipstart / 256
    HAVING aliases = 1 AND hosts > 1
  ) AS `u24`
) AS `us`
JOIN s1_Nodes AS `n`
  ON n.ipstart = us.ipstart AND n.ipend = us.ipend
ORDER BY `us`.subnet ASC;