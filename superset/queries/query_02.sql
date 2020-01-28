SELECT
    COUNT(1) as qntd
FROM
    (SELECT
        respondente_id,
        pais_id,
        sistema_operacional_id
    FROM
        stackoverflow.respondente) AS A
    INNER JOIN
        (SELECT
            sistema_operacional_id
        FROM
            stackoverflow.sistema_operacional
        WHERE
            nome = 'Windows') AS B
    ON
        A.sistema_operacional_id = B.sistema_operacional_id
    INNER JOIN
        (SELECT
            pais_id
        FROM
            stackoverflow.pais
        WHERE
            nome = 'United States') AS C
    ON
        C.pais_id = C.pais_id