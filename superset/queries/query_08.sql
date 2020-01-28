SELECT
    COUNT(A.respondente_id) AS quantidade,
    B.nome as pais
FROM 
    stackoverflow.respondente AS A
INNER JOIN
    (SELECT
        nome,
        pais_id,
        CASE
            WHEN nome = 'United States' THEN 4787.90
            WHEN nome = 'India' THEN 243.52
            WHEN nome = 'United Kingdom' THEN 6925.63
            WHEN nome = 'Germany' THEN 6664
            WHEN nome = 'Canada' THEN 5567.68
            ELSE NULL
        END AS salario_minimo
    FROM
        stackoverflow.pais) AS B
ON
    A.pais_id = B.pais_id
WHERE
    B.salario_minimo IS NOT NULL
AND
    A.salario > (5 * B.salario_minimo)
GROUP BY
    B.nome
ORDER BY
    quantidade DESC
    


            