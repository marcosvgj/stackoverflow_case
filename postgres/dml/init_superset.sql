INSERT INTO public.saved_query (created_on, changed_on, id, user_id, db_id, "label", "schema", "sql", description, changed_by_fk, created_by_fk, extra_json) VALUES('2020-01-27 00:00:00.000', '2020-01-27 00:00:00.000', 1, 1, 1, 'Question 1', 'stackoverflow', 'SELECT
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
    qntd_respondente asc', 'Qual a quantidade de respondentes de cada país?', 1, 1, '{}');
INSERT INTO public.saved_query (created_on, changed_on, id, user_id, db_id, "label", "schema", "sql", description, changed_by_fk, created_by_fk, extra_json) VALUES('2020-01-27 00:00:00.000', '2020-01-27 00:00:00.000', 2, 1, 1, 'Question 2', 'stackoverflow', 'SELECT
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
            nome = ''Windows'') AS B
    ON
        A.sistema_operacional_id = B.sistema_operacional_id
    INNER JOIN
        (SELECT
            pais_id
        FROM
            stackoverflow.pais
        WHERE
            nome = ''United States'') AS C
    ON
        C.pais_id = C.pais_id', 'Quantos usuários que moram em “United States” gostam de Windows?', 1, 1, '{}');
INSERT INTO public.saved_query (created_on, changed_on, id, user_id, db_id, "label", "schema", "sql", description, changed_by_fk, created_by_fk, extra_json) VALUES('2020-01-27 00:00:00.000', '2020-01-27 00:00:00.000', 3, 1, 1, 'Question 3', 'stackoverflow', 'SELECT
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
        nome = ''Israel'') AS B
ON
    A.pais_id = B.pais_id
INNER JOIN
    (SELECT
        sistema_operacional_id,
        nome
    FROM
        stackoverflow.sistema_operacional
    WHERE
        nome = ''Linux-based'') AS C
ON
    A.sistema_operacional_id = C.sistema_operacional_id', 'Qual a média de salário dos usuários que moram em Israel e gostam de Linux?', 1, 1, '{}');
INSERT INTO public.saved_query (created_on, changed_on, id, user_id, db_id, "label", "schema", "sql", description, changed_by_fk, created_by_fk, extra_json) VALUES('2020-01-27 00:00:00.000', '2020-01-27 00:00:00.000', 4, 1, 1, 'Question 4', 'stackoverflow', 'SELECT
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
        nome = ''Slack'') AS B
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
    D.tamanho', 'Qual a média e o desvio padrão do salário dos usuários que usam Slack para cada
tamanho de empresa disponível? (dica: o resultado deve ser uma tabela semelhante a
apresentada abaixo)', 1, 1, '{}');
INSERT INTO public.saved_query (created_on, changed_on, id, user_id, db_id, "label", "schema", "sql", description, changed_by_fk, created_by_fk, extra_json) VALUES('2020-01-27 00:00:00.000', '2020-01-27 00:00:00.000', 5, 1, 1, 'Question 5', 'stackoverflow', 'SELECT
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
    A.sistema_operacional_id = B.sistema_operacional_id', 'Qual a diferença entre a média de salário dos respondentes do Brasil que acham que
criar código é um hobby e a média de todos de salário de todos os respondentes
brasileiros agrupado por cada sistema operacional que eles usam? (dica: o resultado
deve ser uma tabela semelhante a apresentada abaixo)', 1, 1, '{}');
INSERT INTO public.saved_query (created_on, changed_on, id, user_id, db_id, "label", "schema", "sql", description, changed_by_fk, created_by_fk, extra_json) VALUES('2020-01-27 00:00:00.000', '2020-01-27 00:00:00.000', 6, 1, 1, 'Question 6', 'stackoverflow', 'SELECT
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
        nome != ''Not Specified'' ) AS B
ON
    A.ferramenta_comunic_id = B.ferramenta_comunic_id
ORDER BY
    A.qntd DESC
LIMIT 3;', 'Quais são as top 3 tecnologias mais usadas pelos desenvolvedores?', 1, 1, '{}');
INSERT INTO public.saved_query (created_on, changed_on, id, user_id, db_id, "label", "schema", "sql", description, changed_by_fk, created_by_fk, extra_json) VALUES('2020-01-27 00:00:00.000', '2020-01-27 00:00:00.000', 7, 1, 1, 'Question 7', 'stackoverflow', 'SELECT
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
LIMIT 5', 'Quais são os top 5 países em questão de salário?', 1, 1, '{}');
INSERT INTO public.saved_query (created_on, changed_on, id, user_id, db_id, "label", "schema", "sql", description, changed_by_fk, created_by_fk, extra_json) VALUES('2020-01-27 00:00:00.000', '2020-01-27 00:00:00.000', 8, 1, 1, 'Question 8', 'stackoverflow', 'SELECT
    COUNT(A.respondente_id) AS quantidade,
    B.nome as pais
FROM 
    stackoverflow.respondente AS A
INNER JOIN
    (SELECT
        nome,
        pais_id,
        CASE
            WHEN nome = ''United States'' THEN 4787.90
            WHEN nome = ''India'' THEN 243.52
            WHEN nome = ''United Kingdom'' THEN 6925.63
            WHEN nome = ''Germany'' THEN 6664
            WHEN nome = ''Canada'' THEN 5567.68
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
    quantidade DESC', 'A tabela abaixo contém os salários mínimos mensais de cinco países presentes na
amostra de dados. Baseado nesses valores, gostaríamos de saber quantos usuários
ganham mais de 5 salários mínimos em cada um desses países.', 1, 1, '{}');
