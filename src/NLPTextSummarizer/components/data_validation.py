# 5. Update the components (./src/project_name/components/__init__.py)
import os
import urllib.request as request
import zipfile
from NLPTextSummarizer.logging import logger
from NLPTextSummarizer.utils.common import get_size
from NLPTextSummarizer.entity import *
from pathlib import Path

class DataValidation:
    def __init__(self, config:DataValidationConfig):
        self.config = config
    
    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = None
            all_files = os.listdir(os.path.join("artifacts", "data_ingestion", "samsum_dataset"))
            for file in all_files:
                if file not in self.config.ALL_REQUIRED_FILES:
                    validation_status = False
                    with open(self.config.STATUS_FILE, "w") as f:
                        f.write(f"Validation status: {validation_status}")
                else:
                    validation_status = True
                    with open(self.config.STATUS_FILE, 'w') as f:
                        f.write(f"Validation status:{validation_status}")
            return validation_status
        
        except Exception as e:
            raise e