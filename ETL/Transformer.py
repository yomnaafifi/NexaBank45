# i need to put all the traanformer code in this file
# starting with the base class

import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from datetime import datetime
from utils.encryption import CaesarCipher

class BaseTransformer(ABC):
    def __init__(self, data_frame: pd.DataFrame):
        self.df = data_frame

    @abstractmethod
    def transform(self) -> pd.DataFrame: 
        pass

    def add_data_quality_columns(self) -> None:   
        self.df['processing_time'] = datetime.now()
        self.df['partition_date'] = datetime.now().date()
        self.df['partition_hour'] = datetime.now().hour
        
class BillingTransformer(BaseTransformer):
    def transform(self):
        # Calculate payment metrics
        self.df['payment_date'] = pd.to_datetime(self.df['payment_date'])
        self.df['due_date'] = pd.to_datetime(self.df['month'] + '-01')
        
        self.df['late_days'] = (self.df['payment_date'] - self.df['due_date']).dt.days
        self.df['fully_paid'] = self.df['amount_paid'] >= self.df['amount_due']
        self.df['debt'] = self.df['amount_due'] - self.df['amount_paid']
        self.df['fine'] = self.df['late_days'].apply(lambda x: max(x, 0) * 5.15)
        self.df['total_amount'] = self.df['amount_due'] + self.df['fine']
        self.add_data_quality_columns()

        return self.df

class CustomerTransformer(BaseTransformer):
    def transform(self):
        
        self.df['account_open_date'] = pd.to_datetime(self.df['account_open_date'])
        self.df['tenure'] = (datetime.now() - self.df['account_open_date']).dt.days // 365
        
        self.df['customer_segment'] = pd.cut(
            self.df['tenure'],
            bins=[-np.inf, 1, 5, np.inf],
            labels=['Newcomer', 'Normal', 'Loyal']
        )
        self.add_data_quality_columns()
        return self.df

class LoansTransformer(BaseTransformer):
    def transform(self):

        """Transform the loans data by calculations and encrypting sensitive information."""
        
        self.df['utilization_date'] = pd.to_datetime(self.df['utilization_date'])
        
        self.df['age'] = (pd.Timestamp.now() - self.df['utilization_date']).dt.days
        
        self.df['total_cost'] = (self.df['amount_utilized'] * 0.20) + 1000

        self.df['loan_reason'] = self.df['loan_reason'].apply(CaesarCipher.encrypt)
        
        self.add_data_quality_columns()
        return self.df

  
class TicketsTransformer(BaseTransformer):
    def transform(self):
    
        self.df['complaint_date'] = pd.to_datetime(self.df['complaint_date'])
        
        self.df['age'] = (pd.Timestamp.now() - self.df['complaint_date']).dt.days
        
        self.add_data_quality_columns()
        return self.df

class TransactionsTransformer(BaseTransformer):
    def transform(self):
        """Transform the transactions data by calculating cost and total amount."""
        
        self.df['transaction_date'] = pd.to_datetime(self.df['transaction_date'])
    
        self.df['cost'] = 0.5 + (self.df['transaction_amount'] * 0.001)

        self.df['total_amount'] = self.df['transaction_amount'] + self.df['cost']
        
        self.add_data_quality_columns()
        return self.df




