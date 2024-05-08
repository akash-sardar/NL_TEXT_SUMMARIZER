import os
from NLPTextSummarizer.logging import logger
from NLPTextSummarizer.utils.common import get_size
from NLPTextSummarizer.entity import *
from pathlib import Path
from NLPTextSummarizer.logging import logger
from transformers import DataCollatorForSeq2Seq # type: ignore
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments # type: ignore
from datasets import load_from_disk, load_metric # type: ignore
import torch # type: ignore
from tqdm import tqdm # type: ignore
import pandas as pd # type: ignore

class ModelEvaluation:
    def __init__(self, config:ModelEvaluationConfig):
        self.config = config
    
    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        rouge_metric = load_metric("rouge", trust_remote_code=True)
        rouge_names = ["rouge1", "rouge2", "rougeL", "rougeLsum"]
        dataset_samsum_pt = load_from_disk(self.config.data_path)
        score = self.evaluate_score( dataset_samsum_pt["test"], rouge_metric,model, tokenizer, batch_size=2, device = device,  column_text="dialogue", column_summaries="summary")
        rouge_dict = dict((rn, score[rn].mid.fmeasure) for rn in rouge_names)
        pd.DataFrame(rouge_dict, index=[f"pegasus"]).to_csv(self.config.metric_file_name, index = False)      

    def chunks(self, list_of_elements, batch_size):
        for i in range(0, len(list_of_elements), batch_size):
            yield list_of_elements[i:i+batch_size]

    def evaluate_score(self, dataset, metric, model, tokenizer, batch_size = 16, device = "cpu", column_text = "article", column_summaries = "highlights"):
        article_batches = list(self.chunks(dataset[column_text], batch_size))
        target_batches = list(self.chunks(dataset[column_summaries], batch_size))
        for article_batch, target_batch in tqdm(zip(article_batches, target_batches), total = len(article_batches)):
            inputs = tokenizer(article_batch, max_length = 1024, truncation = True, padding = "max_length", return_tensors = "pt")
            summaries = model.generate(
                input_ids = inputs["input_ids"].to(device),
                attention_mask = inputs["attention_mask"].to(device),
                length_penalty = 0.8,
                max_length = 128
            )
            decoded_summaries = [tokenizer.decode(s, skip_special_tokes = True, clean_up_tokenization_spaces = True) for s in summaries]
            decoded_summaries = [d.replace("<n>"," ") for d in decoded_summaries]
            metric.add_batch(predictions = decoded_summaries, references = target_batch)

            
        score = metric.compute()
        return score