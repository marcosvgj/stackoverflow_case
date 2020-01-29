
from service.stackoverflow import Pipeline
from common.utils.logger import logger

START_PIPELINE_MSG = "Starting StackOverflow pipeline"
ENDING_PIPELINE_MSG = "Ending StackOverflow pipeline"

class StackOverflow:    
    
    @staticmethod
    def run():
        logger.warn(START_PIPELINE_MSG)
        pipeline = Pipeline()
        pipeline.run()
        logger.warn(ENDING_PIPELINE_MSG)
        
    