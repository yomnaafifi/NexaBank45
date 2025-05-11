import pandas as pd
from Transformers import BaseTransformer
from datetime import datetime

class TicketsTransformer(BaseTransformer):
    def transform(self):
        # Convert 'issue_date' to datetime
        self.df['complaint_date'] = pd.to_datetime(self.df['complaint_date'])
        
        # Calculate the age of the ticket in days
        self.df['age'] = (pd.Timestamp.now() - self.df['complaint_date']).dt.days
        
        # Add data quality columns
        self.add_data_quality_columns()

