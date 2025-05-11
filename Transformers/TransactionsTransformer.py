import pandas as pd
from Transformers.BaseTransformer import BaseTransformer 
from datetime import datetime

def calculate_cost(row):
    """
    Calculate the cost of a transaction based on the given formula.
    """
    transaction_amount = row['transaction_amount']
    cost = 0.5 + (0.001 * transaction_amount)
    return cost
def calculate_total_amount(row):
    """
    Calculate the total amount of a transaction.
    """
    transaction_amount = row['transaction_amount']
    cost = calculate_cost(row)
    total_amount = transaction_amount + cost
