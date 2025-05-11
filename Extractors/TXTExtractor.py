import pandas as pd
from Extractors.BaseExtractor import BaseExtractor
class TextExtractor(BaseExtractor):
    def __init__(self, file: str):
        super().__init__(file)

    def extract(self) -> pd.DataFrame:
        """
        Extract data from a plain text file using pandas.
        """
        return pd.read_csv(self.file, sep='|')
        