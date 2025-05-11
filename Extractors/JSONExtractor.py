import pandas as pd
from Extractors.BaseExtractor import BaseExtractor
class JSONExtractor(BaseExtractor):
    def __init__(self, file: str):
        super().__init__(file)

    def extract(self) -> pd.DataFrame:
        """
        Extract data from a JSON file using pandas.
        """
        return pd.read_json(self.file)
        