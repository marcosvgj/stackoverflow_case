SELECT
    D.tamanho, 
    AVG(C.salario) AS media_salario,
    STDDEV(C.salario) AS desvio_p_salario
FROM
    stackoverflow.resp_usa_ferramenta AS A
INNER JOIN
    (SELECT
        ferramenta_comunic_id,
        nome
    FROM 
        stackoverflow.ferramenta_comunic
    WHERE
        nome = 'Slack') AS B
ON
    A.ferramenta_comunic_id = B.ferramenta_comunic_id
INNER JOIN
    (SELECT
        respondente_id,
        empresa_id,
        salario
    FROM
        stackoverflow.respondente ) AS C
ON
    A.respondente_id = C.respondente_id
INNER JOIN
    stackoverflow.empresa AS D
ON
    C.empresa_id = D.empresa_ID
GROUP BY
    D.tamanho
ORDER BY
    D.tamanho
