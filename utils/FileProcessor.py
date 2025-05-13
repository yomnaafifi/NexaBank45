import os
from ETL.Extractors import *
from ETL.Transformer import *
from ETL.Loaders import *
from utils.Registry import *

class FileProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.name_without_ext, self.ext = os.path.splitext(self.file_name)

    def get_extractor(self) -> BaseExtractor: 
        if EXTRACTOR_REGISTRY.get(self.ext.lower()):
            return EXTRACTOR_REGISTRY.get(self.ext.lower())(self.file_path)
        else:
            raise ValueError(f"No Extractor found for extension: {self.ext}")
    
    def get_transformer(self) -> BaseTransformer.__class__: 
        if TRANSFORMER_REGISTRY.get(self.name_without_ext.lower()):
            return TRANSFORMER_REGISTRY.get(self.name_without_ext.lower())
        else:
            raise ValueError(f"No Transformer found for file: {self.name_without_ext}")
            
    def validate(self, data: pd.DataFrame) -> bool:
        if self.name_without_ext in SCHEMA_REGISTRY.keys():
            expected_columns = SCHEMA_REGISTRY[self.name_without_ext].keys()
            if not all(col in data.columns for col in expected_columns):
                print(f"DataFrame does not have the expected columns for {self.file_name}.")
                return False
            
            for col, expected_type in SCHEMA_REGISTRY[self.name_without_ext].items():
                if not pd.api.types.is_dtype_equal(data[col].dtype, expected_type):
                    print(f"Column {col} in DataFrame does not have the expected type for {self.file_name}.")
                    return False
                
        else :
            print(f"File name {self.file_name} is not recognized.")
            return False
        return True 