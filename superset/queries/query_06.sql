SELECT
    RANK () OVER (ORDER BY A.qntd DESC) AS colocacao,
    B.nome AS tecnologia
FROM 
    (SELECT
        COUNT(1) as qntd,
        ferramenta_comunic_id
    FROM
        stackoverflow.resp_usa_ferramenta
    GROUP BY
        ferramenta_comunic_id) AS A
INNER JOIN
    (SELECT
        *
    FROM
        stackoverflow.ferramenta_comunic
    WHERE
        nome != 'Not Specified' ) AS B
ON
    A.ferramenta_comunic_id = B.ferramenta_comunic_id
ORDER BY
    A.qntd DESC
LIMIT 3;