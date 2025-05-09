import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime

class BaseTransformer(ABC):
    def __init__(self, data_frame: pd.DataFrame):
        self.df = data_frame

    @abstractmethod
    def transform(self):
        pass

    def add_data_quality_columns(self):
        self.df['processing_time'] = datetime.now()
        self.df['partition_date'] = datetime.now().date()
        self.df['partition_hour'] = datetime.now().hour
