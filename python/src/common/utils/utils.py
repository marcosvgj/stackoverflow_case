import os
import sys

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

def instanceOf(C, subclass):
    try:
        print(list(filter(lambda x: x.__name__ == subclass, C.__subclasses__())))
        return next(filter(lambda x: x.__name__ == subclass, C.__subclasses__()).__iter__())
    except StopIteration as error:
        raise Exception('Please verify if this feature was implemented: %s' % error)