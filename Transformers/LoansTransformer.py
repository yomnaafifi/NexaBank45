import pandas as pd
from Transformers.BaseTransformer import BaseTransformer
from utils.encryption import CaesarCipher


class LoansTransformer(BaseTransformer):
    def transform(self):

        """Transform the loans data by calculations and encrypting sensitive information."""
        
        self.df['utilization_date'] = pd.to_datetime(self.df['utilization_date'])
        
        self.df['age'] = (pd.Timestamp.now() - self.df['utilization_date']).dt.days
        
        self.df['total_cost'] = (self.df['amount_utilized'] * 0.20) + 1000

        self.df['loan_reason'] = self.df['loan_reason'].apply(CaesarCipher.encrypt)
        
        self.add_data_quality_columns()

         