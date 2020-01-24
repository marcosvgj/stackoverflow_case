import socket

class PostgresDAO(DAO):
    def __init__(self):
        """API to access Postgres RDBMS - DAO Implementation"""
        
        secret = configuration()
        self.host = socket.gethostbyname(socket.gethostname())
        self.user = secret.postgres.user
        self.password = secret.postgres.password
        self.port = secret.postgres.port
        
    def select(self, db_table):
        """Query engine to this DAO implementation"""
        try:
            return spark.read\
            .format('jdbc')\
            .option('url', f'jdbc:postgresql://{self.host}:{self.port}/{self.database}')\
            .option('dbtable', f'{db_table}')\
            .option('user', self.user)\
            .option('password', self.password)\
            .option('driver', 'org.postgresql.Driver')\
            .load()     
        except Exception as err: 
            logger.error(err.errno)
            
    def insert(self, db_table, dataframe):
        """Data ingestion engine to this DAO implementation"""
        try:
            data.write\
            .format('jdbc')\
            .option('url', f'jdbc:postgresql://{self.host}:{self.port}/{self.database}')\
            .option('dbtable', f'{db_table}')\
            .option('user', self.user)\
            .option('password', self.password)\
            .option('driver', 'org.postgresql.Driver')\
            .mode('append')\
            .save()
        except Exception as err: 
            logger.error(err.errno)