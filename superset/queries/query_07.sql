SELECT
    RANK () OVER (ORDER BY A.total_salario DESC) AS colocacao,
    B.nome as pais
FROM 
    (SELECT
        SUM(T1.salario) AS total_salario,
        T1.pais_id
    FROM
        (SELECT
            respondente_id, 
            salario,
            pais_id
        FROM
            stackoverflow.respondente) AS T1
    GROUP BY
        pais_id ) AS A
INNER JOIN
    stackoverflow.pais AS B
ON
    A.pais_id = B.pais_id
ORDER BY
    A.total_salario DESC
LIMIT 5