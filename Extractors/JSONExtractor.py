import pandas as pd
import BaseExtractor
class JSONExtractor(BaseExtractor):
    def __init__(self, file: str):
        super().__init__(file)

    def extract(self) -> pd.DataFrame:
        """
        Extract data from a JSON file using pandas.
        """
        data = pd.read_json(self.file)
        return data
