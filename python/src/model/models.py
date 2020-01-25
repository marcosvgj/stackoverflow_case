from pyspark.sql.types import StructField, StringType, IntegerType, StringType, StructType, DoubleType

class CommunicationToolModel:
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
    
class LanguageWorkedWithModel:
    @property
    def schema(self):    
        return StructType([
            StructField('linguagem_programacao_id', IntegerType(), False),
            StructField('nome', StringType(), False)])
    
class CompanyModel:
    @property
    def schema(self):    
        return StructType([
            StructField('empresa_id', IntegerType(), False),
            StructField('tamanho', StringType(), False)])

class CountryModel:
    @property
    def schema(self):    
        return StructType([
            StructField('pais_id', IntegerType(), False),
            StructField('nome', StringType(), False)])

class RespLanguageModel:
    @property
    def schema(self):    
        return StructType([
            StructField('resp_usa_linguagem_id', IntegerType(), False),
            StructField('respondente_id', IntegerType(), False),
            StructField('linguagem_programacao_id', IntegerType(), False),
            StructField('momento', IntegerType(), False)])
    
class RespToolsModel:
    @property
    def schema(self):    
        return StructType([
            StructField('resp_usa_ferramenta_id', IntegerType(), False),
            StructField('respondente_id', IntegerType(), False),
            StructField('ferramenta_comunic_id', IntegerType(), False)])

class RespondentModel:
    @property
    def schema(self):    
        return StructType([
            StructField("respondente_id", IntegerType(), False),
            StructField("contrib_open_source", IntegerType(), False),
            StructField("programa_hobby", IntegerType(), False),
            StructField("salario", DoubleType(), False),
            StructField("sistema_operacional_id", IntegerType(), False),
            StructField("pais_id", IntegerType(), False),
            StructField("empresa_id", IntegerType(), False)])