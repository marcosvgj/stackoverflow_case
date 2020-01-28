# Data Engineering - AME Digital
Uma análise sobre dados do Stack Overflow

### Table of Contents

1. [Resumo](#summary)
1. [Solução](#solution)       
    - 2.1 [Proposta do modelo relacional - ERD](#t1)
    - 2.1 [Normalização de dados utilizando Apache Spark](#t2)
3. [Setup da aplicação](#t3)
    - 2.3 [Criação e ingestão das tabelas](#q4)
    - 2.4 [Queries ad-hoc, uma análise utilizando Spark Dataframe](#q5)


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


## TODO

![Alt text](https://github.com/marcosvgj/dataengineeringatame/blob/develop/docs/teste.png)
