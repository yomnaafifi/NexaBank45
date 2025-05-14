import os
from ETL.Extractors import *
from ETL.Transformer import *
from ETL.Loaders import *
from utils.Registry import *
from utils.logger import logger

class FileProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_name = os.path.basename(self.file_path)
        self.name_without_ext, self.ext = os.path.splitext(self.file_name)
        self.df = pd.DataFrame()

    def get_extractor(self) -> BaseExtractor.__class__: 
        if EXTRACTOR_REGISTRY.get(self.ext.lower()):
            return EXTRACTOR_REGISTRY.get(self.ext.lower())
        else:
            raise ValueError(f"No Extractor found for extension: {self.ext}")
    
    @logger    
    def extract(self) -> pd.DataFrame:
        self.df = self.get_extractor()(self.file_path).extract()

    def get_transformer(self) -> BaseTransformer.__class__: 
        if TRANSFORMER_REGISTRY.get(self.name_without_ext.lower()):
            return TRANSFORMER_REGISTRY.get(self.name_without_ext.lower())
        else:
            raise ValueError(f"No Transformer found for file: {self.name_without_ext}")

    @logger    
    def transform(self) -> pd.DataFrame:
        self.df = self.get_transformer()(self.df).transform()

    @logger
    def load(self) -> bool:
        LocalLoader(self.df, "tmp", self.name_without_ext).load()

    @logger
    def validate(self) -> bool:
        if self.name_without_ext in SCHEMA_REGISTRY.keys():
            expected_columns = SCHEMA_REGISTRY[self.name_without_ext].keys()
            if not all(col in self.df.columns for col in expected_columns):
                raise ValueError(f"DataFrame does not have the expected columns for {self.file_name}.")
            
            for col, expected_type in SCHEMA_REGISTRY[self.name_without_ext].items():
                if not pd.api.types.is_dtype_equal(self.df[col].dtype, expected_type):
                    raise ValueError(f"Column {col} in DataFrame does not have the expected type for {self.file_name}.")
                
        else:
            raise ValueError(f"File name {self.file_name} is not recognized.")
        return True
