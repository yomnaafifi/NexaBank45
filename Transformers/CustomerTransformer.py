import pandas as pd
import numpy as np
import BaseTransformer
from datetime import datetime

class CustomerTransformer(BaseTransformer):
    def transform(self):
        # Calculate tenure (years since account opened)
        self.df['account_open_date'] = pd.to_datetime(self.df['account_open_date'])
        self.df['tenure'] = (datetime.now() - self.df['account_open_date']).dt.days // 365
        
        # Segment customers
        self.df['customer_segment'] = pd.cut(
            self.df['tenure'],
            bins=[-np.inf, 1, 5, np.inf],
            labels=['Newcomer', 'Normal', 'Loyal']
        )
        self.add_data_quality_columns()
