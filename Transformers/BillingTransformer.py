import pandas as pd
import BaseTransformer

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
