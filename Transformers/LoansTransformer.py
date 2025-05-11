import pandas as pd
from Transformers import BaseTransformer
from datetime import datetime
from utils.encryption import CaesarCipher


class LoansTransformer(BaseTransformer):
    def transform(self):
        # Convert 'issue_date' to datetime
        self.df['utilization_date'] = pd.to_datetime(self.df['utilization_date'])
        
        # Calculate the age of the loan in days
        self.df['age'] = (pd.Timestamp.now() - self.df['utilization_date']).dt.days
        
        # Calculate the total cost of the loan
        self.df['total_cost'] = (self.df['amount_utilized'] * 0.20) + 1000

        # Encrypt the 'loan_reason' column 
        self.df['loan_reason'] = self.df['loan_reason'].apply(
            lambda x: CaesarCipher.encrypt(x, shift=3) if isinstance(x, str) else x
        )
        
        # Add data quality columns
        self.add_data_quality_columns()

         