import os
import yaml
from common.utils.logger import logger

DEFAULT_CONFIGURATION_FILE='resources/configuration.yml'

def configuration(abs_path=None):
    root = os.path.dirname(os.path.abspath("__main__"))
    path = abs_path if abs_path is not None else os.path.join(root, DEFAULT_CONFIGURATION_FILE)
    try:
        with open(path) as cfg:
            return yaml.load(cfg, Loader=yaml.FullLoader)
    except Exception as error:
        logger.error(f'Fail to read configuration file: {error}')