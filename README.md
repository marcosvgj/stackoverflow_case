# Uma análise sobre dados do Stack Overflow


### Table of Contents

1. [Resumo](#summary)
1. [Solução](#solution)       
    - 2.1 [Proposta do modelo relacional - ERD](#t1)
    - 2.1 [Normalização de dados utilizando Apache Spark](#t2)
3. [Queries executadas](#t3)
4. [Resultados](#t4)
5. [Questão Extra](#t5)

## Resumo <a name="summary"></a>
<p align="justify">O counteúdo deste repositório tem como objetivo demonstrar um fluxo de dados para realizar a normalização de um banco de dados utilizando como base <b>PySpark</b>. Além disso, será demonstrada a utilização da ferramenta <b>Apache Superset</b> para workloads de <i>Self-Service BI.</i></p>

## Solução <a name="solution"></a>
Como destacado anteriormente, o case foi solucionado utilizando como base a tecnologia <b>PySpark</b> e outras tecnologias que viabilizaram esta POC:

1. Apache Superset [<a href="https://superset.incubator.apache.org/"> Link! </a>]
2. Docker [<a href="https://www.docker.com/"> Link! </a>]
3. Docker Compose [<a href="https://docs.docker.com/compose/"> Link! </a>]
4. PySpark 2.4.4 [<a href="https://spark.apache.org/docs/latest/index.html"> Link! </a>]
5. Postgres 9.6 [<a href="https://www.postgresql.org/"> Link! </a>]


### Proposta do modelo relacional - ERD <a name="t1"></a>
O modelo relacional foi implementado sob o banco relacional Postgres 9.6 conforme o Diagrama de Entidade e Relacionamento abaixo: 

![Alt text](https://github.com/marcosvgj/dataengineeringatame/blob/develop/docs/erd_ame.svg)

Logicamente, o modelo foi segmentado em três principais componentes para extração de Entidades e Relacionamentos da base denormalzada inspirado no modelo ***Star Schema (Kimball)***:

1. <b>Tabelas Dimensionais:</b>
    * Respondente 
2. <b>Tabelas Fato</b>
    * Pais
    * Empresa
    * Sistema Operacional
    * Linguagem Programação
    * Ferramenta de Comunicação
3. <b>Tabelas Intermediárias:</b>
    * Respondente usa Ferramenta
    * Respondente usa Linguagem

<i> obs.: As tabelas intermediárias são originadas de relacionamentos <b>N:N</b>, tendo como necessidade a criação de uma tabela intermediária. </i>

3. Docker Compose [<a href="https://docs.docker.com/compose/"> Link! </a>]
4. PySpark 2.4.4 [<a href="https://spark.apache.org/docs/latest/index.html"> Link! </a>]
5. Postgres 9.6 [<a href="https://www.postgresql.org/"> Link! </a>]

### Normalização de dados utilizando Apache Spark <a name="t2"></a>

A organização do código Pyspark utilizada nesta POC seguiu o padrão semelhante a Arquitetura Orientada a Serviços (SOA) evidenciado abaixo. Este padrão contribui para fácil manutenção do código fonte e principalmente para escalabilidade de análises sob o dado coletado.

![Alt text](https://github.com/marcosvgj/dataengineeringatame/blob/develop/docs/arch_soa.svg)

 <table>
    <tr>
      <td> <div align="center">:pushpin: <b>Linguagem Utilizada</b></div> </td>
        <td> <b><i>PySpark</i></b>: Linguagem com base para utilização de ferramentas Big Data, além disso, possui integração nativa com uma das principais ferramentas de orquestração <i>open-Source</i> atualmente (<b>Apache Airflow</b>)</td>
    </tr>
  </table>

### DAO (Database Access Object)
Este componente tem como principal responsabilidade padronizar por meio de uma interface o acesso a diversos conjuntos de dados (<i> inicialmente csv's e tabelas de bancos de dados relacionais (<i>ex.: Postgres 9.6 utilizado nesta POC</i>). 
    
### Common
Este componente tem como principal responsabilidade manter pequenos trechos de códigos que são comumnente utilizados pelas stack's de regra de negócio (<i>ex.: Modelos abstratos do Ingestor, modelo abstrato do DAO</i>). 

### Model
Este componente tem como principal responsabilidade manter um dicionário de dados para cada tabela final gerada na stack das regras de negócio.

### Business
Este componente tem como principal responsabilidade implementar as regras de negócio.

### Service
Este componente tem como principal responsabilidade realizar a junção das regras de negócio e por sua vez prover a visão final do dado.

### API
Este componente tem como principal responsabilidade ser uma interface do componente **Service** (ex.: Interface pode ser utilizada na criação de Operadores customizados para o Apache Airflow - Orquestrador).

### Queries executadas <a name="t3"></a>


A estruturação de códigos utilizada nesta aplicação tem como o objetivo demonstrar (por meio do hands-on) a implementação da arquitetura proposta.

Nesta estruturação foram utilizadas as seguintes tecnologias: 

1. Postgres 9.6 [Dockerizado]
2. Apache Superset [Dockerizado]
3. Apache PySpark [Dockerizado]

<i>obs.: A sincronização destes componentes é de responsabilidade do Docker Compose. </i>

A proposta inicial era provisionar por meio do Docker compose um ambiente controlado para realizar o processo de ETL e a consulta de dados. As queries e os resultados podem ser obtidos através da execução do <b> docker-compose.yml </b> criado.

![Alt text](https://github.com/marcosvgj/dataengineeringatame/blob/develop/docs/visao_dockercompose.svg)

Para realizar a execução siga os passos a seguir:

***Caso o sistema operacional utilizado seja Windows antes de realizar os procedimentos a seguir execute o seguinte comando:*** ```git config --global core.autocrlf input```

1. Verifique se você possui os pré-requisitos na sua máquina: 
    - Docker [<a href="https://docs.docker.com/"> Link! </a>]
    - Docker Compose [<a href="https://docs.docker.com/compose/"> Link! </a>]
2. <b>clone o repositório:</b> ```https://github.com/marcosvgj/dataengineeringatame.git```
3. <b>execute o comando:</b> cd ```dataengineeringatame/```
4. <b>execute o comando:</b> ```docker-compose up --build -d ```
5. Aguarde em torno a execução completa do <b>docker-compose</b>
6. Após a execução de todos os serviços do docker-compose estiver com o status <b>done</b> passe para o próximo passo
7. Abra o Apache Superset em seu navegador de preferência utilizando a URL: <b>http://127.0.0.1:8088/</b>
7. Caso o sistema operacional seja Windows verifique o ip da docker-machine antes, assim a nova URL será <b>$(docker-machine ip):8088</b>
8. Usuário e senha padrão são admin:admin
8. Vá na Aba **SQL Lab** >> **Saved Queries**
9. Para cada query abra o link disponvel na coluna <b> Pop Tab Link </b> e selecione o botão <b> Run Query </b>
10. Repita a etapa 9 para cada query disponibilizada.

Para realizar o ***bypass*** no procedimento acima, os conteúdos foram disponibilizados no próprio repositório vide link's abaixo:

Insights sobre os dados normalizados: 

1. Insight 1 [<a href="https://github.com/marcosvgj/dataengineeringatame/blob/develop/superset/queries/query_01.sql"> Link! </a>]
2. Insight 2 [<a href="https://github.com/marcosvgj/dataengineeringatame/blob/develop/superset/queries/query_02.sql"> Link! </a>]
3. Insight 3 [<a href="https://github.com/marcosvgj/dataengineeringatame/blob/develop/superset/queries/query_03.sql"> Link! </a>]
4. Insight 4 [<a href="https://github.com/marcosvgj/dataengineeringatame/blob/develop/superset/queries/query_04.sql"> Link! </a>]
5. Insight 5 [<a href="https://github.com/marcosvgj/dataengineeringatame/blob/develop/superset/queries/query_05.sql"> Link! </a>]
6. Insight 6 [<a href="https://github.com/marcosvgj/dataengineeringatame/blob/develop/superset/queries/query_06.sql"> Link! </a>]
7. Insight 7 [<a href="https://github.com/marcosvgj/dataengineeringatame/blob/develop/superset/queries/query_07.sql"> Link! </a>]
8. Insight 8 [<a href="https://github.com/marcosvgj/dataengineeringatame/blob/develop/superset/queries/query_08.sql"> Link! </a>]
