# Pipeline component
from NLPTextSummarizer.config.configuration import *
from NLPTextSummarizer.components.model_evaluation import *

class ModelEvaluationTrainingPipeline:
    def __init__(self):
        pass

    def main(self):
        try:
            config = ConfigurationManager()
            model_evaluation_config = config.get_model_evaluation_config()
            model_evaluation = ModelEvaluation(config = model_evaluation_config) 
            model_evaluation.evaluate()
        except Exception as e:
            raise e 