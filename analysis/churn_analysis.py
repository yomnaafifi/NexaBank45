import pandas as pd
import numpy as np
from datetime import datetime, timedelta

customer_profiles = pd.read_parquet('customer_profiles.parquet')
credit_cards_billing = pd.read_parquet('credit_cards_billing.parquet')
transactions = pd.read_parquet('transactions.parquet')

# define churn (90+ days inactive)
analysis_date = pd.to_datetime('today').date()
last_transaction = transactions.groupby('sender')['transaction_date'].max()
churned_customers = last_transaction[last_transaction < (analysis_date - timedelta(days=90))].index

customer_profiles['age_group'] = pd.cut(customer_profiles['age'],
                                       bins=[0, 30, 40, 50, 60, 100],
                                       labels=['<30', '30-39', '40-49', '50-59', '60+'])

customer_spending = transactions.groupby('sender')['transaction_amount'].sum()
customer_profiles = customer_profiles.merge(
    customer_spending.rename('total_spending'),
    left_on='customer_id',
    right_index=True,
    how='left'
)
customer_profiles['spending_level'] = pd.qcut(
    customer_profiles['total_spending'],
    4,
    labels=['Low', 'Medium', 'High', 'VIP']
)

# mark churned customers
customer_profiles['is_churned'] = customer_profiles['customer_id'].isin(churned_customers)

# churn rate across different segments (age, city, spending)
churn_by_age = customer_profiles.groupby('age_group')['is_churned'].mean()
churn_by_city = customer_profiles.groupby('city')['is_churned'].mean().sort_values(ascending=False)
churn_by_spending = customer_profiles.groupby('spending_level')['is_churned'].mean()

# late payment analysis
credit_cards_billing['payment_date'] = pd.to_datetime(credit_cards_billing['payment_date'])
credit_cards_billing['month'] = pd.to_datetime(credit_cards_billing['month'])
credit_cards_billing['days_late'] = (credit_cards_billing['payment_date'] - credit_cards_billing['month']).dt.days - 15

payment_behavior = credit_cards_billing.groupby('customer_id').agg(
    avg_days_late=('days_late', 'mean'),
    late_payment_ratio=('days_late', lambda x: (x > 0).mean())
)

# join churn data with payment behavior
payment_churn = customer_profiles[['customer_id', 'is_churned']].merge(
    payment_behavior,
    on='customer_id',
    how='left'
)

# Calculate correlations
correlation = payment_churn.corr()['is_churned'][['avg_days_late', 'late_payment_ratio']]