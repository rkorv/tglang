SELECT (
    SELECT package_type 
    FROM packages p
    WHERE p.length >= g.length AND p.width >= g.width AND 
    p.height >= g.height
    ORDER BY p.length * p.width * p.height
    LIMIT 1 
) AS package_type, COUNT(*) AS number
FROM gifts g
GROUP BY 1
ORDER BY 1;