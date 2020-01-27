SELECT
    COUNT(1) AS qntd_respondente,
    B.nome AS nome_pais
FROM
    (SELECT
        respondente_id,
        pais_id
    FROM
        stackoverflow.respondente) AS A
INNER JOIN
    stackoverflow.pais as B
ON
    A.pais_id = B.pais_id
GROUP BY
    B.nome
ORDER BY
    qntd_respondente asc