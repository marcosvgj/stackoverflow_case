SELECT
    B.nome AS sistema_operacional,
    A.salario_hobby AS media_hobby,
    A.geral AS media_geral,
    ABS(A.geral - A.salario_hobby) AS diff_media
FROM 
    (SELECT
        AVG(T1.salario) AS geral,
        AVG(T1.salario_hobby) AS salario_hobby,
        T1.sistema_operacional_id 
    FROM 
        (SELECT
            respondente_id,
            salario,
            sistema_operacional_id,
            CASE WHEN programa_hobby = 1 THEN salario ELSE 0 END AS salario_hobby
        FROM
            stackoverflow.respondente) AS T1
    GROUP BY
        sistema_operacional_id ) AS A
INNER JOIN
    stackoverflow.sistema_operacional AS B
ON
    A.sistema_operacional_id = B.sistema_operacional_id