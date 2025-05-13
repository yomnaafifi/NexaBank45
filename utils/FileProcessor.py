import os
from abc import ABC, abstractmethod
from typing import Dict, Type
from Extractors.BaseExtractor import BaseExtractor 
from Extractors.CSVExtractor import CSVExtractor 
from Extractors.JSONExtractor import JSONExtractor 
from Extractors.TXTExtractor import TXTExtractor
from Transformers.BaseTransformer import BaseTransformer
from Transformers.BillingTransformer import BillingTransformer
from Transformers.CustomerTransformer import CustomerTransformer
from Transformers.LoansTransformer import LoansTransformer
from Transformers.TicketsTransformer import TicketsTransformer
from Transformers.TransactionsTransformer import TransactionsTransformer      

from Loaders import *


class FileProcessor:
    # Registry of extractors by file extension
    EXTRACTORS: Dict[str, Type[BaseExtractor]] = {
        '.csv': CSVExtractor,
        '.json': JSONExtractor,
        '.txt': TXTExtractor
    }
    
    # Registry of transformers by filename pattern
    TRANSFORMERS: Dict[str, Type[BaseTransformer]] = {
        # Map filename patterns to transformer classes
        'billing': BillingTransformer,
        'invoice': BillingTransformer,  # Alternate key
        'customer': CustomerTransformer,
        'client': CustomerTransformer,   # Alternate key
        'loan': LoansTransformer,
        'mortgage': LoansTransformer,   # Alternate key
        'ticket': TicketsTransformer,
        'issue': TicketsTransformer,    # Alternate key
        'transaction': TransactionsTransformer,
        'payment': TransactionsTransformer,  # Alternate key
        'txn': TransactionsTransformer       # Short form
    }
    
    @classmethod
    def process_file(cls, file_path: str):
        _, ext = os.path.splitext(file_path)
        extractor_class = cls.EXTRACTORS.get(ext.lower())
        
        if not extractor_class:
            raise ValueError(f"No extractor found for file extension: {ext}")
        
        filename = os.path.basename(file_path).lower()
        transformer_class = None
        
        for pattern, t_class in cls.TRANSFORMERS.items():
            if pattern in filename:
                transformer_class = t_class
                break
        
        extractor = extractor_class()
        data = extractor.extract(file_path)
        
        if transformer_class:
            transformer = transformer_class()
            data = transformer.transform(data)
        
        return data

# # Example Usage
# if __name__ == "__main__":
#     # Example files (would be real paths in practice)
#     sales_csv = "sales_data_2023.csv"
#     customer_json = "customer_records.json"
#     inventory_parquet = "inventory.parquet"
    
#     # Process files
#     sales_data = FileProcessor.process_file(sales_csv)
#     customer_data = FileProcessor.process_file(customer_json)
    
#     print("Sales data processed:", sales_data.head())
#     print("Customer data processed:", customer_data.head())