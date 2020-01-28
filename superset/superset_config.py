import os
import time 
import psycopg2
import logging
from werkzeug.contrib.cache import FileSystemCache

logger = logging.getLogger()

def start_superset_config():
    return """

    Starting of customized superset_config.py:

    Environment Variables:
        DATABASE_DIALECT
        POSTGRES_USER
        POSTGRES_PASSWORD
        POSTGRES_HOST
        POSTGRES_PORT
        POSTGRES_DB
        SUPERSET_DB
        SLEEP_TIME
        
    Functions:
        get_sqlalchemy_database_uri: sqlalchemy_database_uri string constructor
        get_env_variable: get an environment variable given name
        wait_connection: wrap function to connection test
        verify_connection: returns True if the connection are stable. Otherwise False
        verify_metadata_availability: returns True if the connection are stable with a specific table. Otherwise False
    
    """
def show_parameters():
    global DATABASE_DIALECT
    global POSTGRES_USER
    global POSTGRES_PASSWORD
    global POSTGRES_HOST
    global POSTGRES_PORT
    global POSTGRES_DB

    return """
        PARAMETERS VALUES:
        
        -- USER: %s
        -- PASSWORD: %s
        -- HOST: %s
        -- PORT: %s 
        -- POSTGRES_DB: %s

        """ % (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)

def get_sqlalchemy_database_uri():
    global DATABASE_DIALECT
    global POSTGRES_USER
    global POSTGRES_PASSWORD
    global POSTGRES_HOST
    global POSTGRES_PORT
    global POSTGRES_DB

    return "%s://%s:%s@%s:%s/%s" % (
        DATABASE_DIALECT,
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB)

def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)

def verify_connection():
    """Returns True if the connection are responsible. Otherwise False"""
    global CONNECTION
    try:
        cur=CONNECTION.cursor()
        cur.execute("SELECT version();")
    except:
        logger.error("No connection avaiable yet")
        return False
    logger.info("Connection ok. Procceed...")
    return True

def wait_connection(func):
    global SLEEP_TIME
    while func() == False:
        time.sleep(int(SLEEP_TIME))

################################################# running #################################################

DATABASE_DIALECT = get_env_variable("DATABASE_DIALECT")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_variable("POSTGRES_PASSWORD")
POSTGRES_HOST = get_env_variable("POSTGRES_HOST")
POSTGRES_PORT = get_env_variable("POSTGRES_PORT")
SUPERSET_DB = get_env_variable("SUPERSET_DB")
POSTGRES_DB = get_env_variable("POSTGRES_DB")
SLEEP_TIME = get_env_variable("SLEEP_TIME")

SQLALCHEMY_DATABASE_URI = get_sqlalchemy_database_uri()
start_superset_config()
show_parameters()

CONNECTION = psycopg2.connect(host=POSTGRES_HOST, database=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)
wait_connection(verify_connection)