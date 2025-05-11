import pandas as pd
from Transformers.BaseTransformer import BaseTransformer

class TicketsTransformer(BaseTransformer):
    def transform(self):
    
        self.df['complaint_date'] = pd.to_datetime(self.df['complaint_date'])
        
        self.df['age'] = (pd.Timestamp.now() - self.df['complaint_date']).dt.days
        
        self.add_data_quality_columns()

