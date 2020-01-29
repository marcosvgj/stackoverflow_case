from common.utils import spark
from dao.postgres import PostgresDAO
from pyspark.sql.functions import col, explode, split, when, lit, udf, concat, asc, row_number
from dao.external.api.exchange import ExchangeDAO
from common.utils.utils import get_type
from pyspark.sql.window import Window
from pyspark.sql.types import *

currencies = spark.getOrCreate().sparkContext.broadcast(ExchangeDAO(sleep=0.5, retries=2, timeout=5).collect())

class DimensionRules(object):
    @staticmethod
    def create_index(field, source):
        return map(lambda x, y: (x+1, y.asDict()[field]), range(0, len(source)), source)
    
    @staticmethod
    def dictionaryization(metadata):
        """ Responsible to implement business logic to dimensional tables """
        model = metadata.get('model')
        field = metadata.get('description_field')

        if metadata.get('embbebedList') == False:
            data = check_nullity(field=field, metadata=metadata)\
                .select(field)\
                .distinct()\
                .collect()
        else:
            data = check_nullity(field=field, metadata=metadata)\
                .select(field)\
                .withColumn(field, split(col(field), ';'))\
                .withColumn(field, explode(col(field)))\
                .distinct()\
                .collect()
        
        return spark.getOrCreate().createDataFrame(DimensionRules.create_index(field, data), model().schema)

class FactRules(object):    
    
    @staticmethod
    def salary_standardization(metadata):
        year_month = col('ConvertedSalary')/12
        conversion = exchange_conversion("CurrencySymbol","ConvertedSalary")

        return metadata.get('source')\
        .withColumn("ConvertedSalary", year_month)\
        .withColumn("ConvertedSalary", conversion)\
        
    @staticmethod
    def respondent_name_creation(metadata):
        return metadata.get('source').withColumn('nome', concat(lit('respondente_'), col('Respondent')))
    
    @staticmethod
    def columns_renames(metadata):
        return metadata.get('source')\
        .withColumnRenamed("ConvertedSalary", "salario")\
        .withColumnRenamed("OpenSource", "contrib_open_source")\
        .withColumnRenamed("Hobby", "programa_hobby")\
        .withColumnRenamed("Respondent", "respondente_id")
    
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
        

    @staticmethod
    def types_converter(metadata):
        return metadata.get('source')\
            .withColumn("salario", col("salario").cast(DoubleType()))\
            .withColumn("respondente_id", col("respondente_id").cast(IntegerType()))

class MiddleEntityRules(object):

    @staticmethod
    def createIndex(ordered_column, index, source):
        w = Window.orderBy(asc(ordered_column))
        return source.withColumn(index, row_number().over(w))

    @staticmethod
    def generate_intermediary_entity(metadata):
        model = metadata.get('model')
        options = metadata.get('options')
        field = metadata.get('description_field')
        table = options.get('right_table')
        database = options.get("right_database")
        
        right_table = PostgresDAO().select('%s.%s' % (database, table))
        left_table = check_nullity(metadata=metadata, field=field)
        
        if metadata.get('embbebedList') == False:
            data = left_table\
                .select(options.get('left_columns_selected'))\
                .join(right_table, col(options.get('right_original_column_target')) == getattr(right_table, options.get("right_column_target")))\
                .withColumnRenamed(options.get('left_original_column_id'), options.get('left_column_id'))
            
            data = MiddleEntityRules.createIndex(options.get('left_column_id'), options.get('right_column_id'), data)\
                .select(model().schema.fieldNames())
        else:
            data = left_table\
                .select(options.get('left_columns_selected'))\
                .withColumn(field, split(col(options.get("right_original_column_target")), ';'))\
                .withColumn(field, explode(col(options.get("right_original_column_target"))))\
                .join(right_table, col(options.get('right_original_column_target')) == getattr(right_table, options.get("right_column_target")))\
                .withColumnRenamed(options.get('left_original_column_id'), options.get('left_column_id'))\
                .withColumn(options.get('left_column_id'), col(options.get('left_column_id')).cast(IntegerType()))

            data = MiddleEntityRules.createIndex(options.get('left_column_id'), options.get('right_column_id'), data)
        if options.get("has_adicional_columns") == True:
            for i in options.get("adicional_columns"):
                setup = options.get("adicional_columns_definition")[i]
                data = data.withColumnRenamed(i, setup["name"])
                if setup.get("has_conversion_values") == True:
                    global MAPPER
                    MAPPER = spark.getOrCreate().sparkContext.broadcast(setup["conversion_values"])
                    data = data.withColumn(setup['name'], conversor(setup['name']))
                    data = data.withColumn(setup['name'], col(setup['name']).cast(get_type(setup['column_type'])))
        return data.select(model().schema.fieldNames())

@udf()
def exchange_conversion(currencySymbol, salary):
    global currencies
    defaul_value = 0.0
    try:
        return currencies.value[currencySymbol] * salary if salary is not None else defaul_value
    except KeyError:
        return defaul_value

@udf()
def conversor(field):
    try:
        return MAPPER.value[field]
    except KeyError:
        return MAPPER.value['others']

def check_nullity(metadata, field, in_null_cases='Not Specified'):
    """ Responsible for verifying the field's integrity given dataframe """
    return metadata.get('source').\
        withColumn(field, when(col(field).isNull(), lit(in_null_cases))\
        .otherwise(col(field)))