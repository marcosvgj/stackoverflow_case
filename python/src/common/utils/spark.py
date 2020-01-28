from pyspark.sql import SparkSession

def getOrCreate():
    return SparkSession.builder\
                .master("local[*]")\
                .appName("Data engineering at Ame Digital")\
                .config("spark.jars", "/home/marcos/dataengineeringatame/python/jars/postgresql-9.4.1207.jre6.jar")\
                .getOrCreate()