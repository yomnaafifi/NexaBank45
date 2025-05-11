import pandas as pd
from Transformers.BaseTransformer import BaseTransformer 

class TransactionsTransformer(BaseTransformer):
    def transform(self):
        """Transform the transactions data by calculating cost and total amount."""
        
        self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'])
    
        self.df['cost'] = 0.5 + (self.df['transaction_amount'] * 0.001)

        self.df['total_amount'] = self.df['transaction_amount'] + self.df['cost']
        
        self.add_data_quality_columns()















