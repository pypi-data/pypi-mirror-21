SELECT ipstart, ipend, subnet, alias, env, x, y, radius
FROM s1_Nodes AS `n`
  JOIN (SELECT src AS 'ip' from s1_ds2_Links
        UNION
        SELECT dst AS 'ip' from s1_ds2_Links) AS `lnks`
  ON `lnks`.ip = `n`.ipstart
WHERE `n`.ipstart=`n`.ipend OR alias IS NOT NULL;

SELECT DISTINCT ipstart, ipend, subnet, alias, env, x, y, radius
FROM s1_Nodes AS `n`
  JOIN (SELECT src AS 'ip' from s1_ds2_Links
        UNION
        SELECT dst AS 'ip' from s1_ds2_Links) AS `lnks`
  ON `lnks`.ip BETWEEN `n`.ipstart AND `n`.ipend
WHERE `n`.ipstart=`n`.ipend OR alias IS NOT NULL;