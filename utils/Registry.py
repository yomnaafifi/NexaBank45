from ETL.Extractors import *
from ETL.Transformer import *
import numpy
import pandas as pd

SCHEMA_REGISTRY: dict[str, dict[str,]] = {
    "customer_profiles" : {"customer_id" : pd.StringDtype, "name" : pd.StringDtype , "gender" : pd.StringDtype, "age" : int, "city" : pd.StringDtype, "account_open_date" : numpy.object_, "product_type" : pd.StringDtype, "customer_tier" : pd.StringDtype},
    "credit_cards_billing" : {"bill_id" : pd.StringDtype, "customer_id" : pd.StringDtype, "month" : numpy.object_, "amount_due" : float, "amount_paid" : float, "payment_date" : numpy.object_},
    "support_tickets" : {"ticket_id" : pd.StringDtype, "customer_id" : pd.StringDtype, "complaint_category" : pd.StringDtype, "complaint_date" : numpy.object_, "severity" : int},
    "loans" : {"customer_id" : pd.StringDtype, "loan_type" : pd.StringDtype, "amount_utilized" : int, "utilization_date" : numpy.object_, "loan_reason" : pd.StringDtype},
    "transactions" : {"sender" : pd.StringDtype, "receiver" : pd.StringDtype, "transaction_amount" : int, "transaction_date" : numpy.object_}
}

EXTRACTOR_REGISTRY: dict[str, BaseExtractor] = {
    ".csv": CSVExtractor,
    ".txt": TextExtractor,
    ".json": JSONExtractor,
}

TRANSFORMER_REGISTRY: dict[str, BaseTransformer] = {
    "customer_profiles": CustomerTransformer,
    "credit_cards_billing": BillingTransformer,
    "support_tickets": TicketsTransformer,
    "loans": LoansTransformer,
    "transactions": TransactionsTransformer,
}
