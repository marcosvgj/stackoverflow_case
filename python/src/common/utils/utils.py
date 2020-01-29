import os
import sys
from pyspark.sql import types

def get_model_class(name):
    """ Get class of Model given name """
    module_name = get_env_variable('MODEL_PATH')
    return getattr(sys.modules[module_name], name)

def get_env_variable(var, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var]
    except KeyError:
        ERROR_MSG = "The environment variable {} was missing. ".format(var)
        if default is not None: 
            return default
        else:
            raise EnvironmentError(ERROR_MSG)

def get_type(name):
    return getattr(types, name)()

def get_spark_jar():
    """ Get class of Model given name """
    return get_env_variable('USED_JAR_PATH')
    