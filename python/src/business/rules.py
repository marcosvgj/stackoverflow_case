from common.utils import spark
from dao.postgres import PostgresDAO
from pyspark.sql.functions import col, explode, split, when, lit, udf, concat
from dao.external.api.exchange import ExchangeDAO
from pyspark.sql.types import *

currencies = spark.getOrCreate().sparkContext.broadcast(ExchangeDAO(sleep=0.5, retries=2, timeout=5).collect())

class DimensionRules(object):
    @staticmethod
    def create_index(field, source):
        return map(lambda x, y: (x+1, y.asDict()[field]), range(0, len(source)), source)
    
    @staticmethod
    def checkNullity(metadata, field, in_null_cases='Not Specified'):
        """ Responsible for verifying the field's integrity given dataframe """
        return metadata.get('source').\
            withColumn(field, when(col(field).isNull(), lit(in_null_cases))\
            .otherwise(col(field)))

    @staticmethod
    def dictionaryization(metadata):
        """ Responsible to implement business logic to dimensional tables """
        model = metadata.get('model')
        field = metadata.get('description_field')

        if metadata.get('embbebedList') == False:
            data = DimensionRules.checkNullity(field=field, metadata=metadata)\
                .select(field)\
                .distinct()\
                .collect()
        else:
            data = DimensionRules.checkNullity(field=field, metadata=metadata)\
                .select(field)\
                .withColumn(field, split(col(field), ';'))\
                .withColumn(field, explode(col(field)))\
                .distinct()\
                .collect()
        
        return spark.getOrCreate().createDataFrame(DimensionRules.create_index(field, data), model().schema)

class FactRules(object):    
    
    @staticmethod
    def salary_standardization(metadata):
        rule_year_to_month_salary_type = when(col('SalaryType') == 'Yearly',col('ConvertedSalary')/12)
        rule_year_to_month_default = when(col('SalaryType').isNull(), col('ConvertedSalary')/12)
        rule_null_salary = when(col('ConvertedSalary').isNull(), lit(0)).otherwise(col('ConvertedSalary'))
        rule_apply_exchange_standardization = exchange_conversion("CurrencySymbol","ConvertedSalary")
        rule_cast_double = col('ConvertedSalary').cast(DoubleType())

        return metadata.get('source')\
        .withColumn("ConvertedSalary", rule_year_to_month_salary_type)\
        .withColumn("ConvertedSalary", rule_year_to_month_default)\
        .withColumn("ConvertedSalary", rule_null_salary)\
        .withColumn("ConvertedSalary", rule_apply_exchange_standardization)\
        .withColumn("ConvertedSalary", rule_cast_double)
        
    @staticmethod
    def respondent_name_creation(metadata):
        return metadata.get('source').withColumn('nome', concat(lit('respondente_'), col('Respondent')))
    
    @staticmethod
    def columns_renames(metadata):
        return metadata.get('source')\
        .withColumnRenamed("ConvertedSalary", "salario")\
        .withColumnRenamed("OpenSource", "contrib_open_source")\
        .withColumnRenamed("Hobby", "programa_hobby")\
        .withColumnRenamed("Respondent", "respondente_id")\
        .withColumn("respondente_id", col("respondente_id").cast(IntegerType()))
    
    @staticmethod
    def treat_embbebed_list(metadata):
        return metadata.get("source")\
            .withColumn("LanguageWorkedWith", split(col("LanguageWorkedWith"), ';'))\
            .withColumn("LanguageWorkedWith", explode(col("LanguageWorkedWith")))\
            .withColumn("CommunicationTools", split(col("CommunicationTools"), ';'))\
            .withColumn("CommunicationTools", explode(col("CommunicationTools")))

    @staticmethod
    def fact_enrichment(metadata):
        pais = PostgresDAO().select('stackoverflow.pais').withColumnRenamed("nome", "pais_nome")
        sistema_operacional = PostgresDAO().select('stackoverflow.sistema_operacional').withColumnRenamed("nome", "so_nome")
        empresa = PostgresDAO().select('stackoverflow.empresa')

        return metadata.get('source')\
        .join(pais, pais.pais_nome == col("Country"))\
        .join(sistema_operacional, sistema_operacional.so_nome == col("OperatingSystem"))\
        .join(empresa, empresa.tamanho == col("CompanySize"))
    
    @staticmethod
    def field_to_boolean(metadata):
        return metadata.get('source')\
        .withColumn("contrib_open_source", when(col("contrib_open_source") == 'Yes', lit(1)).otherwise(lit(0)))\
        .withColumn("programa_hobby", when(col("programa_hobby") == 'Yes', lit(1)).otherwise(lit(0)))\
        .withColumn("salario", col("salario").cast(DoubleType()))

@udf()
def exchange_conversion(currencySymbol, salary):
    global currencies
    defaul_value = 0.0
    try:
        return currencies.value[currencySymbol] * salary if salary is not None else defaul_value
    except KeyError as err:
        return defaul_value