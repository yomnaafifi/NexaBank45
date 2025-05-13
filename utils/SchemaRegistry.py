from ETL.Extractors import *
from ETL.Transformer import *

ValidSchemas = {
    "customer_profiles" : ["customer_id", "name", "gender", "age", "city", "account_open_date", "product_type","customer_tier"],
    "credit_cards_billing" : ["bill_id", "customer_id", "month", "amount_due", "amount_paid", "payment_date"],
    "support_tickets" : ["ticket_id", "customer_id", "complaint_category", "complaint_date", "severity"],
    "loans" : ["customer_id", "loan_type", "amount_utilized", "utilization_date", "loan_reason"],
    "transactions" : ["sender", "receiver", "transaction_amount", "transaction_date"]
}



ValidType= {
    "customer_profiles" : {"customer_id" : int, "name" : str , "gender" : str, "age" : int, "city" : str, "account_open_date" : datetime.date, "product_type" : str, "customer_tier" : str},
    "credit_cards_billing" : {"bill_id" : int, "customer_id" : int, "month" : str, "amount_due" : float, "amount_paid" : float, "payment_date" : datetime.date},
    "support_tickets" : {"ticket_id" : int, "customer_id" : int, "complaint_category" : str, "complaint_date" : datetime.date, "severity" : str},
    "loans" : {"customer_id" : int, "loan_type" : str, "amount_utilized" : float, "utilization_date" : datetime.date, "loan_reason" : str},
    "transactions" : {"sender" : int, "receiver" : int, "transaction_amount" : float, "transaction_date" : datetime.date}
}



EXTRACTOR_REGISTRY = {
    ".csv": CSVExtractor,
    ".txt": TextExtractor,
    ".json": JSONExtractor,
}

TRANSFORMER_REGISTRY = {
    "customer_profiles": CustomerTransformer,
    "credit_cards_billing": BillingTransformer,
    "support_tickets": TicketsTransformer,
    "loans": LoansTransformer,
    "transactions": TransactionsTransformer,
}