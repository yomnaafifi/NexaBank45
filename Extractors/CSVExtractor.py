import pandas as pd
import BaseExtractor
class CSVExtractor(BaseExtractor):
    def __init__(self, file: str):
        super().__init__(file)
        
    def extract(self) -> pd.DataFrame:
        """
        Extract data from a CSV file using pandas.
        """
        data = pd.read_csv(self.file)
        return data
