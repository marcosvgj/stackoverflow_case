SELECT
    AVG(A.salario) as media_salario
FROM
    (SELECT
        respondente_id,
        pais_id,
        sistema_operacional_id,
        salario
    FROM
        stackoverflow.respondente ) AS A
INNER JOIN
    (SELECT
        pais_id,
        nome
    FROM
        stackoverflow.pais
    WHERE
        nome = 'Israel') AS B
ON
    A.pais_id = B.pais_id
INNER JOIN
    (SELECT
        sistema_operacional_id,
        nome
    FROM
        stackoverflow.sistema_operacional
    WHERE
        nome = 'Linux-based') AS C
ON
    A.sistema_operacional_id = C.sistema_operacional_id