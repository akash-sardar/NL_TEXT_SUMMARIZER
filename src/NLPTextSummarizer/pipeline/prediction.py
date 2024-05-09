from NLPTextSummarizer.config.configuration import *
from transformers import pipeline
from transformers import AutoTokenizer

class PredcitionPipeline:
    def __init__(self):
        config = ConfigurationManager()
        self.config = config.get_model_evaluation_config()
    
    def predict(self, text):
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        gen_kwargs = {
           "length_penalty" : 0.8,
            "num_beams" : 8,
            "max_length" : 128
        }
        pipe = pipeline("summarization", model = self.config.model_path, tokenizer=tokenizer)
        print("Dialogue:")
        print(text)
        output = pipe(text, **gen_kwargs)[0]["summary_text"]
        print("\nModel Summary:\n")
        print(output)
        return output