from pyspark.sql.types import StructField, StringType, IntegerType, StringType, StructType, DoubleType

class CommunicationToolModel(StructType):
    @property
    def schema(self):    
        return StructType([
            StructField('ferramenta_comunic_id', IntegerType(), False),
            StructField('nome', StringType(), False)])

class SOModel(StructType):
    @property
    def schema(self):
        return StructType([
                    StructField('sistema_operacional_id', IntegerType(), False),
                    StructField('nome', StringType(), False)])
    
class LanguageWorkedWithModel(StructType):
    @property
    def schema(self):    
        return StructType([
            StructField('linguagem_programacao_id', IntegerType(), False),
            StructField('nome', StringType(), False)])
    
class CompanyModel(StructType):
    @property
    def schema(self):    
        return StructType([
            StructField('empresa_id', IntegerType(), False),
            StructField('tamanho', StringType(), False)])

class CountryModel(StructType):
    @property
    def schema(self):    
        return StructType([
            StructField('pais_id', IntegerType(), False),
            StructField('nome', StringType(), False)])

class RespLanguageModel(StructType):
    @property
    def schema(self):    
        return StructType([
            StructField('resp_usa_linguagem_id', IntegerType(), False),
            StructField('respondente_id', IntegerType(), False),
            StructField('linguagem_programacao_id', IntegerType(), False),
            StructField('momento', IntegerType(), False)])
    
class RespToolsModel(StructType):
    @property
    def schema(self):    
        return StructType([
            StructField('resp_usa_ferramenta_id', IntegerType(), False),
            StructField('respondente_id', IntegerType(), False),
            StructField('ferramenta_comunic_id', IntegerType(), False)])

class RespondentModel(StructType):
    @property
    def schema(self):    
        return StructType([
            StructField("respondente_id", IntegerType(), False),
            StructField("nome", StringType(), False),
            StructField("contrib_open_source", IntegerType(), False),
            StructField("programa_hobby", IntegerType(), False),
            StructField("salario", DoubleType(), False),
            StructField("sistema_operacional_id", IntegerType(), False),
            StructField("pais_id", IntegerType(), False),
            StructField("empresa_id", IntegerType(), False)])