# 5. Update the components (./src/project_name/components/__init__.py)
import os
import urllib.request as request
import zipfile
from NLPTextSummarizer.logging import logger
from NLPTextSummarizer.utils.common import get_size
from NLPTextSummarizer.entity import *
from pathlib import Path

class DataIngestion:
    def __init__(self, config:DataIngestionConfig):
        self.config = config
    
    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url = self.config.source_URL,
                filename = self.config.local_data_file
            )
            logger.info(f"{filename} donloaded with follwoing info:\n {headers}")
        else:
            logger.info(f"{self.config.local_data_file} already exists of size: {get_size(Path(self.config.local_data_file))}")

    
    def extract_zip_file(self):
        '''
        zip_file_path = str
        Extarcts the zip file into the data directory
        Function return None
        '''
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok = True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)