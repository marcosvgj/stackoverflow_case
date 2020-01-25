from pyspark.sql.functions import udf

class Fact(Ingestor):
    CURRENCIES = spark.sparkContext.broadcast(ExchangeDAO(sleep=0.5, retries=2, timeout=5).collect())
    
    def __init__(self, source, model, database='default', table='table', sink='HiveDAO'):
        self.metadata = dict({
            'source': source,
            'database': database,
            'table': table,
            'sink': sink,
            'model': model})

    def get(self):
        model = self.metadata.get('model')
        self.update_source(Ingestor.apply(Fact.rule_1, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_2, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_3, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_4, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_5, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_6, self.metadata))
        return self.metadata.get('source')\
        .select(model().schema.fieldNames()).distinct()
    
    def save(self):
        model = self.metadata.get('model')
        self.update_source(Ingestor.apply(Fact.rule_1, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_2, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_3, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_4, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_5, self.metadata))
        self.update_source(Ingestor.apply(Fact.rule_6, self.metadata))
        data = self.metadata.get('source')\
        .select(model().schema.fieldNames())\
        .distinct()
        self.load(self.metadata, data)
    
    def update_source(self, data):
        self.metadata.update({'source': data})
    
    @udf()
    def exchange(currencySymbol, salary):
        DEFAULT_USD_VALUE = 3.81
        try:
            return CURRENCIES.value[currencySymbol] * salary if salary is not None else 0.0
        except KeyError as err:
            return DEFAULT_USD_VALUE * salary if salary is not None else 0.0
    
    def rule_1(metadata):
        data = metadata.get('source')\
        .withColumn("ConvertedSalary", when(col('SalaryType') == 'Yearly',col('ConvertedSalary')/12)\
                    .when(col('SalaryType').isNull(), col('ConvertedSalary')/12)\
                    .otherwise(col('ConvertedSalary')))
        data = data.withColumn("ConvertedSalary", when(col('ConvertedSalary').isNull(), lit(0))\
        .otherwise(col('ConvertedSalary')))
        data = data.withColumn("ConvertedSalary", col('ConvertedSalary').cast(DoubleType()))
        return data.withColumn("ConvertedSalary", Fact.exchange("CurrencySymbol","ConvertedSalary"))
        
                
    def rule_2(metadata):
        respondent_udf = udf(lambda x: f'respondente_{x}')
        return metadata.get('source').withColumn('nome', respondent_udf('Respondent'))
    
    def rule_3(metadata):
        return metadata.get('source')\
        .withColumnRenamed("ConvertedSalary", "salario")\
        .withColumnRenamed("OpenSource", "contrib_open_source")\
        .withColumnRenamed("Hobby", "programa_hobby")\
        .withColumnRenamed("Respondent", "respondente_id")\
        .withColumn("respondente_id", col("respondente_id").cast(IntegerType()))
    
    def rule_4(metadata):
        data = metadata.get("source")\
            .withColumn("LanguageWorkedWith", split(col("LanguageWorkedWith"), ';'))\
            .withColumn("LanguageWorkedWith", explode(col("LanguageWorkedWith")))
        return data\
            .withColumn("CommunicationTools", split(col("CommunicationTools"), ';'))\
            .withColumn("CommunicationTools", explode(col("CommunicationTools")))
    
    def rule_5(metadata):
        pais = PostgresDAO().select('stackoverflow.pais')\
        .withColumnRenamed("nome", "pais_nome")
        
        sistema_operacional = PostgresDAO().select('stackoverflow.sistema_operacional')\
        .withColumnRenamed("nome", "so_nome")
        
        empresa = PostgresDAO().select('stackoverflow.empresa')
        
        return metadata.get('source')\
        .join(pais, pais.pais_nome == col("Country"))\
        .join(sistema_operacional, sistema_operacional.so_nome == col("OperatingSystem"))\
        .join(empresa, empresa.tamanho == col("CompanySize"))
    
    def rule_6(metadata):
        return metadata.get('source')\
        .withColumn("contrib_open_source", when(col('contrib_open_source') == 'Yes', lit(1))\
                    .otherwise(lit(0)))\
        .withColumn("programa_hobby", when(col('programa_hobby') == 'Yes', lit(1))\
                    .otherwise(lit(0)))\
        .withColumn("salario", col("salario").cast(DoubleType()))
        
        
    