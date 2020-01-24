DROP SCHEMA IF EXISTS stackoverflow;
CREATE SCHEMA stackoverflow;

DROP TABLE IF EXISTS stackoverflow.empresa;
CREATE TABLE IF NOT EXISTS stackoverflow.empresa (
    empresa_id INT NOT NULL,
    tamanho VARCHAR(255) NOT NULL,
    PRIMARY KEY (empresa_id)
);

DROP TABLE IF EXISTS stackoverflow.pais;
CREATE TABLE IF NOT EXISTS stackoverflow.pais (
    pais_id INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (pais_id)
);

DROP TABLE IF EXISTS stackoverflow.sistema_operacional;
CREATE TABLE IF NOT EXISTS stackoverflow.sistema_operacional (
    sistema_operacional_id INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (sistema_operacional_id)
);

DROP TABLE IF EXISTS stackoverflow.linguagem_programacao;
CREATE TABLE IF NOT EXISTS stackoverflow.linguagem_programacao (
    linguagem_programacao_id INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (linguagem_programacao_id)
);


DROP TABLE IF EXISTS stackoverflow.ferramenta_comunic;
CREATE TABLE IF NOT EXISTS stackoverflow.ferramenta_comunic (
    ferramenta_comunic_id INT NOT NULL,
    nome VARCHAR(255) NOT NULL,
    PRIMARY KEY (ferramenta_comunic_id)
);

DROP TABLE IF EXISTS stackoverflow.respondente;
CREATE TABLE IF NOT EXISTS stackoverflow.respondente (
    respondente_id SERIAL,
    nome VARCHAR(255) NOT NULL,
    contrib_open_source SMALLINT NOT NULL,
    programa_hobby SMALLINT NOT NULL,
    salario FLOAT NOT NULL,
    sistema_operacional_id INT NOT NULL,
    pais_id INT NOT NULL,
    empresa_id INT NOT NULL,
    PRIMARY KEY (respondente_id),
    FOREIGN KEY (sistema_operacional_id)
        REFERENCES stackoverflow.sistema_operacional (sistema_operacional_id)
        ON UPDATE RESTRICT ON DELETE CASCADE,
    FOREIGN KEY (pais_id)
        REFERENCES stackoverflow.pais (pais_id)
        ON UPDATE RESTRICT ON DELETE CASCADE,
    FOREIGN KEY (empresa_id)
        REFERENCES stackoverflow.empresa (empresa_id)
        ON UPDATE RESTRICT ON DELETE CASCADE
);

DROP TABLE IF EXISTS stackoverflow.resp_usa_linguagem;
CREATE TABLE IF NOT EXISTS stackoverflow.resp_usa_linguagem (
    resp_usa_linguagem_id SERIAL,
    respondente_id INT NOT NULL,
    linguagem_programacao_id INT NOT NULL,
    momento SMALLINT NOT NULL,
    PRIMARY KEY (resp_usa_linguagem_id),
    FOREIGN KEY (respondente_id)
        REFERENCES stackoverflow.respondente (respondente_id)
        ON UPDATE RESTRICT ON DELETE CASCADE,
    FOREIGN KEY (linguagem_programacao_id)
        REFERENCES stackoverflow.linguagem_programacao (linguagem_programacao_id)
        ON UPDATE RESTRICT ON DELETE CASCADE
);


DROP TABLE IF EXISTS stackoverflow.resp_usa_ferramenta;
CREATE TABLE IF NOT EXISTS stackoverflow.resp_usa_ferramenta (
    resp_usa_ferramenta_id SERIAL,
    respondente_id INT NOT NULL,
    ferramenta_comunic_id INT NOT NULL,
    PRIMARY KEY (resp_usa_ferramenta_id),
    FOREIGN KEY (respondente_id)
        REFERENCES stackoverflow.respondente (respondente_id)
        ON UPDATE RESTRICT ON DELETE CASCADE,
    FOREIGN KEY (ferramenta_comunic_id)
        REFERENCES stackoverflow.ferramenta_comunic (ferramenta_comunic_id)
        ON UPDATE RESTRICT ON DELETE CASCADE
);